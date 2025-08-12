import os
import ast
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from api_bot import get_course_data, add_user_entry, delete_user_entry, get_user_entries, get_all_courses

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    check_courses.start()

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def add(ctx, *, course_json: str):
    user_id = str(ctx.author.id)
    course_dict = ast.literal_eval(course_json)
    course_dict['user_id'] = user_id

    add_user_entry(user_id, course_dict)
    
    await ctx.send(f"Added course: {course_dict.get('course_code', 'unknown')}")

@bot.command()
async def delete(ctx, *, number: int):
    user_id = str(ctx.author.id)
    entries = get_user_entries(user_id)

    if not entries:
        await ctx.send("You have no entries.")
        return

    if number < 1 or number > len(entries):
        await ctx.send("Invalid entry number.")
        return

    entry_to_delete = entries[number - 1]
    delete_user_entry(entry_to_delete['id'])
    await ctx.send(f"Deleted course: {entry_to_delete['course']}")

@bot.command()
async def myentries(ctx):
    user_id = str(ctx.author.id)
    entries = get_user_entries(user_id)

    if not entries:
        await ctx.send("You have no entries.")
        return

    message_lines = ["Your Entries:"]
    for i, entry in enumerate(entries, 1):
        message_lines.append(f"{i}. {entry['course']}")

    await ctx.send("\n".join(message_lines))

@tasks.loop(hours=8)
async def check_courses():
    await check_courses_logic()

async def check_courses_logic():
    all_courses = get_all_courses()
    if not all_courses:
        return
    open_courses = await get_course_data(all_courses)
    if open_courses:
        channel = bot.get_channel(int(CHANNEL_ID))
        await channel.send("\n".join(open_courses))

@bot.command()
@commands.has_permissions(administrator=True)
async def run_api(ctx):
    await check_courses_logic()
    await ctx.send("API check started.")

bot.run(TOKEN)
