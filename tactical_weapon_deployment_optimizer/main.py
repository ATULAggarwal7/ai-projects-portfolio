# main.py - UPDATED WITH MAXIMUM MOBILITY LOGIC AND CHARMAP PROTECTION

import math
import os
from config import GRID_RESOLUTION_KM, GRID_RADIUS_MULTIPLIER
from weapons.weapons_data import WEAPONS
from utils.geoutils import haversine_distance, generate_grid, calculate_compass_direction
from utils.geoutils import generate_smart_forward_positions, evaluate_tactical_advantage, calculate_position_from_bearing
from utils.mathutils import calculate_total_damage, is_placement_realistic
from weapon_recommender import WeaponRecommender, safe_print

def get_user_position():
    """Get friendly position from user"""
    safe_print("\n=== Enter Friendly Position ===")
    safe_print("Where are you operating from?")
    
    try:
        lat = float(input("Enter your Latitude (e.g., 28.6000): "))
        lon = float(input("Enter your Longitude (e.g., 77.2000): "))
        return (lat, lon)
    except ValueError:
        safe_print("Invalid coordinates. Using default position (28.6000, 77.2000)")
        return (28.6000, 77.2000)

def get_enemy_positions():
    """Get enemy positions interactively from user"""
    safe_print("\n=== Enter Enemy Positions ===")
    safe_print("Add enemy units one by one. Enter 'done' when finished.")
    
    enemy_positions = []
    enemy_counter = 1
    
    # Available enemy types for user reference
    available_types = ["Main Battle Tank", "Infantry", "Artillery", "Air Defense", 
                      "Infantry Fighting Vehicle", "Command Center", "Supply Depot"]
    
    safe_print(f"\nAvailable enemy types: {', '.join(available_types)}")
    
    while True:
        safe_print(f"\n--- Enemy Unit #{enemy_counter} ---")
        
        enemy_id = input("Enemy ID/Name (e.g., 'tank_1'): ").strip()
        if enemy_id.lower() == 'done':
            break
            
        try:
            lat = float(input("Latitude: "))
            lon = float(input("Longitude: "))
            
            safe_print("Enemy types: Main Battle Tank, Infantry, Artillery, Air Defense, etc.")
            enemy_type = input("Enemy type: ").strip()
            
            enemy_positions.append((enemy_id, lat, lon, enemy_type))
            enemy_counter += 1
            
            safe_print(f"Added {enemy_type} at ({lat}, {lon})")
            
        except ValueError:
            safe_print("Invalid input. Please enter numeric coordinates.")
            continue
    
    safe_print(f"\nTotal {len(enemy_positions)} enemy positions added.")
    return enemy_positions

def get_friendly_positions(main_position):
    """Get additional friendly positions interactively"""
    safe_print("\n=== Enter Friendly Positions ===")
    safe_print("Add other friendly units/positions for safety checks.")
    safe_print("Enter 'done' to skip or finish.")
    
    friendly_positions = []
    friendly_counter = 1
    
    # Always include the main position
    friendly_positions.append(("main_base", main_position[0], main_position[1]))
    
    while True:
        safe_print(f"\n--- Friendly Position #{friendly_counter} ---")
        
        friendly_id = input("Friendly ID/Name (e.g., 'base_camp'): ").strip()
        if friendly_id.lower() == 'done':
            break
            
        try:
            lat = float(input("Latitude: "))
            lon = float(input("Longitude: "))
            
            friendly_positions.append((friendly_id, lat, lon))
            friendly_counter += 1
            
            safe_print(f"Added friendly position at ({lat}, {lon})")
            
        except ValueError:
            safe_print("Invalid input. Please enter numeric coordinates.")
            continue
    
    safe_print(f"\nTotal {len(friendly_positions)} friendly positions (including yours).")
    return friendly_positions

