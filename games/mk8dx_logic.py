import json

# Load data from JSON
with open('./stats/mario_kart/8_deluxe/kart_part_stats.json') as f:
    data = json.load(f)


def find_matching_parts(category_data, selected_stats):
    matching_parts = []
    for part_name, stats in category_data.items():
        if all(stats[key] == selected_stats[key] for key in selected_stats):
            matching_parts.append(part_name)
    return matching_parts


def get_case_insensitive_key(dictionary, search_key):
    # Find the actual key in the dictionary that matches the search key case-insensitively
    for key in dictionary:
        if key.lower() == search_key.lower():
            return key
    return None


def get_combo_stats(character: str, vehicle: str, tires: str, glider: str):
    try:
        # Find the correct case-sensitive keys
        character_key = get_case_insensitive_key(data["characters"], character)
        vehicle_key = get_case_insensitive_key(data["vehicles"], vehicle)
        tires_key = get_case_insensitive_key(data["tires"], tires)
        glider_key = get_case_insensitive_key(data["gliders"], glider)

        # Check if any parts weren't found
        if not all([character_key, vehicle_key, tires_key, glider_key]):
            raise ValueError("One or more of the selected parts do not exist in the database.")

        # Retrieve stats for each selected part
        char_stats = data["characters"][character_key]
        vehicle_stats = data["vehicles"][vehicle_key]
        tires_stats = data["tires"][tires_key]
        glider_stats = data["gliders"][glider_key]

        # Calculate total stats
        total_stats = {
            "acceleration": char_stats["acceleration"] + vehicle_stats["acceleration"] + tires_stats["acceleration"] + glider_stats["acceleration"],
            "weight": char_stats["weight"] + vehicle_stats["weight"] + tires_stats["weight"] + glider_stats["weight"],
            "mini_turbo": char_stats["mini_turbo"] + vehicle_stats["mini_turbo"] + tires_stats["mini_turbo"] + glider_stats["mini_turbo"],
            "speed": [sum(x) for x in zip(char_stats["speed"], vehicle_stats["speed"], tires_stats["speed"], glider_stats["speed"])],
            "handling": [sum(x) for x in zip(char_stats["handling"], vehicle_stats["handling"], tires_stats["handling"], glider_stats["handling"])],
            "traction": char_stats["traction"] + vehicle_stats["traction"] + tires_stats["traction"] + glider_stats["traction"]
        }

        # Find matching parts with case-insensitive comparison
        matching_characters = find_matching_parts(data["characters"], char_stats)
        matching_vehicles = find_matching_parts(data["vehicles"], vehicle_stats)
        matching_tires = find_matching_parts(data["tires"], tires_stats)
        matching_gliders = find_matching_parts(data["gliders"], glider_stats)

        return {
            "char_stats": char_stats,
            "vehicle_stats": vehicle_stats,
            "tires_stats": tires_stats,
            "glider_stats": glider_stats,
            "total_stats": total_stats,
            "matching_characters": [char for char in matching_characters if char.lower() != character_key.lower()] or ["None found."],
            "matching_vehicles": [v for v in matching_vehicles if v.lower() != vehicle_key.lower()] or ["None found."],
            "matching_tires": [t for t in matching_tires if t.lower() != tires_key.lower()] or ["None found."],
            "matching_gliders": [g for g in matching_gliders if g.lower() != glider_key.lower()] or ["None found."]
        }

    except KeyError:
        raise ValueError("One or more of the selected parts do not exist in the database.")
