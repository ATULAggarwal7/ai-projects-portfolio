# utils/geoutils.py - UPDATED WITH SMART POSITIONING

import math
import numpy as np

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance (in kilometers) between two points
    on the Earth's surface given their latitude and longitude in decimal degrees.
    """
    R = 6371  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance_km = R * c
    return distance_km

def generate_grid(center_lat, center_lon, radius_km, resolution_km):
    """
    Generates a flat grid of candidate points around a center location.
    Returns a list of (lat, lon) tuples.
    WARNING: This is a simple approximation. For large areas, use a proper projection.
    """
    # Approximate km per degree at equator (~111km). Adjust for latitude.
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * math.cos(math.radians(center_lat))

    grid_points = []
    steps = int(radius_km / resolution_km)
    # Create offsets from the center
    for i in range(-steps, steps + 1):
        for j in range(-steps, steps + 1):
            # Calculate new point based on offsets
            lat_offset = i * resolution_km / km_per_deg_lat
            lon_offset = j * resolution_km / km_per_deg_lon
            new_lat = center_lat + lat_offset
            new_lon = center_lon + lon_offset
            grid_points.append((new_lat, new_lon))
    return grid_points

def calculate_compass_direction(lat1, lon1, lat2, lon2):
    """
    Calculate compass direction from point 1 to point 2
    Returns: (bearing_degrees, compass_direction)
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Calculate bearing
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing_rad = math.atan2(x, y)
    bearing_deg = (math.degrees(bearing_rad) + 360) % 360
    
    # Convert to compass direction
    compass_directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
                         'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    compass_index = int((bearing_deg + 11.25) / 22.5) % 16
    compass_dir = compass_directions[compass_index]
    
    return bearing_deg, compass_dir

def calculate_movement_instructions(current_pos, target_pos):
    """
    Calculate grid movement instructions: direction and distance
    Returns: (direction_degrees, direction_compass, distance_km, grid_reference)
    """
    # Calculate bearing/direction
    lat1, lon1 = current_pos
    lat2, lon2 = target_pos
    
    bearing_deg, compass_dir = calculate_compass_direction(lat1, lon1, lat2, lon2)
    
    # Calculate distance
    distance_km = haversine_distance(lat1, lon1, lat2, lon2)
    
    # Create grid reference (simplified MGRS-style)
    lat_diff = target_pos[0] - current_pos[0]
    lon_diff = target_pos[1] - current_pos[1]
    
    if lat_diff >= 0:
        ns_dir = "N"
        ns_dist = lat_diff * 111  # approx km per degree latitude
    else:
        ns_dir = "S" 
        ns_dist = abs(lat_diff) * 111
        
    if lon_diff >= 0:
        ew_dir = "E"
        ew_dist = lon_diff * 111 * math.cos(math.radians(current_pos[0]))  # adjust for latitude
    else:
        ew_dir = "W"
        ew_dist = abs(lon_diff) * 111 * math.cos(math.radians(current_pos[0]))
    
    grid_reference = f"{ns_dir}{ns_dist:.1f}km {ew_dir}{ew_dist:.1f}km"
    
    return bearing_deg, compass_dir, distance_km, grid_reference

def calculate_position_from_bearing(lat, lon, bearing_deg, distance_km):
    """Calculate new position given bearing and distance"""
    R = 6371  # Earth radius in km
    
    # Convert to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    bearing_rad = math.radians(bearing_deg)
    
    # Calculate new position
    new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(distance_km/R) + 
                           math.cos(lat_rad) * math.sin(distance_km/R) * math.cos(bearing_rad))
    
    new_lon_rad = lon_rad + math.atan2(math.sin(bearing_rad) * math.sin(distance_km/R) * math.cos(lat_rad),
                                      math.cos(distance_km/R) - math.sin(lat_rad) * math.sin(new_lat_rad))
    
    return (math.degrees(new_lat_rad), math.degrees(new_lon_rad))