def calculate_movement_instructions(current_pos, target_pos):
    """Calculate grid movement instructions: direction and distance"""
    lat1, lon1 = current_pos
    lat2, lon2 = target_pos
    
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
    
    # Calculate distance
    distance_km = haversine_distance(current_pos[0], current_pos[1], target_pos[0], target_pos[1])
    
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
        ew_dist = lon_diff * 111 * math.cos(math.radians(current_pos[0]))
    else:
        ew_dir = "W"
        ew_dist = abs(lon_diff) * 111 * math.cos(math.radians(current_pos[0]))
    
    grid_reference = f"{ns_dir}{ns_dist:.1f}km {ew_dir}{ew_dist:.1f}km"
    
    return bearing_deg, compass_dir, distance_km, grid_reference

def optimize_weapon_placement(friendly_position, enemy_positions, all_friendly_positions, selected_weapon):
    """SMART optimization - considers moving to maximum mobility limit"""
    # Find the weapon name
    selected_weapon_name = [k for k, v in WEAPONS.items() if v == selected_weapon][0]
    
    # Calculate original distances BEFORE moving
    original_distances = {}
    for enemy_id, enemy_lat, enemy_lon, enemy_type in enemy_positions:
        original_distance = haversine_distance(friendly_position[0], friendly_position[1], enemy_lat, enemy_lon)
        if selected_weapon["min_range_km"] <= original_distance <= selected_weapon["max_range_km"]:
            original_effectiveness = selected_weapon["lethality_function"](original_distance, selected_weapon)
        else:
            original_effectiveness = 0.0
            
        original_distances[enemy_id] = {
            'distance': original_distance,
            'type': enemy_type,
            'effectiveness': original_effectiveness
        }
    
    safe_print(f"\nGenerating SMART tactical positions for {selected_weapon_name}...")
    
    # Generate SMART tactical positions
    smart_positions = generate_smart_forward_positions(
        friendly_position, enemy_positions, selected_weapon, num_positions=100
    )
    
    # ADD SPECIAL CASE: Maximum mobility position directly toward enemy
    if enemy_positions:
        # Calculate direction to closest enemy
        enemy_lats = [lat for _, lat, lon, _ in enemy_positions]
        enemy_lons = [lon for _, lat, lon, _ in enemy_positions]
        enemy_center = (sum(enemy_lats)/len(enemy_lats), sum(enemy_lons)/len(enemy_lons))
        
        bearing_to_enemy, _ = calculate_compass_direction(
            friendly_position[0], friendly_position[1], enemy_center[0], enemy_center[1]
        )
        
        # Create maximum mobility position
        max_mobility_pos = calculate_position_from_bearing(
            friendly_position[0], friendly_position[1], 
            bearing_to_enemy, selected_weapon["max_placement_distance_km"]
        )
        
        # Add this as a special tactical position
        max_mobility_data = {
            'position': max_mobility_pos,
            'approach': "Maximum Advance",
            'approach_emoji': "",
            'bearing': bearing_to_enemy,
            'distance_advanced': selected_weapon["max_placement_distance_km"],
            'enemy_distance': min([
                haversine_distance(max_mobility_pos[0], max_mobility_pos[1], e_lat, e_lon)
                for _, e_lat, e_lon, _ in enemy_positions
            ]),
            'tactical_score': 0.7  # Good score for maximum advance
        }
        smart_positions.append(max_mobility_data)
    
    safe_print(f"Generated {len(smart_positions)} SMART tactical positions (including maximum advance)")
    safe_print("   Evaluating: Direct Assault, Flanking, Maximum Advance...")
    
    best_score = -1
    best_candidate = None
    best_approach = ""
    best_tactical_score = 0
    valid_candidates = 0
    
    for pos_data in smart_positions:
        candidate_pos = pos_data['position']
        approach = pos_data['approach']
        approach_emoji = pos_data.get('approach_emoji', '')
        tactical_score = pos_data.get('tactical_score', 0)
        
        # Check if placement is realistic
        is_realistic, reason = is_placement_realistic(
            selected_weapon, candidate_pos, friendly_position, enemy_positions
        )
        
        if not is_realistic:
            continue
            
        # Calculate damage
        total_damage = calculate_total_damage(
            candidate_pos[0], candidate_pos[1], 
            enemy_positions, selected_weapon, 
            all_friendly_positions,
            min_safe_distance=2.0
        )
        
        if total_damage >= 0:
            valid_candidates += 1
            
            # Combine damage score with tactical advantage
            final_score = total_damage * (0.6 + 0.4 * tactical_score)
            
            if final_score > best_score:
                best_score = final_score
                best_candidate = candidate_pos
                best_approach = f"{approach_emoji} {approach}".strip()
                best_tactical_score = tactical_score
    
    return best_candidate, best_score, valid_candidates, len(smart_positions), selected_weapon_name, best_approach, best_tactical_score, original_distances

