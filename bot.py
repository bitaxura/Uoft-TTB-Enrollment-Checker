import os
import ast
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from api_bot import get_course_data

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

all_courses = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    check_courses.start()

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def add(ctx, *, text: str):
    try:
        data = ast.literal_eval(text)
    except Exception as e:
        await ctx.send("Error adding course please fix format")
        return
    
    data['user_id'] = str(ctx.author.id)
    all_courses.append(data)

    await ctx.send("Added course")

@bot.command()
async def delete(ctx, *, number: int):
    user_entries = [e for e in all_courses if e['user_id'] == str(ctx.author.id)]
    if not user_entries:
        await ctx.send("You have no entries.")
        return

    if number < 1 or number > len(user_entries):
        await ctx.send("Invalid entry number.")
        return
    
    to_delete = user_entries[number - 1]
    all_courses.remove(to_delete)
    await ctx.send(f"Deleted course: {to_delete}")

@bot.command()
async def myentries(ctx):
    user_entries = [e for e in all_courses if e['user_id'] == str(ctx.author.id)]

    if not user_entries:
        await ctx.send("You have no entries.")
        return
    
    message_lines = ["Your Entries: "]
    for i, entry in enumerate(user_entries, 1):
        message_lines.append(f"{i}. {entry}")

    await ctx.send("\n".join(message_lines))

@tasks.loop(hours=6)
async def check_courses():
    await check_courses_logic()

async def check_courses_logic():
    if not all_courses:
        return
    open_courses = await get_course_data(all_courses)
    if open_courses:
        channel = bot.get_channel(int(CHANNEL_ID))
        await channel.send("\n".join(open_courses))

@bot.command()
async def run_api(ctx):
    await check_courses_logic()
    await ctx.send("API check started.")

bot.run(TOKEN)