def is_forward_position(candidate_pos, friendly_pos, enemy_positions):
    """Check if position is forward (closer to ANY enemy)"""
    if not enemy_positions:
        return False
        
    current_min_dist = min([
        haversine_distance(friendly_pos[0], friendly_pos[1], e_lat, e_lon)
        for _, e_lat, e_lon, _ in enemy_positions
    ])
    
    candidate_min_dist = min([
        haversine_distance(candidate_pos[0], candidate_pos[1], e_lat, e_lon)
        for _, e_lat, e_lon, _ in enemy_positions
    ])
    
    return candidate_min_dist < current_min_dist

def generate_smart_forward_positions(friendly_pos, enemy_positions, weapon_data, num_positions=50):
    """
    Generate SMART forward positions considering:
    - Flanking maneuvers
    - Cover approaches  
    - Multiple axis of advance
    - Terrain advantages
    """
    smart_positions = []
    
    if not enemy_positions:
        return smart_positions
    
    # Get enemy cluster info
    enemy_lats = [lat for _, lat, lon, _ in enemy_positions]
    enemy_lons = [lon for _, lat, lon, _ in enemy_positions]
    enemy_center = (sum(enemy_lats)/len(enemy_lats), sum(enemy_lons)/len(enemy_lons))
    
    # Calculate direction to enemy
    bearing_to_enemy, compass_dir = calculate_compass_direction(
        friendly_pos[0], friendly_pos[1], enemy_center[0], enemy_center[1]
    )
    
    max_advance = weapon_data["max_placement_distance_km"]
    engagement_range = weapon_data["max_range_km"]
    
    # Generate multiple tactical approaches
    approaches = [
        ("Direct Assault", 0, "🎯"),           # Straight toward enemy
        ("Left Flank", -45, "🔄"),             # 45° left flank
        ("Right Flank", 45, "🔄"),              # 45° right flank  
        ("Wide Left Flank", -90, "🔄"),         # Wide left flank
        ("Wide Right Flank", 90, "🔄"),         # Wide right flank
        ("Cover Approach", -30, "🏞️"),         # Using cover
        ("High Ground", 30, "⛰️"),             # Seeking elevation
    ]
    
    for approach_name, angle_offset, emoji in approaches:
        # Calculate approach direction
        approach_bearing = (bearing_to_enemy + angle_offset) % 360
        
        # Generate positions along this approach at different distances
        for distance_ratio in [0.3, 0.5, 0.7, 0.9]:  # Different advancement levels
            advance_distance = max_advance * distance_ratio
            
            # Calculate position along approach vector
            pos = calculate_position_from_bearing(
                friendly_pos[0], friendly_pos[1], 
                approach_bearing, advance_distance
            )
            
            # Check if this is a forward position
            if is_forward_position(pos, friendly_pos, enemy_positions):
                # Calculate enemy distance
                enemy_distance = min([
                    haversine_distance(pos[0], pos[1], e_lat, e_lon)
                    for _, e_lat, e_lon, _ in enemy_positions
                ])
                
                smart_positions.append({
                    'position': pos,
                    'approach': approach_name,
                    'approach_emoji': emoji,
                    'bearing': approach_bearing,
                    'distance_advanced': advance_distance,
                    'enemy_distance': enemy_distance,
                    'tactical_score': evaluate_tactical_advantage(pos, enemy_positions, approach_name)
                })
    
    return smart_positions[:num_positions]

def evaluate_tactical_advantage(position, enemy_positions, approach_type):
    """Evaluate how tactically smart a position is"""
    score = 0.5  # Base score
    
    # Flanking bonuses
    if "Flank" in approach_type:
        score += 0.3  # Flanking is tactically superior
    if "Wide" in approach_type:
        score += 0.2  # Wide flanking is even better
    
    if "Cover" in approach_type or "High Ground" in approach_type:
        score += 0.2  # Terrain advantages
    
    # Distance optimization - prefer positions that don't over-advance
    if enemy_positions:
        closest_enemy = min([
            haversine_distance(position[0], position[1], e_lat, e_lon)
            for _, e_lat, e_lon, _ in enemy_positions
        ])
        
        # Prefer positions that maintain some distance (not too close)
        if closest_enemy > 2.0:  # At least 2km from enemy
            score += 0.2
        if closest_enemy > 5.0:  # Good standoff distance
            score += 0.1
    
    return min(score, 1.0)  # Cap at 1.0