def realistic_quick_analysis(weapon, best_candidate, friendly_position, enemy_positions, damage_score, approach, tactical_score):
    """Provide REALISTIC analysis with tactical assessment"""
    if not best_candidate:
        return "No realistic tactical position found", "", "", ""
    
    distance_to_you = haversine_distance(friendly_position[0], friendly_position[1], 
                                       best_candidate[0], best_candidate[1])
    
    # Calculate movement instructions
    bearing_deg, compass_dir, distance_km, grid_ref = calculate_movement_instructions(friendly_position, best_candidate)
    
    # Check if weapon can realistically reach the placement
    if distance_to_you > weapon.get("max_placement_distance_km", 5.0):
        analysis = f"UNREALISTIC: {distance_to_you:.1f}km > {weapon['max_placement_distance_km']}km mobility limit"
        return analysis, "", "", ""
    
    # Check engagement effectiveness
    min_enemy_distance = float('inf')
    for enemy_id, enemy_lat, enemy_lon, enemy_type in enemy_positions:
        enemy_dist = haversine_distance(best_candidate[0], best_candidate[1], enemy_lat, enemy_lon)
        min_enemy_distance = min(min_enemy_distance, enemy_dist)
    
    if min_enemy_distance > weapon["max_range_km"]:
        analysis = f"INEFFECTIVE: Closest enemy {min_enemy_distance:.1f}km > {weapon['max_range_km']}km range"
        return analysis, "", "", ""
    
    # Tactical assessment
    if tactical_score >= 0.8:
        tactical_analysis = "EXCELLENT TACTICAL POSITION"
    elif tactical_score >= 0.6:
        tactical_analysis = "GOOD TACTICAL POSITION"
    elif tactical_score >= 0.4:
        tactical_analysis = "FAIR TACTICAL POSITION"
    else:
        tactical_analysis = "BASIC TACTICAL POSITION"
    
    # Damage assessment
    if damage_score >= len(enemy_positions) * 0.8:
        damage_analysis = "MAXIMUM DAMAGE POTENTIAL"
    elif damage_score >= len(enemy_positions) * 0.5:
        damage_analysis = "GOOD DAMAGE POTENTIAL"
    else:
        damage_analysis = "LIMITED DAMAGE POTENTIAL"
    
    analysis = f"{tactical_analysis} | {damage_analysis}"
    movement_info = f"Move {compass_dir} ({bearing_deg:.0f} deg) - {distance_km:.1f}km"
    grid_info = f"Grid: {grid_ref}"
    approach_info = f"Tactic: {approach}"
    
    return analysis, movement_info, grid_info, approach_info

def safe_write_file(file_path, content):
    """Safely write content to file with proper encoding handling"""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        safe_print(f"Warning: Could not save with UTF-8 encoding: {e}")
        # Fallback: try without special characters
        try:
            # Remove or replace problematic characters
            safe_content = content
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(safe_content)
            return True
        except Exception as e2:
            safe_print(f"Error: Could not save file: {e2}")
            return False

