import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from games.mk8dx_logic import get_combo_stats

load_dotenv()


class MarioKartBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.tree.sync()


bot = MarioKartBot()


@bot.tree.command(name="combostats", description="Get stats for Mario Kart 8 Deluxe combo")
@app_commands.describe(
    character="Choose a character",
    vehicle="Choose a vehicle",
    tires="Choose a set of tires",
    glider="Choose a glider"
)
async def combostats(interaction: discord.Interaction, character: str, vehicle: str, tires: str, glider: str):
    try:
        stats = get_combo_stats(character, vehicle, tires, glider)

        response = (
            "Speed & Handling are listed in the order of **Ground/Air/Water/Anti-Gravity**\n"
            "Other stats are listed in the order of **Acceleration/Weight/Mini-Turbo/Traction**\n\n"
        )

        response += (
            f"- {character}: {stats['char_stats']['acceleration']}/{stats['char_stats']['weight']}/{stats['char_stats']['mini_turbo']}/{stats['char_stats']['traction']} | "
            f"{'/'.join(map(str, stats['char_stats']['speed']))} (Speed) | "
            f"{'/'.join(map(str, stats['char_stats']['handling']))} (Handling)\n"
            f"-> Matching characters: {', '.join(stats['matching_characters'])}\n\n"
        )

        response += (
            f"- {vehicle}: {stats['vehicle_stats']['acceleration']}/{stats['vehicle_stats']['weight']}/{stats['vehicle_stats']['mini_turbo']}/{stats['vehicle_stats']['traction']} | "
            f"{'/'.join(map(str, stats['vehicle_stats']['speed']))} (Speed) | "
            f"{'/'.join(map(str, stats['vehicle_stats']['handling']))} (Handling)\n"
            f"-> Matching vehicles: {', '.join(stats['matching_vehicles'])}\n\n"
        )

        response += (
            f"- {tires}: {stats['tires_stats']['acceleration']}/{stats['tires_stats']['weight']}/{stats['tires_stats']['mini_turbo']}/{stats['tires_stats']['traction']} | "
            f"{'/'.join(map(str, stats['tires_stats']['speed']))} (Speed) | "
            f"{'/'.join(map(str, stats['tires_stats']['handling']))} (Handling)\n"
            f"-> Matching tires: {', '.join(stats['matching_tires'])}\n\n"
        )

        response += (
            f"- {glider}: {stats['glider_stats']['acceleration']}/{stats['glider_stats']['weight']}/{stats['glider_stats']['mini_turbo']}/{stats['glider_stats']['traction']} | "
            f"{'/'.join(map(str, stats['glider_stats']['speed']))} (Speed) | "
            f"{'/'.join(map(str, stats['glider_stats']['handling']))} (Handling)\n"
            f"-> Matching gliders: {', '.join(stats['matching_gliders'])}\n\n"
        )

        # Total Stats
        response += (
            "Total Stats:\n"
            f"- Speed: {'/'.join(map(str, stats['total_stats']['speed']))}\n"
            f"- Acceleration: {stats['total_stats']['acceleration']}\n"
            f"- Weight: {stats['total_stats']['weight']}\n"
            f"- Handling: {'/'.join(map(str, stats['total_stats']['handling']))}\n"
            f"- Traction: {stats['total_stats']['traction']}\n"
            f"- Mini-Turbo: {stats['total_stats']['mini_turbo']}"
        )

        await interaction.response.send_message(response)

    except ValueError as e:
        await interaction.response.send_message(str(e), ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
