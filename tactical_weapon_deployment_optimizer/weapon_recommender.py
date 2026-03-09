# weapon_recommender.py - UPDATED WITH SMART MAXIMUM MOBILITY LOGIC

from weapons.weapons_data import WEAPONS
from utils.geoutils import haversine_distance, calculate_position_from_bearing, calculate_compass_direction

def safe_print(text):
    """Safely print text that might contain special characters"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback: replace problematic characters
        safe_text = text.encode('utf-8', errors='replace').decode('utf-8')
        print(safe_text)

class WeaponRecommender:
    def __init__(self, friendly_position, enemy_positions):
        self.friendly_pos = friendly_position
        self.enemy_positions = enemy_positions
        
    def analyze_enemy_composition(self):
        """Analyze what types of enemies we're facing"""
        enemy_types = {}
        for enemy_id, enemy_lat, enemy_lon, enemy_type in self.enemy_positions:
            enemy_types[enemy_type] = enemy_types.get(enemy_type, 0) + 1
        return enemy_types
    
    def calculate_enemy_cluster_info(self):
        """Find enemy cluster center and spread"""
        if not self.enemy_positions:
            return None, 0
            
        avg_lat = sum(lat for _, lat, lon, _ in self.enemy_positions) / len(self.enemy_positions)
        avg_lon = sum(lon for _, lat, lon, _ in self.enemy_positions) / len(self.enemy_positions)
        
        max_distance = 0
        for enemy_id, enemy_lat, enemy_lon, enemy_type in self.enemy_positions:
            distance = haversine_distance(avg_lat, avg_lon, enemy_lat, enemy_lon)
            max_distance = max(max_distance, distance)
            
        return (avg_lat, avg_lon), max_distance
    
    def calculate_engagement_distance(self):
        """Calculate distances from friendly position to enemies"""
        distances = []
        for enemy_id, enemy_lat, enemy_lon, enemy_type in self.enemy_positions:
            distance = haversine_distance(self.friendly_pos[0], self.friendly_pos[1], enemy_lat, enemy_lon)
            distances.append(distance)
        return distances
    
    def can_weapon_reach_realistically(self, weapon_data, cluster_center):
        """SMART CHECK: Consider moving to max mobility limit to engage"""
        explanations = []
        
        if not self.enemy_positions:
            return False, ["No enemy positions"]
        
        # 1. Find closest enemy distance
        closest_enemy_distance = float('inf')
        closest_enemy_pos = None
        for enemy_id, enemy_lat, enemy_lon, enemy_type in self.enemy_positions:
            distance_to_enemy = haversine_distance(self.friendly_pos[0], self.friendly_pos[1], 
                                                 enemy_lat, enemy_lon)
            if distance_to_enemy < closest_enemy_distance:
                closest_enemy_distance = distance_to_enemy
                closest_enemy_pos = (enemy_lat, enemy_lon)
        
        max_mobility = weapon_data["max_placement_distance_km"]
        max_range = weapon_data["max_range_km"]
        min_range = weapon_data["min_range_km"]
        
        # 2. SMART CHECK: Calculate distance after moving MAXIMUM possible distance toward enemy
        if closest_enemy_pos:
            # Calculate position after moving maximum distance toward closest enemy
            bearing_to_enemy, _ = calculate_compass_direction(
                self.friendly_pos[0], self.friendly_pos[1], 
                closest_enemy_pos[0], closest_enemy_pos[1]
            )
            
            max_advance_pos = calculate_position_from_bearing(
                self.friendly_pos[0], self.friendly_pos[1], 
                bearing_to_enemy, max_mobility
            )
            
            # Calculate distance from maximum advance position to enemy
            distance_after_max_move = haversine_distance(
                max_advance_pos[0], max_advance_pos[1],
                closest_enemy_pos[0], closest_enemy_pos[1]
            )
        else:
            distance_after_max_move = closest_enemy_distance - max_mobility
        
        # 3. Check if weapon can engage after moving to maximum mobility position
        if distance_after_max_move <= max_range and distance_after_max_move >= min_range:
            # Weapon CAN engage if we move to maximum mobility position
            effectiveness_after_move = weapon_data["lethality_function"](distance_after_max_move, weapon_data)
            explanations.append(f"CAN ENGAGE: Move {max_mobility}km forward to engage at {distance_after_max_move:.1f}km")
            explanations.append(f"Effectiveness after movement: {effectiveness_after_move:.1f}/1.0")
            return True, explanations
        
        # 4. Check if weapon can engage from current position (no movement needed)
        elif min_range <= closest_enemy_distance <= max_range:
            effectiveness_current = weapon_data["lethality_function"](closest_enemy_distance, weapon_data)
            explanations.append(f"CAN ENGAGE FROM CURRENT POSITION: Enemy at perfect range")
            explanations.append(f"Effectiveness: {effectiveness_current:.1f}/1.0 - No movement needed")
            return True, explanations
        
        # 5. Check if enemy is within range but too close (need to move backward - not allowed)
        elif closest_enemy_distance < min_range:
            explanations.append(f"ENEMY TOO CLOSE: {closest_enemy_distance:.1f}km < {min_range:.1f}km minimum range")
            explanations.append("Cannot move backward - consider different weapon")
            return False, explanations
        
        # 6. Enemy is beyond range even after maximum movement
        else:
            # Calculate how much closer we need to move
            additional_movement_needed = closest_enemy_distance - max_range
            if additional_movement_needed > max_mobility:
                additional_movement_needed -= max_mobility
                explanations.append(f"BEYOND MAXIMUM REACH: Need to move {additional_movement_needed:.1f}km closer first")
                explanations.append(f"Even after moving {max_mobility}km, enemy would be {distance_after_max_move:.1f}km away")
            else:
                explanations.append(f"CANNOT ENGAGE: Enemy {closest_enemy_distance:.1f}km beyond effective range")
            return False, explanations
    
    def evaluate_weapon_suitability(self, weapon_name, weapon_data):
        """Comprehensive weapon evaluation with SMART MAXIMUM MOBILITY checks"""
        scores = {}
        explanations = []
        
        # Get battlefield analysis
        enemy_types = self.analyze_enemy_composition()
        cluster_center, cluster_spread = self.calculate_enemy_cluster_info()
        engagement_distances = self.calculate_engagement_distance()
        closest_enemy_distance = min(engagement_distances) if engagement_distances else 0
        
        # REALITY CHECK: Can this weapon engage considering maximum mobility?
        can_engage, engage_explanations = self.can_weapon_reach_realistically(weapon_data, cluster_center)
        explanations.extend(engage_explanations)
        
        if not can_engage:
            return 0.1, explanations, {"target_matching": 0.0, "range_mobility": 0.0, "tactical": 0.1}
        
        # 1. Target Matching Analysis (40% weight)
        target_score = 0
        perfect_matches = 0
        poor_matches = 0
        
        for enemy_type, count in enemy_types.items():
            if enemy_type in weapon_data["preferred_targets"]:
                target_score += count * 1.0
                perfect_matches += count
                explanations.append(f"Perfect against {count} {enemy_type}(s)")
            elif enemy_type in weapon_data["unsuitable_targets"]:
                target_score += count * 0.1
                poor_matches += count
                explanations.append(f"Poor against {count} {enemy_type}(s)")
            else:
                target_score += count * 0.6
                explanations.append(f"Neutral against {count} {enemy_type}(s)")
        
        target_score_normalized = target_score / len(self.enemy_positions) if self.enemy_positions else 0
        scores["target_matching"] = target_score_normalized * 0.40
        
        # 2. Range and Mobility Analysis (35% weight)
        mobility_scores = {"high": 1.0, "medium": 0.7, "low": 0.4}
        mobility_score = mobility_scores.get(weapon_data["mobility"], 0.5)
        
        # Calculate effectiveness considering maximum mobility
        max_mobility_effectiveness = self.calculate_max_mobility_effectiveness(weapon_data, closest_enemy_distance)
        
        # Mobility advantage
        if weapon_data["mobility"] == "high":
            mobility_advantage = 1.0
            explanations.append("High mobility - can use maximum advance effectively")
        elif weapon_data["mobility"] == "medium":
            mobility_advantage = 0.7
            explanations.append("Medium mobility - good for tactical advances")
        else:
            mobility_advantage = 0.4
            explanations.append("Low mobility - limited advance capability")
        
        range_mobility_score = (mobility_score * 0.4 + max_mobility_effectiveness * 0.6)
        scores["range_mobility"] = range_mobility_score * 0.35
        
        # 3. Tactical Effectiveness (25% weight)
        deployment_speed = max(0, 1 - (weapon_data["deployment_time_min"] / 30))
        
        # Maximum advance capability
        if weapon_data["mobility"] == "high":
            advance_score = 0.9
            explanations.append("Excellent maximum advance capability")
        elif weapon_data["mobility"] == "medium":
            advance_score = 0.7
            explanations.append("Good maximum advance capability")
        else:
            advance_score = 0.5
            explanations.append("Limited maximum advance capability")
        
        tactical_score = (max_mobility_effectiveness * 0.5 + deployment_speed * 0.3 + advance_score * 0.2)
        scores["tactical"] = tactical_score * 0.25
        
        # 4. Calculate final score
        final_score = sum(scores.values())
        
        # Add tactical summary
        explanations.append(f"Closest enemy: {closest_enemy_distance:.1f}km")
        explanations.append(f"Effective range: {weapon_data['min_range_km']}-{weapon_data['max_range_km']}km")
        explanations.append(f"Max advance: {weapon_data['max_placement_distance_km']}km")
        
        return final_score, explanations, scores
    
    def calculate_max_mobility_effectiveness(self, weapon_data, enemy_distance):
        """Calculate effectiveness after moving maximum distance toward enemy"""
        max_mobility = weapon_data["max_placement_distance_km"]
        max_range = weapon_data["max_range_km"]
        min_range = weapon_data["min_range_km"]
        
        # Calculate distance after maximum movement
        distance_after_max_move = max(0, enemy_distance - max_mobility)
        
        if distance_after_max_move < min_range:
            return 0.0  # Would be too close even after maximum movement
        elif distance_after_max_move <= max_range:
            # Calculate effectiveness from optimal position after maximum movement
            return weapon_data["lethality_function"](distance_after_max_move, weapon_data)
        else:
            return 0.0  # Still out of range after maximum movement
    
    def recommend_weapons(self, top_n=5):
        """Recommend weapons considering MAXIMUM MOBILITY potential"""
        if not self.enemy_positions:
            safe_print("No enemy positions provided for analysis")
            return []
            
        enemy_composition = self.analyze_enemy_composition()
        engagement_distances = self.calculate_engagement_distance()
        closest_enemy_distance = min(engagement_distances) if engagement_distances else 0
        
        safe_print(f"\nSMART BATTLEFIELD ANALYSIS:")
        safe_print(f"   Enemy Composition: {', '.join([f'{k} ({v})' for k, v in enemy_composition.items()])}")
        safe_print(f"   Closest Enemy: {closest_enemy_distance:.1f}km")
        safe_print(f"   Total Targets: {len(self.enemy_positions)}")
        safe_print(f"   TACTIC: MAXIMUM MOBILITY ASSAULT")
        
        weapon_assessments = []
        
        safe_print(f"\nAnalyzing {len(WEAPONS)} weapons for MAXIMUM MOBILITY engagement...")
        
        for weapon_name, weapon_data in WEAPONS.items():
            score, explanations, breakdown = self.evaluate_weapon_suitability(weapon_name, weapon_data)
            weapon_assessments.append({
                'name': weapon_name,
                'score': score,
                'explanations': explanations,
                'breakdown': breakdown,
                'data': weapon_data
            })
        
        # Filter for weapons that can actually engage with maximum mobility
        mobile_weapons = [w for w in weapon_assessments if w['score'] > 0.2]
        mobile_weapons.sort(key=lambda x: x['score'], reverse=True)
        
        safe_print(f"Found {len(mobile_weapons)} suitable weapons for MAXIMUM MOBILITY ASSAULT")
        
        return mobile_weapons[:top_n]

    def generate_recommendation_report(self, recommendations):
        """Generate report for MAXIMUM MOBILITY recommendations"""
        report = []
        
        if not recommendations:
            report.append("NO SUITABLE WEAPONS FOR MAXIMUM MOBILITY ASSAULT")
            report.append("   No weapons can engage even after maximum forward movement")
            report.append("   Consider:")
            report.append("   • Moving your entire unit closer to enemy positions")
            report.append("   • Using different engagement strategies")
            report.append("   • Requesting support from longer-range assets")
            return "\n".join(report)
        
        report.append(f"TOP {len(recommendations)} MAXIMUM MOBILITY WEAPONS:")
        report.append("")
        
        for i, weapon in enumerate(recommendations, 1):
            if weapon['score'] >= 0.7:
                score_color = "EXCELLENT"
                symbol = "[BEST]"
            elif weapon['score'] >= 0.5:
                score_color = "GOOD" 
                symbol = "[GOOD]"
            elif weapon['score'] >= 0.3:
                score_color = "FAIR"
                symbol = "[FAIR]"
            else:
                score_color = "MARGINAL"
                symbol = "[WEAK]"
                
            report.append(f"{symbol} {i}. {weapon['name']} - {score_color} (Score: {weapon['score']:.2f}/1.0)")
            report.append(f"   Type: {weapon['data']['type']}")
            report.append(f"   Range: {weapon['data']['min_range_km']}-{weapon['data']['max_range_km']}km")
            report.append(f"   Mobility: {weapon['data']['mobility'].title()} (Max Advance: {weapon['data']['max_placement_distance_km']}km)")
            
            # Key assessments for MAXIMUM MOBILITY
            report.append("   MAXIMUM MOBILITY ASSESSMENT:")
            critical_items = [e for e in weapon['explanations'] if any(x in e for x in ['CAN ENGAGE', 'Effectiveness', 'mobility', 'advance'])]
            
            for explanation in critical_items[:4]:
                report.append(f"      - {explanation}")
            
            # Mobility capability
            if weapon['data']['mobility'] == "high":
                report.append(f"   MOBILITY: EXCELLENT - Can utilize full advance potential")
            elif weapon['data']['mobility'] == "medium":
                report.append(f"   MOBILITY: GOOD - Effective maximum advance")
            else:
                report.append(f"   MOBILITY: LIMITED - Restricted advance capability")
                
            report.append("")
        
        return "\n".join(report)