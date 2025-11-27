"""Fetch real models from NHTSA VPIC for ALL makes and populate data/models.json comprehensively."""
import requests
import json
import time
import os
import urllib.parse

BASE = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE, 'data', 'models.json')
BACKUP_PATH = DATA_PATH + '.bak'

VPIC_BASE = 'https://vpic.nhtsa.dot.gov/api/vehicles'

def infer_subtiers(vtype, model_name):
    """Infer subtier options based on vehicle type."""
    t = (vtype or '').lower()
    name = (model_name or '').lower()
    if 'truck' in t or 'pickup' in name:
        return ["Single-Cab", "Double-Cab", "Crew-Cab"]
    if 'coupe' in t or 'roadster' in t or 'coupe' in name or 'roadster' in name:
        return ["2-Door"]
    if 'sedan' in t or 'sedan' in name:
        return ["4-Door"]
    if 'hatch' in t or 'hatchback' in name:
        return ["3-Door", "5-Door"]
    if 'suv' in t or 'crossover' in t or 'wagon' in t:
        return ["Standard"]
    if 'van' in t or 'minivan' in t:
        return ["Standard", "Extended"]
    return ["Standard"]

def infer_vehicle_type_from_model_name(model_name):
    """Infer vehicle type from model name patterns."""
    name = (model_name or '').lower()
    if any(x in name for x in ['f-', 'f1', 'f2', 'f3', 'silverado', 'sierra', 'ram', 'tundra', 'tacoma', 'frontier', 'colorado', 'ranger', 'truck']):
        return 'Truck'
    if any(x in name for x in ['roadster', 'miata', 'mx-5']):
        return 'Roadster'
    if any(x in name for x in ['911', 'boxster', 'cayman', 'corvette', 'camaro', 'challenger', 'mustang', 'coupe']):
        return 'Coupe'
    if any(x in name for x in ['suv', 'explorer', 'escape', 'expedition', 'tahoe', 'suburban', 'yukon', 'denali', 'rogue', 'pathfinder', 'highlander', 'rav4', 'cx-', 'q3', 'q5', 'q7', 'x3', 'x5', 'x7', 'gla', 'gle', 'glc', 'forester', 'crosstrek', 'outback', 'wrangler', 'cherokee', 'grand cherokee', 'compass', 'renegade']):
        return 'SUV'
    if any(x in name for x in ['sedan', 'accord', 'civic', 'camry', 'corolla', 'prius', 'altima', 'maxima', 'sentra', 'elantra', 'sonata', 'forte', 'rio', 'optima', 'a3', 'a4', 'a6', 'a8', '3 series', '5 series', '7 series', 'c-class', 'e-class', 's-class', 'is', 'es', 'gs', 'ls', 'model 3', 'model s', 'charger']):
        return 'Sedan'
    if any(x in name for x in ['hatch', 'golf', 'focus']):
        return 'Hatchback'
    if any(x in name for x in ['wagon', 'outback']):
        return 'Wagon'
    if any(x in name for x in ['van', 'odyssey', 'sprinter', 'promeaster']):
        return 'Van'
    if any(x in name for x in ['minivan']):
        return 'Minivan'
    return 'Unknown'

def get_models_for_make(make):
    """Fetch real models from VPIC for a make."""
    url = f"{VPIC_BASE}/GetModelsForMake/{urllib.parse.quote(make)}?format=json"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    j = resp.json()
    results = j.get('Results', [])
    seen = set()
    models = []
    for r in results:
        name = r.get('Model_Name') or r.get('Model') or ''
        if not name or name in seen:
            continue
        seen.add(name)
        models.append(name)
    return models

def main():
    if not os.path.exists(DATA_PATH):
        print('data/models.json not found')
        return

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        old_data = json.load(f)

    # Backup current state
    with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        json.dump(old_data, f, indent=2, ensure_ascii=False)
    print('Backup written to', BACKUP_PATH)

    # Get all makes from old data
    makes = list(old_data.keys())
    print(f'Fetching real models for {len(makes)} makes from VPIC...')
    
    new_data = {}
    fetched_count = 0
    skipped_count = 0

    for i, make in enumerate(makes, 1):
        print(f'[{i}/{len(makes)}] {make}...', end=' ', flush=True)
        try:
            models_list = get_models_for_make(make)
        except Exception as e:
            print(f'ERROR: {e}')
            # Keep old data as fallback
            new_data[make] = old_data.get(make, [{"name": "Standard Model", "type": "Unknown", "subtiers": ["Standard"]}])
            skipped_count += 1
            time.sleep(0.3)
            continue

        if not models_list:
            print('no models')
            # Keep old data as fallback
            new_data[make] = old_data.get(make, [{"name": "Standard Model", "type": "Unknown", "subtiers": ["Standard"]}])
            skipped_count += 1
            time.sleep(0.3)
            continue

        # Build model entries (limit to 200 per make)
        new_models = []
        for model_name in models_list[:200]:
            vtype = infer_vehicle_type_from_model_name(model_name)
            subtiers = infer_subtiers(vtype, model_name)
            new_models.append({
                'name': model_name,
                'type': vtype,
                'subtiers': subtiers
            })
            time.sleep(0.02)

        new_data[make] = new_models
        fetched_count += 1
        print(f'{len(new_models)} models')
        time.sleep(0.25)

    # Write updated data
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)

    print(f'\n✓ Updated data/models.json')
    print(f'  Fetched real models for {fetched_count} makes')
    print(f'  Kept/fallback for {skipped_count} makes')
    print(f'  Total makes: {len(new_data)}')

if __name__ == '__main__':
    main()