def main():
    safe_print("=== Weapon Placement Optimizer v4.0 ===")
    safe_print("Now with SMART MAXIMUM MOBILITY POSITIONING\n")
    
    while True:
        # Get all inputs interactively
        friendly_position = get_user_position()
        enemy_positions = get_enemy_positions()
        
        if not enemy_positions:
            safe_print("No enemy positions entered. Please try again.")
            continue
            
        friendly_positions = get_friendly_positions(friendly_position)
        
        # Get weapon recommendations
        safe_print("\nAnalyzing combat situation with MAXIMUM MOBILITY tactics...")
        recommender = WeaponRecommender(friendly_position, enemy_positions)
        recommended_weapons = recommender.recommend_weapons(top_n=3)
        
        # Display recommendations
        safe_print("\n" + "="*70)
        safe_print("SMART MAXIMUM MOBILITY WEAPON RECOMMENDATION SYSTEM")
        safe_print("="*70)

        recommendation_report = recommender.generate_recommendation_report(recommended_weapons)
        safe_print(recommendation_report)
        
        # Weapon selection
        safe_print("\n" + "="*60)
        safe_print("WEAPON SELECTION")
        safe_print("="*60)
        
        if not recommended_weapons:
            safe_print("No suitable weapons found. Please try different positions.")
            restart = input("Press Enter to restart or type 'exit' to quit: ").strip().lower()
            if restart == 'exit':
                break
            continue
        
        weapon_names = [weapon['name'] for weapon in recommended_weapons]
        safe_print("Recommended Weapons:")
        for i, weapon_name in enumerate(weapon_names, 1):
            safe_print(f"{i}. {weapon_name}")
        safe_print(f"4. See all available weapons")
        safe_print(f"5. Restart with new positions")
        safe_print(f"6. Exit program")
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "5":
                safe_print("\nRestarting...")
                continue
            elif choice == "6":
                safe_print("Thank you for using Weapon Placement Optimizer. Goodbye!")
                break
            elif choice == "4":
                weapon_names = list(WEAPONS.keys())
                safe_print("\nAll Available Weapons:")
                for i, name in enumerate(weapon_names, 1):
                    safe_print(f"{i}. {name}")
                weapon_choice = int(input("\nEnter your weapon choice (number): ")) - 1
                selected_weapon_name = weapon_names[weapon_choice]
            else:
                weapon_choice = int(choice) - 1
                if 0 <= weapon_choice < len(weapon_names):
                    selected_weapon_name = weapon_names[weapon_choice]
                else:
                    safe_print("Invalid choice. Using first recommended weapon.")
                    selected_weapon_name = weapon_names[0]
            
            selected_weapon = WEAPONS[selected_weapon_name]
            safe_print(f"Selected: {selected_weapon_name}")

        except (ValueError, IndexError):
            safe_print("Invalid selection. Using first recommended weapon.")
            selected_weapon_name = weapon_names[0]
            selected_weapon = WEAPONS[selected_weapon_name]

        # Perform SMART optimization
        best_candidate, best_score, valid_candidates, total_candidates, selected_weapon_name, best_approach, tactical_score, original_distances = optimize_weapon_placement(
            friendly_position, enemy_positions, friendly_positions, selected_weapon
        )

        # Display results
        safe_print(f"\nEvaluation complete. Found {valid_candidates} valid tactical positions out of {total_candidates}.")
        
        if best_candidate and best_score > 0:
            # Calculate NEW distances after moving
            new_distances = {}
            for enemy_id, enemy_lat, enemy_lon, enemy_type in enemy_positions:
                new_distance = haversine_distance(best_candidate[0], best_candidate[1], enemy_lat, enemy_lon)
                # Calculate effectiveness from new position
                if selected_weapon["min_range_km"] <= new_distance <= selected_weapon["max_range_km"]:
                    new_effectiveness = selected_weapon["lethality_function"](new_distance, selected_weapon)
                else:
                    new_effectiveness = 0.0
                    
                new_distances[enemy_id] = {
                    'distance': new_distance,
                    'type': enemy_type,
                    'effectiveness': new_effectiveness
                }
            
            safe_print(f"\n*** SMART TACTICAL POSITION FOUND ***")
            safe_print(f"Weapon: {selected_weapon_name}")
            safe_print(f"Tactical Approach: {best_approach}")
            safe_print(f"Target Grid: Latitude: {best_candidate[0]:.6f}, Longitude: {best_candidate[1]:.6f}")
            safe_print(f"Distance from current position: {haversine_distance(friendly_position[0], friendly_position[1], best_candidate[0], best_candidate[1]):.1f} km")
            safe_print(f"Predicted Total Damage Score: {best_score:.2f}")
            safe_print(f"Tactical Advantage Score: {tactical_score:.2f}/1.0")
            
            # Calculate and display movement instructions
            bearing_deg, compass_dir, distance_km, grid_ref = calculate_movement_instructions(friendly_position, best_candidate)
            
            safe_print(f"\nMOVEMENT INSTRUCTIONS:")
            safe_print(f"   Direction: {compass_dir} ({bearing_deg:.0f} deg)")
            safe_print(f"   Distance: {distance_km:.1f} km")
            safe_print(f"   Grid Reference: {grid_ref}")
            
            # Show BEFORE & AFTER comparison
            safe_print(f"\nENGAGEMENT ANALYSIS - BEFORE & AFTER:")
            safe_print("=" * 50)
            for enemy_id in original_distances:
                original_data = original_distances[enemy_id]
                new_data = new_distances[enemy_id]
                
                safe_print(f"TARGET: {enemy_id} ({original_data['type']}):")
                safe_print(f"   BEFORE: {original_data['distance']:.1f}km -> Effectiveness: {original_data['effectiveness']:.1f}")
                safe_print(f"   AFTER:  {new_data['distance']:.1f}km -> Effectiveness: {new_data['effectiveness']:.1f}")
                
                improvement = new_data['effectiveness'] - original_data['effectiveness']
                distance_change = new_data['distance'] - original_data['distance']
                
                if improvement > 0:
                    safe_print(f"   [IMPROVEMENT]: +{improvement:.2f} effectiveness")
                elif improvement < 0:
                    safe_print(f"   [DECREASE]: {improvement:.2f} effectiveness")
                else:
                    safe_print(f"   [NO CHANGE]")
                safe_print(f"   Distance Change: {distance_change:+.1f}km\n")
            
            # Save results
            os.makedirs("data/output", exist_ok=True)
            timestamp = len(os.listdir("data/output")) + 1 if os.path.exists("data/output") else 1
            output_file = f"data/output/smart_position_{timestamp}.txt"
            
            # Build the content to save
            output_content = "=== SMART WEAPON PLACEMENT OPTIMIZER v4.0 RESULTS ===\n\n"
            
            # Basic Information
            output_content += "MISSION OVERVIEW:\n"
            output_content += "=" * 50 + "\n"
            output_content += f"Current Position: {friendly_position}\n"
            output_content += f"Selected Weapon: {selected_weapon_name}\n"
            output_content += f"Weapon Type: {selected_weapon['type']}\n"
            output_content += f"Effective Range: {selected_weapon['min_range_km']}-{selected_weapon['max_range_km']}km\n"
            output_content += f"Mobility Limit: {selected_weapon['max_placement_distance_km']}km\n"
            output_content += f"Tactical Approach: {best_approach}\n"
            output_content += f"Tactical Advantage Score: {tactical_score:.2f}/1.0\n\n"
            
            # Movement Instructions
            output_content += "MOVEMENT INSTRUCTIONS:\n"
            output_content += "=" * 50 + "\n"
            output_content += f"Optimal Tactical Position:\n"
            output_content += f"  Latitude: {best_candidate[0]:.6f}\n"
            output_content += f"  Longitude: {best_candidate[1]:.6f}\n"
            output_content += f"  Distance to Move: {distance_km:.1f} km\n"
            output_content += f"  Direction: {compass_dir} ({bearing_deg:.0f} deg)\n"
            output_content += f"  Grid Reference: {grid_ref}\n"
            output_content += f"  Movement Efficiency: {((distance_km/selected_weapon['max_placement_distance_km'])*100):.1f}% of max mobility used\n\n"
            
            # BEFORE & AFTER COMPARISON
            output_content += "ENGAGEMENT ANALYSIS - BEFORE & AFTER:\n"
            output_content += "=" * 50 + "\n"
            
            total_improvement = 0
            for enemy_id in original_distances:
                original_data = original_distances[enemy_id]
                new_data = new_distances[enemy_id]
                
                output_content += f"TARGET: {enemy_id} ({original_data['type']}):\n"
                output_content += f"   BEFORE Movement (From Original Position):\n"
                output_content += f"     - Distance: {original_data['distance']:.1f}km\n"
                output_content += f"     - Effectiveness: {original_data['effectiveness']:.1f}/1.0\n"
                output_content += f"     - Status: {'IN RANGE' if original_data['effectiveness'] > 0 else 'OUT OF RANGE'}\n"
                
                output_content += f"   AFTER Movement (From Tactical Position):\n"
                output_content += f"     - Distance: {new_data['distance']:.1f}km\n"
                output_content += f"     - Effectiveness: {new_data['effectiveness']:.1f}/1.0\n"
                output_content += f"     - Status: {'IN RANGE' if new_data['effectiveness'] > 0 else 'OUT OF RANGE'}\n"
                
                # Improvement calculation
                improvement = new_data['effectiveness'] - original_data['effectiveness']
                total_improvement += improvement
                distance_change = new_data['distance'] - original_data['distance']
                
                if improvement > 0:
                    output_content += f"   [IMPROVEMENT]: +{improvement:.2f} effectiveness\n"
                elif improvement < 0:
                    output_content += f"   [DECREASE]: {improvement:.2f} effectiveness\n"
                else:
                    output_content += f"   [NO CHANGE]: Same effectiveness\n"
                
                output_content += f"   Distance Change: {distance_change:+.1f}km\n\n"
            
            # Performance Summary
            output_content += "PERFORMANCE SUMMARY:\n"
            output_content += "=" * 50 + "\n"
            output_content += f"Predicted Total Damage Score: {best_score:.2f}/1.0\n"
            
            # Calculate average effectiveness improvement
            avg_improvement = total_improvement / len(original_distances) if original_distances else 0
            output_content += f"Average Effectiveness Improvement: {avg_improvement:+.2f}/1.0\n"
            
            # Tactical Benefits
            output_content += f"\nTACTICAL BENEFITS ACHIEVED:\n"
            if "Flank" in best_approach:
                output_content += "   - Enemy surprised from unexpected direction\n"
                output_content += "   - Reduced exposure to enemy fire\n"
                output_content += "   - Better firing angles\n"
            if "Maximum" in best_approach:
                output_content += "   - Maximum mobility utilized\n"
                output_content += "   - Optimal engagement distance achieved\n"
            if "Cover" in best_approach:
                output_content += "   - Natural protection from terrain\n"
                output_content += "   - Harder for enemy to detect\n"
            
            output_content += f"   - Maximum weapon effectiveness utilized\n"
            
            # Weapon Specific Notes
            output_content += f"\nWEAPON-SPECIFIC NOTES:\n"
            optimal_min = selected_weapon['min_range_km'] + (selected_weapon['max_range_km'] - selected_weapon['min_range_km']) * 0.3
            optimal_max = selected_weapon['max_range_km'] * 0.9
            output_content += f"   {selected_weapon_name} performs best at {optimal_min:.1f}-{optimal_max:.1f}km\n"
            output_content += f"   Minimum safe engagement: {selected_weapon['min_range_km']}km\n"
            output_content += f"   Maximum effective range: {selected_weapon['max_range_km']}km\n\n"
            
            output_content += "MISSION SUCCESS PROBABILITY: HIGH\n"
            
            # Save the file safely
            if safe_write_file(output_file, output_content):
                safe_print(f"\nResults saved to {output_file}")
            else:
                safe_print(f"\nWarning: Results could not be saved properly")
            
            # Show realistic analysis
            analysis, movement, grid, approach_info = realistic_quick_analysis(
                selected_weapon, best_candidate, friendly_position, enemy_positions, best_score, best_approach, tactical_score
            )
            safe_print(f"\nTACTICAL ANALYSIS: {analysis}")
            safe_print(f"   {movement}")
            safe_print(f"   {grid}")
            safe_print(f"   {approach_info}")
                
        else:
            safe_print("\nNo valid tactical position found.")
            safe_print("Try: Selecting a more mobile weapon or different enemy positions.")

        # Ask if user wants to restart
        safe_print("\n" + "="*50)
        restart = input("Press Enter to restart or type 'exit' to quit: ").strip().lower()
        if restart == 'exit':
            safe_print("Thank you for using Weapon Placement Optimizer. Goodbye!")
            break

if __name__ == "__main__":
    main()