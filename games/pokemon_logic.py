import json


def load_pokemon_data():
    with open("./stats/pokemon/sc_vi/pokemon_list.json") as f:
        return json.load(f)


def get_pokemon_stats(pokemon_name: str):
    data = load_pokemon_data()
    pokemon_data = data["pokemon"]

    # Check if pokemon exists
    if pokemon_name not in pokemon_data:
        raise ValueError(f"Pokemon '{pokemon_name}' doesn't exist in Scarlet & Violet!")

    target_pokemon = pokemon_data[pokemon_name]

    # Calculate base stat total
    base_stat_total = sum(target_pokemon["stats"].values())

    return {
        "name": pokemon_name,
        "dex_id": target_pokemon["home_dex_id"],
        "stats": target_pokemon["stats"],
        "base_stat_total": base_stat_total,
        "types": target_pokemon["types"],
        "abilities": target_pokemon["abilities"],
        "legal_formats": target_pokemon["legal_vgc_formats"]
    }
