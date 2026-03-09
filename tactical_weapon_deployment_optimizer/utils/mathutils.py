# utils/mathutils.py - UPDATED WITH REALISTIC CONSTRAINTS

from utils.geoutils import haversine_distance

def calculate_total_damage(candidate_lat, candidate_lon, enemy_positions, weapon, friendly_positions=None, min_safe_distance=2.0):
    """
    Calculate total damage score considering friendly positions and REALISTIC constraints.
    """
    total_damage = 0.0
    
    # 1. Check if too close to friendly positions (safety first)
    if friendly_positions:
        for friendly_id, friendly_lat, friendly_lon in friendly_positions:
            safe_distance = haversine_distance(candidate_lat, candidate_lon, friendly_lat, friendly_lon)
            if safe_distance < min_safe_distance:
                return -1  # Invalid position - too close to friendlies
    
    engaged_targets = 0
    for enemy_id, enemy_lat, enemy_lon, enemy_type in enemy_positions:
        distance_km = haversine_distance(candidate_lat, candidate_lon, enemy_lat, enemy_lon)
        
        # Check if target is within weapon's operational range
        if distance_km < weapon["min_range_km"] or distance_km > weapon["max_range_km"]:
            continue  # Target out of range
            
        damage = weapon["lethality_function"](distance_km, weapon)
        total_damage += damage
        engaged_targets += 1
    
    # Return normalized damage score
    if engaged_targets == 0:
        return 0.0
    
    return total_damage

def is_placement_realistic(weapon, candidate_position, current_position, enemy_positions):
    """
    Check if a placement position is realistic considering weapon mobility.
    """
    distance_from_current = haversine_distance(current_position[0], current_position[1],
                                             candidate_position[0], candidate_position[1])
    
    # Check mobility constraint
    max_deployment = weapon.get("max_placement_distance_km", 5.0)
    if distance_from_current > max_deployment:
        return False, f"Position {distance_from_current:.1f}km away exceeds {max_deployment}km mobility limit"
    
    # Check if weapon can actually engage from this position
    can_engage = False
    for enemy_id, enemy_lat, enemy_lon, enemy_type in enemy_positions:
        engagement_distance = haversine_distance(candidate_position[0], candidate_position[1],
                                               enemy_lat, enemy_lon)
        if weapon["min_range_km"] <= engagement_distance <= weapon["max_range_km"]:
            can_engage = True
            break
    
    if not can_engage:
        return False, "Cannot engage any targets from this position"
    
    return True, "Realistic placement"