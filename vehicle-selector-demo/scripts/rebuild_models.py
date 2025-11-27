#!/usr/bin/env python3
"""
Rebuild models.json with comprehensive real vehicle data for all makes.
This completely replaces the old file with accurate, curated model data.
"""

import json
import os

# Comprehensive vehicle models database (all 101+ makes)
complete_data = {
    "Acura": [
        {"name": "MDX", "type": "SUV", "subtiers": ["Standard"]},
        {"name": "RDX", "type": "SUV", "subtiers": ["Standard"]},
        {"name": "TLX", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "ILX", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Alfa Romeo": [
        {"name": "Giulia", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Stelvio", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Aston Martin": [
        {"name": "DB11", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Vantage", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "DBX", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Audi": [
        {"name": "A3", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "A4", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "A6", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "A8", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Q3", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Q5", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "Q7", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "TT", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "R8", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Bentley": [
        {"name": "Continental GT", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Flying Spur", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Bentayga", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "BMW": [
        {"name": "328i", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "330i", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "X1", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "X3", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "X5", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "X7", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Z4", "type": "Roadster", "subtiers": ["2-Door"]},
        {"name": "M440i", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Bugatti": [
        {"name": "Chiron", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Veyron", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Buick": [
        {"name": "LaCrosse", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Regal", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Encore", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Enclave", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Cadillac": [
        {"name": "Escalade", "type": "SUV", "subtiers": ["Standard", "ESV"]},
        {"name": "Escalade IQ", "type": "SUV", "subtiers": ["Standard", "ESV"]},
        {"name": "CT4", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "CT5", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "CT6", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "XT4", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "XT5", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "XT6", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Lyric", "type": "SUV", "subtiers": ["Mid-Size"]}
    ],
    "Chevrolet": [
        {"name": "Malibu", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Cruze", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Spark", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "Camaro", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Corvette", "type": "Coupe", "subtiers": ["2-Door", "Targa"]},
        {"name": "Silverado", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "Colorado", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "Equinox", "type": "SUV", "subtiers": ["Standard"]},
        {"name": "Blazer", "type": "SUV", "subtiers": ["Standard"]},
        {"name": "Tahoe", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Suburban", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Traverse", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Trax", "type": "SUV", "subtiers": ["Compact"]}
    ],
    "Chrysler": [
        {"name": "300", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Pacifica", "type": "Minivan", "subtiers": ["Standard", "Extended"]}
    ],
    "Citroen": [
        {"name": "C3", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "C5", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Dacia": [
        {"name": "Duster", "type": "SUV", "subtiers": ["Standard"]},
        {"name": "Sandero", "type": "Hatchback", "subtiers": ["5-Door"]}
    ],
    "Daewoo": [
        {"name": "Matiz", "type": "Hatchback", "subtiers": ["5-Door"]}
    ],
    "Daihatsu": [
        {"name": "Terios", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Dodge": [
        {"name": "Charger", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Challenger", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Durango", "type": "SUV", "subtiers": ["2-Row", "3-Row"]},
        {"name": "Journey", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Donkervoort": [
        {"name": "D8", "type": "Roadster", "subtiers": ["2-Door"]}
    ],
    "Ferrari": [
        {"name": "F8 Tributo", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "296 GTB", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "SF90 Stradale", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Portofino", "type": "Convertible", "subtiers": ["2-Door"]},
        {"name": "Roma", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Daytona SP3", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Fiat": [
        {"name": "500", "type": "Hatchback", "subtiers": ["3-Door", "5-Door"]},
        {"name": "500X", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "500L", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "Panda", "type": "Hatchback", "subtiers": ["5-Door"]}
    ],
    "Fisker": [
        {"name": "Ocean", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "Karma", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Ford": [
        {"name": "Mustang", "type": "Coupe", "subtiers": ["2-Door", "4-Door"]},
        {"name": "F-150", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "Escape", "type": "SUV", "subtiers": ["Standard", "Hybrid"]},
        {"name": "Explorer", "type": "SUV", "subtiers": ["2-Row", "3-Row"]},
        {"name": "Focus", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Fusion", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Ranger", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "Edge", "type": "SUV", "subtiers": ["Standard"]},
        {"name": "Expedition", "type": "SUV", "subtiers": ["2-Row", "3-Row"]},
        {"name": "Bronco", "type": "SUV", "subtiers": ["2-Door", "4-Door"]}
    ],
    "GMC": [
        {"name": "Sierra", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "Sierra Denali", "type": "Truck", "subtiers": ["Crew-Cab"]},
        {"name": "Yukon", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Terrain", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Acadia", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Canyon", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]}
    ],
    "Great Wall": [
        {"name": "Haval H6", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Hindustan": [
        {"name": "Ambassador", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Hummer": [
        {"name": "H1", "type": "SUV", "subtiers": ["Standard"]},
        {"name": "H2", "type": "SUV", "subtiers": ["Standard"]},
        {"name": "H3", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Hyundai": [
        {"name": "Elantra", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Sonata", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Tucson", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Santa Fe", "type": "SUV", "subtiers": ["2-Row", "3-Row"]},
        {"name": "Accent", "type": "Sedan", "subtiers": ["2-Door", "4-Door"]},
        {"name": "Prius", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Infiniti": [
        {"name": "Q50", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Q60", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "QX50", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "QX60", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "QX80", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Isuzu": [
        {"name": "D-Max", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "MU-X", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Jaguar": [
        {"name": "XE", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "XF", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "XJ", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "F-PACE", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "F-TYPE", "type": "Roadster", "subtiers": ["2-Door"]}
    ],
    "Jeep": [
        {"name": "Wrangler", "type": "SUV", "subtiers": ["2-Door", "4-Door"]},
        {"name": "Cherokee", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Grand Cherokee", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "Compass", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Renegade", "type": "SUV", "subtiers": ["Subcompact"]},
        {"name": "Gladiator", "type": "Truck", "subtiers": ["Crew-Cab"]}
    ],
    "Jensen": [
        {"name": "Interceptor", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Kia": [
        {"name": "Optima", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Forte", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Rio", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Sportage", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Sorento", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Niro", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Telluride", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Koenigsegg": [
        {"name": "Jesko", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Gemera", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Lamborghini": [
        {"name": "Huracán", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Revuelto", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Urus", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Lancia": [
        {"name": "Ypsilon", "type": "Hatchback", "subtiers": ["3-Door", "5-Door"]}
    ],
    "Land Rover": [
        {"name": "Discovery", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Discovery Sport", "type": "SUV", "subtiers": ["2-Row"]},
        {"name": "Range Rover", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Range Rover Sport", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "Range Rover Evoque", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Defender", "type": "SUV", "subtiers": ["2-Door", "4-Door"]}
    ],
    "Lada": [
        {"name": "Vesta", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Granta", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Lexus": [
        {"name": "IS", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "ES", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "GS", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "LS", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "RX", "type": "SUV", "subtiers": ["Compact", "Hybrid"]},
        {"name": "NX", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "GX", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "LX", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "LX600", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Ligier": [
        {"name": "JS2", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Lotus": [
        {"name": "Exige", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Emira", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Eletre", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Maserati": [
        {"name": "Ghibli", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Quattroporte", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "MC20", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Levante", "type": "SUV", "subtiers": ["Mid-Size"]}
    ],
    "Maybach": [
        {"name": "S-Class", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "GLS", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Mazda": [
        {"name": "Mazda3", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Mazda6", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "CX-30", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "CX-5", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "CX-9", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "MX-5", "type": "Roadster", "subtiers": ["2-Door"]},
        {"name": "RX-8", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "McLaren": [
        {"name": "570S", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "720S", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "GT", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Mercedes-Benz": [
        {"name": "A-Class", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "C-Class", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "E-Class", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "S-Class", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "GLA", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "GLC", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "GLE", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "GLS", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "AMG GT", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "SL", "type": "Roadster", "subtiers": ["2-Door"]},
        {"name": "Sprinter", "type": "Van", "subtiers": ["Standard", "Extended"]}
    ],
    "Mercury": [
        {"name": "Grand Marquis", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "MG": [
        {"name": "MG5", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "ZS", "type": "SUV", "subtiers": ["Compact"]}
    ],
    "Microcar": [
        {"name": "MC1", "type": "Hatchback", "subtiers": ["3-Door"]}
    ],
    "Mini": [
        {"name": "Cooper", "type": "Hatchback", "subtiers": ["3-Door", "5-Door"]},
        {"name": "Countryman", "type": "SUV", "subtiers": ["Compact"]}
    ],
    "Mitsubishi": [
        {"name": "Lancer", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Outlander", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Eclipse Cross", "type": "SUV", "subtiers": ["Compact"]}
    ],
    "Morgan": [
        {"name": "Plus Four", "type": "Roadster", "subtiers": ["2-Door"]}
    ],
    "Morris": [
        {"name": "Minor", "type": "Hatchback", "subtiers": ["4-Door"]}
    ],
    "Nissan": [
        {"name": "Altima", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Maxima", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Sentra", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Rogue", "type": "SUV", "subtiers": ["Standard", "Hybrid"]},
        {"name": "Pathfinder", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Murano", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "Frontier", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "Titan", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "GT-R", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Noble": [
        {"name": "M600", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "NSU": [
        {"name": "Ro 80", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Pagani": [
        {"name": "Huayra", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Panhard": [
        {"name": "PL17", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Panoz": [
        {"name": "Esperante", "type": "Roadster", "subtiers": ["2-Door"]}
    ],
    "Perodua": [
        {"name": "Myvi", "type": "Hatchback", "subtiers": ["5-Door"]}
    ],
    "Peugeot": [
        {"name": "308", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "3008", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "5008", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Pontiac": [
        {"name": "G6", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Porsche": [
        {"name": "911", "type": "Coupe", "subtiers": ["2-Door", "Targa"]},
        {"name": "Boxster", "type": "Roadster", "subtiers": ["2-Door"]},
        {"name": "Cayman", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Cayenne", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "Macan", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Panamera", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Taycan", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Proton": [
        {"name": "Saga", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Ram": [
        {"name": "1500", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "2500", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "3500", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "ProMaster", "type": "Van", "subtiers": ["Standard", "Extended"]}
    ],
    "Renault": [
        {"name": "Clio", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "Megane", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "Duster", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Renault Samsung": [
        {"name": "SM7", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Reva": [
        {"name": "G-Wiz", "type": "Hatchback", "subtiers": ["3-Door"]}
    ],
    "Rolls-Royce": [
        {"name": "Phantom", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Ghost", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Wraith", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Dawn", "type": "Roadster", "subtiers": ["2-Door"]},
        {"name": "Cullinan", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Rover": [
        {"name": "Mini", "type": "Hatchback", "subtiers": ["4-Door"]}
    ],
    "Saab": [
        {"name": "9-3", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "9-5", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Samsung": [
        {"name": "SM5", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Scion": [
        {"name": "FR-S", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Seat": [
        {"name": "Ibiza", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "Leon", "type": "Hatchback", "subtiers": ["5-Door"]}
    ],
    "Shuanghuan": [
        {"name": "CEO", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Skoda": [
        {"name": "Fabia", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "Superb", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Smart": [
        {"name": "Fortwo", "type": "Hatchback", "subtiers": ["2-Door", "3-Door"]},
        {"name": "Forfour", "type": "Hatchback", "subtiers": ["5-Door"]}
    ],
    "Spyker": [
        {"name": "C8", "type": "Roadster", "subtiers": ["2-Door"]}
    ],
    "SsangYong": [
        {"name": "Tivoli", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Rexton", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Studebaker": [
        {"name": "Champion", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Subaru": [
        {"name": "Legacy", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Outback", "type": "Wagon", "subtiers": ["4-Door"]},
        {"name": "Impreza", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "WRX", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Forester", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Crosstrek", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Ascent", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Suzuki": [
        {"name": "Swift", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "Vitara", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "S-Cross", "type": "SUV", "subtiers": ["Compact"]}
    ],
    "Tata": [
        {"name": "Tiago", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "Nexon", "type": "SUV", "subtiers": ["Compact"]}
    ],
    "Tesla": [
        {"name": "Model 3", "type": "Sedan", "subtiers": ["4-Door", "Dual-Motor"]},
        {"name": "Model S", "type": "Sedan", "subtiers": ["4-Door", "Plaid"]},
        {"name": "Model X", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Model Y", "type": "SUV", "subtiers": ["Compact", "Dual-Motor"]},
        {"name": "Roadster", "type": "Roadster", "subtiers": ["2-Door"]}
    ],
    "Toyota": [
        {"name": "Camry", "type": "Sedan", "subtiers": ["2-Door", "4-Door"]},
        {"name": "Corolla", "type": "Sedan", "subtiers": ["2-Door", "4-Door"]},
        {"name": "Supra", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "RAV4", "type": "SUV", "subtiers": ["Standard", "Hybrid"]},
        {"name": "Prius", "type": "Sedan", "subtiers": ["Standard", "Plus", "Prime"]},
        {"name": "Highlander", "type": "SUV", "subtiers": ["2-Row", "3-Row"]},
        {"name": "4Runner", "type": "SUV", "subtiers": ["4-Door"]},
        {"name": "Tundra", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "Tacoma", "type": "Truck", "subtiers": ["Single-Cab", "Double-Cab", "Crew-Cab"]},
        {"name": "Sequoia", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "Sienna", "type": "Minivan", "subtiers": ["Standard"]}
    ],
    "Trabant": [
        {"name": "Trabant 601", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Triumph": [
        {"name": "TR6", "type": "Roadster", "subtiers": ["2-Door"]}
    ],
    "TVR": [
        {"name": "Chimaera", "type": "Roadster", "subtiers": ["2-Door"]}
    ],
    "Ultima": [
        {"name": "GTR", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Umm": [
        {"name": "Al Zawraa", "type": "SUV", "subtiers": ["Standard"]}
    ],
    "Vauxhall": [
        {"name": "Corsa", "type": "Hatchback", "subtiers": ["5-Door"]},
        {"name": "Astra", "type": "Hatchback", "subtiers": ["5-Door"]}
    ],
    "Vector": [
        {"name": "W8", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Venturi": [
        {"name": "Atlantique", "type": "Coupe", "subtiers": ["2-Door"]}
    ],
    "Vignale": [
        {"name": "Maserati", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Volkswagen": [
        {"name": "Golf", "type": "Hatchback", "subtiers": ["3-Door", "5-Door"]},
        {"name": "Jetta", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Passat", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "Beetle", "type": "Coupe", "subtiers": ["2-Door"]},
        {"name": "Tiguan", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "Atlas", "type": "SUV", "subtiers": ["3-Row"]},
        {"name": "ID.4", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "ID. Buzz", "type": "Van", "subtiers": ["Standard"]}
    ],
    "Volvo": [
        {"name": "S60", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "S90", "type": "Sedan", "subtiers": ["4-Door"]},
        {"name": "XC40", "type": "SUV", "subtiers": ["Compact"]},
        {"name": "XC60", "type": "SUV", "subtiers": ["Mid-Size"]},
        {"name": "XC90", "type": "SUV", "subtiers": ["3-Row"]}
    ],
    "Wartburg": [
        {"name": "Knight", "type": "Sedan", "subtiers": ["4-Door"]}
    ],
    "Westfield": [
        {"name": "SEiC", "type": "Roadster", "subtiers": ["2-Door"]}
    ],
    "Wiesmann": [
        {"name": "MF5", "type": "Roadster", "subtiers": ["2-Door"]}
    ],
    "Willys": [
        {"name": "Jeep", "type": "SUV", "subtiers": ["2-Door", "4-Door"]}
    ],
    "Zastava": [
        {"name": "Yugo", "type": "Hatchback", "subtiers": ["3-Door", "5-Door"]}
    ],
    "Zenvo": [
        {"name": "ST1", "type": "Coupe", "subtiers": ["2-Door"]}
    ]
}

# Get output path
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, '..', 'data', 'models.json')
output_path = os.path.abspath(output_path)

# Ensure directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write JSON file
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(complete_data, f, indent=2, ensure_ascii=False)

print(f"✓ models.json rebuilt successfully!")
print(f"  Location: {output_path}")
print(f"  Total makes: {len(complete_data)}")
total_models = sum(len(models) for models in complete_data.values())
print(f"  Total models: {total_models}")
