import os
from dotenv import load_dotenv
import discord
from discord import app_commands
import json

load_dotenv()

# Load data from JSON
with open('./stats/data.json') as f:
    data = json.load(f)


class MarioKartBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.tree.sync()


bot = MarioKartBot()


def find_matching_parts(category_data, selected_stats):
    matching_parts = []
    for part_name, stats in category_data.items():
        # Check if all stats match
        if all(stats[key] == selected_stats[key] for key in selected_stats):
            matching_parts.append(part_name)
    return matching_parts


@bot.tree.command(name="combostats", description="Get stats for Mario Kart 8 Deluxe combo")
@app_commands.describe(
    character="Choose a character",
    vehicle="Choose a vehicle",
    tires="Choose a set of tires",
    glider="Choose a glider"
)
async def combostats(interaction: discord.Interaction, character: str, vehicle: str, tires: str, glider: str):
    try:
        # Retrieve stats for each selected part
        char_stats = data["characters"][character]
        vehicle_stats = data["vehicles"][vehicle]
        tires_stats = data["tires"][tires]
        glider_stats = data["gliders"][glider]

        # Calculate total stats
        total_stats = {
            "acceleration": char_stats["acceleration"] + vehicle_stats["acceleration"] + tires_stats["acceleration"] + glider_stats["acceleration"],
            "weight": char_stats["weight"] + vehicle_stats["weight"] + tires_stats["weight"] + glider_stats["weight"],
            "mini_turbo": char_stats["mini_turbo"] + vehicle_stats["mini_turbo"] + tires_stats["mini_turbo"] + glider_stats["mini_turbo"],
            "speed": [sum(x) for x in zip(char_stats["speed"], vehicle_stats["speed"], tires_stats["speed"], glider_stats["speed"])],
            "handling": [sum(x) for x in zip(char_stats["handling"], vehicle_stats["handling"], tires_stats["handling"], glider_stats["handling"])],
            "traction": char_stats["traction"] + vehicle_stats["traction"] + tires_stats["traction"] + glider_stats["traction"]
        }

        # Find matching parts
        matching_characters = find_matching_parts(
            data["characters"], char_stats)
        matching_vehicles = find_matching_parts(
            data["vehicles"], vehicle_stats)
        matching_tires = find_matching_parts(data["tires"], tires_stats)
        matching_gliders = find_matching_parts(data["gliders"], glider_stats)

        # Filter out the selected part from each matching list
        matching_characters = [char for char in matching_characters if char != character]
        if not matching_characters:
            matching_characters = ["None found."]
        matching_vehicles = [vehicle_name for vehicle_name in matching_vehicles if vehicle_name != vehicle]
        if not matching_vehicles:
            matching_vehicles = ["None found."]
        matching_tires = [tire_name for tire_name in matching_tires if tire_name != tires]
        if not matching_tires:
            matching_tires = ["None found."]
        matching_gliders = [glider_name for glider_name in matching_gliders if glider_name != glider]
        if not matching_gliders:
            matching_gliders = ["None found."]


        # Build response
        response = (
            f"Speed & Handling are listed in the order of **Ground/Air/Water/Anti-Gravity**\n"
            f"Other stats are listed in the order of **Acceleration/Weight/Mini-Turbo/Traction**\n\n"
        )

        response += (
            f"- {character}: {char_stats['acceleration']}/{char_stats['weight']}/{char_stats['mini_turbo']}/{char_stats['traction']} | "
            f"{'/'.join(map(str, char_stats['speed']))} (Speed) | "
            f"{'/'.join(map(str, char_stats['handling']))} (Handling)\n"
            f"-> Matching characters: {', '.join(matching_characters)}\n\n"
        )

        response += (
            f"- {vehicle}: {vehicle_stats['acceleration']}/{vehicle_stats['weight']}/{vehicle_stats['mini_turbo']}/{vehicle_stats['traction']} | "
            f"{'/'.join(map(str, vehicle_stats['speed']))} (Speed) | "
            f"{'/'.join(map(str, vehicle_stats['handling']))} (Handling)\n"
            f"-> Matching vehicles: {', '.join(matching_vehicles)}\n\n"
        )

        response += (
            f"- {tires}: {tires_stats['acceleration']}/{tires_stats['weight']}/{tires_stats['mini_turbo']}/{tires_stats['traction']} | "
            f"{'/'.join(map(str, tires_stats['speed']))} (Speed) | "
            f"{'/'.join(map(str, tires_stats['handling']))} (Handling)\n"
            f"-> Matching tires: {', '.join(matching_tires)}\n\n"
        )

        response += (
            f"- {glider}: {glider_stats['acceleration']}/{glider_stats['weight']}/{glider_stats['mini_turbo']}/{glider_stats['traction']} | "
            f"{'/'.join(map(str, glider_stats['speed']))} (Speed) | "
            f"{'/'.join(map(str, glider_stats['handling']))} (Handling)\n"
            f"-> Matching gliders: {', '.join(matching_gliders)}\n\n"
        )

        # Total Stats
        response += (
            "Total Stats:\n"
            f"- Speed: {'/'.join(map(str, total_stats['speed']))}\n"
            f"- Acceleration: {total_stats['acceleration']}\n"
            f"- Weight: {total_stats['weight']}\n"
            f"- Handling: {'/'.join(map(str, total_stats['handling']))}\n"
            f"- Traction: {total_stats['traction']}\n"
            f"- Mini-Turbo: {total_stats['mini_turbo']}"
        )

        await interaction.response.send_message(response)

    except KeyError:
        await interaction.response.send_message("One or more of the selected parts do not exist in the database.", ephemeral=True)
    
    except Exception as e:
        await interaction.response.send_message(f"An error occured: {e}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
