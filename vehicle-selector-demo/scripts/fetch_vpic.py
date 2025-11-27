"""Fetch models for makes from NHTSA VPIC and replace placeholders in data/models.json.

Usage:
  python scripts/fetch_vpic.py

Notes:
- This script updates `data/models.json` in place (creates a backup `models.json.bak`).
- It attempts to infer a vehicle "type" via VPIC's GetVehicleTypesForMakeModel endpoint; if none, it uses heuristics.
- It keeps requests conservative with a short sleep to avoid rate limits.
"""
import requests
import json
import time
import os
import urllib.parse

BASE = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE, 'data', 'models.json')
BACKUP_PATH = DATA_PATH + '.bak'

VPIC_BASE = 'https://vpic.nhtsa.dot.gov/api/vehicles'

# Simple heuristics to map types -> subtiers
def infer_subtiers(vtype, model_name):
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
    # fallback
    return ["Standard"]


def get_models_for_make(make):
    url = f"{VPIC_BASE}/GetModelsForMake/{urllib.parse.quote(make)}?format=json"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    j = resp.json()
    results = j.get('Results', [])
    # Extract unique model names preserving order
    seen = set()
    models = []
    for r in results:
        name = r.get('Model_Name') or r.get('Model') or ''
        if not name: continue
        if name not in seen:
            seen.add(name)
            models.append(name)
    return models


def infer_vehicle_type_from_model_name(model_name):
    """Infer vehicle type from model name patterns only (no API calls)."""
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
    # fallback
    return 'Unknown'


def main():
    if not os.path.exists(DATA_PATH):
        print('data/models.json not found at', DATA_PATH)
        return

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Backup
    with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print('Backup written to', BACKUP_PATH)

    updated = False
    makes = list(data.keys())
    print('Found', len(makes), 'makes in models.json')

    for i, make in enumerate(makes, 1):
        models = data.get(make) or []
        # Determine if it's placeholder: has exactly 1 model AND (name is "Standard Model" OR type is "Unknown")
        is_placeholder = False
        if len(models) == 1:
            model_name = models[0].get('name', '').lower().strip()
            model_type = models[0].get('type', '').lower().strip()
            # Single-entry placeholders: name "standard model" or type "unknown"
            if model_name == 'standard model' or model_type == 'unknown':
                is_placeholder = True

        if not is_placeholder:
            continue

        print(f'[{i}/{len(makes)}] Fetching models for make:', make)
        try:
            fetched = get_models_for_make(make)
        except Exception as e:
            print('  Failed to fetch models for', make, ' — ', e)
            continue

        if not fetched:
            print('  No models returned for', make)
            continue

        # Limit models per make to a reasonable number to avoid extreme size (e.g., 200)
        limit = 200
        new_models = []
        for model_name in fetched[:limit]:
            vtype = infer_vehicle_type_from_model_name(model_name)
            subtiers = infer_subtiers(vtype, model_name)
            new_models.append({
                'name': model_name,
                'type': vtype,
                'subtiers': subtiers
            })
            time.sleep(0.05)  # small delay

        if new_models:
            data[make] = new_models
            updated = True
            print('  Replaced placeholder with', len(new_models), 'models for', make)
        # polite pause between makes
        time.sleep(0.35)

    if updated:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print('Updated data/models.json')
    else:
        print('No updates made (no placeholders found or fetch failed)')


if __name__ == '__main__':
    main()
