# weapons/weapons_data.py - COMPLETE WITH ALL WEAPONS

WEAPONS = {
    # 1. Main Battle Tanks (High Mobility - can move 50km+)
    "T-90 Bhishma": {
        "type": "Main Battle Tank",
        "max_range_km": 5.0,
        "min_range_km": 0.5,
        "mobility": "high",
        "max_placement_distance_km": 50.0,
        "deployment_time_min": 5,
        "preferred_targets": ["Main Battle Tank", "Infantry Fighting Vehicle", "Bunkers", "Armored Vehicles"],
        "unsuitable_targets": ["Aircraft", "Artillery", "Area Targets", "Personnel"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 3.0 else (0.7 if distance_km <= 4.0 else 0.4)
    },
    "T-72 Ajeya": {
        "type": "Main Battle Tank", 
        "max_range_km": 3.0,
        "min_range_km": 0.5,
        "mobility": "high",
        "max_placement_distance_km": 50.0,
        "deployment_time_min": 5,
        "preferred_targets": ["Main Battle Tank", "Infantry Fighting Vehicle", "Light Armor"],
        "unsuitable_targets": ["Aircraft", "Artillery", "Area Targets", "Personnel"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 2.0 else (0.6 if distance_km <= 2.5 else 0.3)
    },
    "Arjun MBT": {
        "type": "Main Battle Tank",
        "max_range_km": 4.0,
        "min_range_km": 0.5,
        "mobility": "high",
        "max_placement_distance_km": 50.0,
        "deployment_time_min": 5,
        "preferred_targets": ["Main Battle Tank", "Infantry Fighting Vehicle", "Fortifications"],
        "unsuitable_targets": ["Aircraft", "Artillery", "Area Targets", "Personnel"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 3.0 else (0.8 if distance_km <= 3.5 else 0.5)
    },

    # 2. Infantry Fighting Vehicles (Medium Mobility - can move 20km)
    "BMP-1": {
        "type": "Infantry Fighting Vehicle",
        "max_range_km": 3.0,
        "min_range_km": 0.1,
        "mobility": "medium",
        "max_placement_distance_km": 20.0,
        "deployment_time_min": 3,
        "preferred_targets": ["Infantry", "Light Vehicles", "Bunkers", "Personnel"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Artillery"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 1.0 else (0.6 if distance_km <= 2.0 else 0.3)
    },
    "BMP-2 Sarath": {
        "type": "Infantry Fighting Vehicle",
        "max_range_km": 4.0,
        "min_range_km": 0.1,
        "mobility": "medium",
        "max_placement_distance_km": 20.0,
        "deployment_time_min": 3,
        "preferred_targets": ["Infantry", "Light Armor", "Helicopters", "Personnel"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Artillery"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 1.5 else (0.8 if distance_km <= 3.0 else 0.4)
    },
    "TATA Kestrel APC/IFV": {
        "type": "Infantry Fighting Vehicle",
        "max_range_km": 4.0,
        "min_range_km": 0.1,
        "mobility": "medium",
        "max_placement_distance_km": 20.0,
        "deployment_time_min": 2,
        "preferred_targets": ["Infantry", "Light Vehicles", "Personnel"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Artillery"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 2.0 else (0.7 if distance_km <= 3.0 else 0.4)
    },

    # 3. Artillery (Medium Mobility - can move 30km, but slower)
    "Dhanush Howitzer": {
        "type": "Artillery",
        "max_range_km": 38.0,
        "min_range_km": 3.0,
        "mobility": "medium",
        "max_placement_distance_km": 30.0,
        "deployment_time_min": 15,
        "preferred_targets": ["Artillery", "Command Centers", "Infantry Concentrations", "Supply Depots", "Structures"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Personnel", "Moving Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km >= 5.0 and distance_km <= 30.0 else (0.8 if distance_km <= 35.0 else 0.5)
    },
    "M777 Howitzer": {
        "type": "Artillery", 
        "max_range_km": 40.0,
        "min_range_km": 4.0,
        "mobility": "medium",
        "max_placement_distance_km": 30.0,
        "deployment_time_min": 10,
        "preferred_targets": ["Artillery", "Bunkers", "Infantry", "Structures", "Command Centers"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Personnel", "Moving Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km >= 5.0 and distance_km <= 35.0 else (0.7 if distance_km <= 38.0 else 0.4)
    },
    "Bofors FH77 Howitzer": {
        "type": "Artillery",
        "max_range_km": 30.0,
        "min_range_km": 3.0,
        "mobility": "medium",
        "max_placement_distance_km": 25.0,
        "deployment_time_min": 12,
        "preferred_targets": ["Infantry", "Light Vehicles", "Artillery", "Structures"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Moving Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km >= 4.0 and distance_km <= 25.0 else (0.6 if distance_km <= 28.0 else 0.3)
    },
    "Pinaka MBRL": {
        "type": "Multiple Rocket Launcher",
        "max_range_km": 40.0,
        "min_range_km": 10.0,
        "mobility": "medium",
        "max_placement_distance_km": 25.0,
        "deployment_time_min": 8,
        "preferred_targets": ["Area Targets", "Infantry Concentrations", "Supply Depots", "Vehicle Parks"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Point Targets"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km >= 15.0 and distance_km <= 35.0 else (0.5 if distance_km <= 38.0 else 0.2)
    },

    # 4. Army Air Defense (AAD) - Variable Mobility
    "Akash SAM": {
        "type": "Surface-to-Air Missile",
        "max_range_km": 25.0,
        "min_range_km": 1.0,
        "mobility": "medium",
        "max_placement_distance_km": 25.0,
        "deployment_time_min": 10,
        "preferred_targets": ["Aircraft", "Helicopters", "Drones", "Cruise Missiles"],
        "unsuitable_targets": ["Main Battle Tank", "Infantry", "Bunkers", "Ground Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km >= 3.0 and distance_km <= 20.0 else (0.4 if distance_km <= 23.0 else 0.1)
    },
    "Spyder SAM": {
        "type": "Surface-to-Air Missile",
        "max_range_km": 15.0,
        "min_range_km": 1.0,
        "mobility": "medium",
        "max_placement_distance_km": 20.0,
        "deployment_time_min": 8,
        "preferred_targets": ["Aircraft", "Helicopters", "Drones"],
        "unsuitable_targets": ["Main Battle Tank", "Infantry", "Ground Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km >= 2.0 and distance_km <= 12.0 else (0.5 if distance_km <= 14.0 else 0.2)
    },
    "L70 AA Gun": {
        "type": "Anti-Aircraft Gun",
        "max_range_km": 4.0,
        "min_range_km": 0.5,
        "mobility": "low",
        "max_placement_distance_km": 10.0,
        "deployment_time_min": 5,
        "preferred_targets": ["Low-flying Aircraft", "Helicopters", "Drones"],
        "unsuitable_targets": ["Main Battle Tank", "Infantry", "Ground Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 2.0 else (0.6 if distance_km <= 3.0 else 0.3)
    },
    "ZU-23-2 AA Gun": {
        "type": "Anti-Aircraft Gun", 
        "max_range_km": 2.5,
        "min_range_km": 0.3,
        "mobility": "low",
        "max_placement_distance_km": 8.0,
        "deployment_time_min": 3,
        "preferred_targets": ["Low-flying Aircraft", "Helicopters", "Light Vehicles"],
        "unsuitable_targets": ["Main Battle Tank", "Infantry", "Armored Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 1.5 else (0.5 if distance_km <= 2.0 else 0.2)
    },

    # 5. Infantry and Support Weapons (Low Mobility - max 5km placement)
    "INSAS Rifle": {
        "type": "Infantry Rifle",
        "max_range_km": 0.45,
        "min_range_km": 0.05,
        "mobility": "low",
        "max_placement_distance_km": 5.0,
        "deployment_time_min": 1,
        "preferred_targets": ["Personnel", "Light Targets"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Artillery", "Armored Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 0.2 else (0.4 if distance_km <= 0.35 else 0.1)
    },
    "AK-203 Rifle": {
        "type": "Infantry Rifle",
        "max_range_km": 0.6,
        "min_range_km": 0.05,
        "mobility": "low",
        "max_placement_distance_km": 5.0,
        "deployment_time_min": 1,
        "preferred_targets": ["Personnel", "Light Targets"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Artillery", "Armored Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 0.3 else (0.5 if distance_km <= 0.5 else 0.2)
    },
    "Negev LMG": {
        "type": "Light Machine Gun",
        "max_range_km": 1.0,
        "min_range_km": 0.1,
        "mobility": "low",
        "max_placement_distance_km": 5.0,
        "deployment_time_min": 2,
        "preferred_targets": ["Personnel", "Light Vehicles", "Suppression"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Artillery", "Armored Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 0.6 else (0.7 if distance_km <= 0.8 else 0.4)
    },
    "Dragunov SVD": {
        "type": "Sniper Rifle",
        "max_range_km": 1.2,
        "min_range_km": 0.1,
        "mobility": "low",
        "max_placement_distance_km": 5.0,
        "deployment_time_min": 2,
        "preferred_targets": ["Personnel", "Officers", "Light Vehicles"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Artillery", "Armored Vehicles"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 0.8 else (0.8 if distance_km <= 1.0 else 0.5)
    },

    # 6. Engineer and Support Weapons
    "Bangalore Torpedo": {
        "type": "Demolition",
        "max_range_km": 0.0015,  # 1.5 meters
        "min_range_km": 0.0,
        "mobility": "low",
        "max_placement_distance_km": 2.0,
        "deployment_time_min": 5,
        "preferred_targets": ["Obstacles", "Wire", "Mines"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Personnel", "Structures"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 0.001 else 0.0
    },
    "Bridge-laying Tank": {
        "type": "Engineering Vehicle",
        "max_range_km": 0.022,  # 22 meter span
        "min_range_km": 0.0,
        "mobility": "medium",
        "max_placement_distance_km": 15.0,
        "deployment_time_min": 10,
        "preferred_targets": ["Obstacles", "Gaps"],
        "unsuitable_targets": ["Main Battle Tank", "Aircraft", "Personnel"],
        "lethality_function": lambda distance_km, weapon: 1.0 if distance_km <= 0.02 else 0.0
    }
}