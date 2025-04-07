import discord
from discord.ext import commands
import openai
import googletrans
import requests
import re
import pytesseract
from PIL import Image
import io
import smtplib
import os
import asyncio
from dotenv import load_dotenv
from email.mime.text import MIMEText
load_dotenv()


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

# openai.api_key = os.getenv("openai.api_key")
openai.api_key = OPENAI_API_KEY
# intents = discord.Intents.default()
# intents.messages = True
# intents.message_content = True
# bot = commands.Bot(command_prefix="/", intents=intents)

# # To-Do List storage (per user)
# todo_lists = {}

# # Translator
# translator = googletrans.Translator()

# # ----- Helper Functions -----

# # AI Assistant (ChatGPT-like response)
# async def ask_ai(question):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": question}]
#     )
#     return response.choices[0].message.content.strip()

# # Weather Information
# def get_weather(city):
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
#     response = requests.get(url).json()
#     if response.get("cod") != 200:
#         return "❌ City not found!"
#     weather = response["weather"][0]["description"].title()
#     temp = response["main"]["temp"]
#     return f"🌤 **Weather in {city}:** {weather}, {temp}°C"

# # News Fetcher
# def get_news(category="general"):
#     url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={NEWS_API_KEY}"
#     response = requests.get(url).json()
#     articles = response.get("articles", [])[:5]
#     if not articles:
#         return "❌ No news found!"
#     return "\n".join([f"📰 {article['title']} - {article['url']}" for article in articles])

# # Currency Converter
# def convert_currency(amount, from_currency, to_currency):
#     url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/{from_currency.upper()}"
#     response = requests.get(url).json()
#     rate = response.get("conversion_rates", {}).get(to_currency.upper())
#     if not rate:
#         return "❌ Invalid currency codes!"
#     converted = round(amount * rate, 2)
#     return f"💰 {amount} {from_currency.upper()} = {converted} {to_currency.upper()}"

# # OCR (Text Extraction from Image)
# def extract_text_from_image(image_data):
#     image = Image.open(io.BytesIO(image_data))
#     text = pytesseract.image_to_string(image)
#     return text.strip() if text else "❌ No readable text found!"

# # ----- Commands -----

# import asyncio
# import re

# def parse_natural_time(input_str):
#     """
#     Parses '1h30m', '2h15m10s', '45s', etc. into seconds.
#     Accepts optional leading 'me in', 'in', etc.
#     """
#     input_str = input_str.lower().strip()
    
#     # Remove "me in", "in", etc.
#     input_str = re.sub(r"^(me\s+)?in\s+", "", input_str)

#     # Match time chunks like 1h, 30m, 10s
#     matches = re.findall(r"(\d+)([hms])", input_str)
#     if not matches:
#         return None

#     seconds = 0
#     for value, unit in matches:
#         value = int(value)
#         if unit == 'h':
#             seconds += value * 3600
#         elif unit == 'm':
#             seconds += value * 60
#         elif unit == 's':
#             seconds += value
#     return seconds



# async def schedule_reminder(ctx, delay, message):
#     """Waits and then sends the reminder."""
#     try:
#         await asyncio.sleep(delay)
#         await ctx.send(f"🔔 <@{ctx.author.id}> Reminder: {message}")
#     except asyncio.CancelledError:
#         await ctx.send("❌ Reminder was cancelled.")
# @bot.command()
# async def remind(ctx, *, time_and_message: str):
#     """
#     Set a natural language reminder.
#     Examples:
#     /remind me in 1h30m Take a break
#     /remind in 45s check timer
#     /remind 10m
#     """
#     # Split the time from the message (everything before first word not containing h/m/s)
#     parts = time_and_message.strip().split()
    
#     # Find where time ends and message begins
#     time_expr = []
#     message = []

#     for part in parts:
#         if re.match(r"^\d+[hms]$", part.lower()):
#             time_expr.append(part)
#         else:
#             message.append(part)

#     if not time_expr:
#         # fallback: maybe time and message aren't cleanly split, parse from full string
#         seconds = parse_natural_time(time_and_message)
#         message_text = re.sub(r"(\d+[hms])+", "", time_and_message).strip()
#     else:
#         time_str = ''.join(time_expr)
#         seconds = parse_natural_time(time_str)
#         message_text = " ".join(message) if message else "Reminder!"

#     if not seconds:
#         await ctx.send("❌ Invalid time format. Try examples like:\n`1h30m`, `10m`, `45s`")
#         return

#     await ctx.send(f"⏰ Reminder set for **{time_str if time_expr else time_and_message.split()[0]}** from now.")
#     bot.loop.create_task(schedule_reminder(ctx, seconds, message_text))



# @bot.command()
# async def ask(ctx, *, question: str):
#     """Ask AI assistant any question"""
#     response = await ask_ai(question)
#     await ctx.send(f"🤖 **AI Assistant:** {response}")

# @bot.command()
# async def todo(ctx, action: str, *, item: str = None):
#     """Manage To-Do List: /todo add 'Task', /todo remove 'Task', /todo list"""
#     user_id = ctx.author.id
#     todo_lists.setdefault(user_id, [])

#     if action == "add" and item:
#         todo_lists[user_id].append(item)
#         await ctx.send(f"✅ Added: `{item}` to your To-Do List.")
#     elif action == "remove" and item:
#         if item in todo_lists[user_id]:
#             todo_lists[user_id].remove(item)
#             await ctx.send(f"❌ Removed: `{item}` from your To-Do List.")
#         else:
#             await ctx.send(f"⚠ `{item}` not found in your To-Do List.")
#     elif action == "list":
#         if not todo_lists[user_id]:
#             await ctx.send("📝 Your To-Do List is empty.")
#         else:
#             tasks = "\n".join([f"- {task}" for task in todo_lists[user_id]])
#             await ctx.send(f"📝 **Your To-Do List:**\n{tasks}")
#     else:
#         await ctx.send("❌ Invalid usage! Use `/todo add Task`, `/todo remove Task`, or `/todo list`.")
# @bot.command()
# async def translate(ctx, lang: str, *, text: str):
#     """Translate text using LibreTranslate (free, no API key required)"""
#     try:
#         url = "https://libretranslate.com/translate"
#         payload = {
#             "q": text,
#             "source": "auto",
#             "target": lang,
#             "format": "text"
#         }
#         headers = {"Content-Type": "application/json"}
#         response = requests.post(url, json=payload, headers=headers).json()

#         if "translatedText" in response:
#             await ctx.send(f"🌍 **Translation ({lang}):**\n{response['translatedText']}")
#         else:
#             await ctx.send(f"❌ Translation failed: {response}")
#     except Exception as e:
#         await ctx.send(f"❌ Translation failed! Error: {e}")



# @bot.command()
# async def weather(ctx, *, city: str):
#     """Get real-time weather info (e.g., /weather London)"""
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
#     response = requests.get(url).json()

#     if response.get("cod") != 200:
#         await ctx.send("❌ City not found! Please check the name and try again.")
#         return

#     weather_description = response["weather"][0]["description"].title()
#     temperature = response["main"]["temp"]
#     humidity = response["main"]["humidity"]
#     wind_speed = response["wind"]["speed"]

#     await ctx.send(f"🌤 **Weather in {city}:**\n"
#                    f"🌡 Temperature: {temperature}°C\n"
#                    f"💧 Humidity: {humidity}%\n"
#                    f"💨 Wind Speed: {wind_speed} m/s\n"
#                    f"☁ {weather_description}")



# @bot.command()
# async def news(ctx, category="general"):
#     """Fetch latest news headlines (e.g., /news tech)"""
#     valid_categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    
#     if category.lower() not in valid_categories:
#         await ctx.send(f"❌ Invalid category! Use one of: {', '.join(valid_categories)}")
#         return

#     url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={NEWS_API_KEY}"
#     response = requests.get(url).json()

#     if response.get("status") != "ok":
#         await ctx.send("❌ Error fetching news. Please try again later.")
#         return

#     articles = response.get("articles", [])[:5]
#     if not articles:
#         await ctx.send("❌ No news found for this category.")
#         return

#     news_summary = "\n".join([f"📰 {article['title']} - {article['url']}" for article in articles])
#     await ctx.send(f"🗞 **Latest {category.capitalize()} News:**\n{news_summary}")


# @bot.command()
# async def currency(ctx, amount: float, from_currency: str, to_currency: str):
#     """Convert currencies (e.g., /currency 10 USD EUR)"""
#     conversion = convert_currency(amount, from_currency, to_currency)
#     await ctx.send(conversion)

# @bot.command()
# async def ocr(ctx):
#     """Extract text from an uploaded image"""
#     if ctx.message.attachments:
#         image_url = ctx.message.attachments[0].url
#         image_data = requests.get(image_url).content
#         extracted_text = extract_text_from_image(image_data)
#         await ctx.send(f"📝 **Extracted Text:**\n{extracted_text}")
#     else:
#         await ctx.send("❌ Please upload an image with the command.")

# # Run the bot
# bot.run(DISCORD_TOKEN)
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# In-memory storage
todo_lists = {}
message_history = {}  # channel_id: list of recent messages
translator = googletrans.Translator()

# ----- Helper Functions -----

async def ask_ai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content.strip()

def send_sms_via_email(phone_number, carrier, message_text):
    # Define carrier gateways
    gateways = {
        "verizon": "vtext.com",
        "att": "txt.att.net",      # For AT&T
        "tmobile": "tmomail.net",
        "sprint": "messaging.sprintpcs.com",
    }
    
    # Check if carrier is supported
    if carrier.lower() not in gateways:
        raise ValueError("Carrier not supported. Available: verizon, att, tmobile, sprint.")
    
    recipient = f"{phone_number}@{gateways[carrier.lower()]}"
    
    # Email server configuration from environment variables
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    msg = MIMEText(message_text)
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Subject"] = ""  # SMS messages usually don't use a subject
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") != 200:
        return "❌ City not found!"
    weather = response["weather"][0]["description"].title()
    temp = response["main"]["temp"]
    return f"🌤 **Weather in {city}:** {weather}, {temp}°C"

def get_news(category="general"):
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])[:5]
    if not articles:
        return "❌ No news found!"
    return "\n".join([f"📰 {article['title']} - {article['url']}" for article in articles])

def convert_currency(amount, from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/{from_currency.upper()}"
    response = requests.get(url).json()
    rate = response.get("conversion_rates", {}).get(to_currency.upper())
    if not rate:
        return "❌ Invalid currency codes!"
    converted = round(amount * rate, 2)
    return f"💰 {amount} {from_currency.upper()} = {converted} {to_currency.upper()}"

def extract_text_from_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return text.strip() if text else "❌ No readable text found!"

def parse_natural_time(input_str):
    input_str = input_str.lower().strip()
    input_str = re.sub(r"^(me\s+)?in\s+", "", input_str)
    matches = re.findall(r"(\d+)([hms])", input_str)
    if not matches:
        return None
    seconds = 0
    for value, unit in matches:
        value = int(value)
        if unit == 'h':
            seconds += value * 3600
        elif unit == 'm':
            seconds += value * 60
        elif unit == 's':
            seconds += value
    return seconds

async def schedule_reminder(ctx, delay, message_text):
    try:
        await asyncio.sleep(delay)
        # Send reminder in Discord
        await ctx.send(f"🔔 <@{ctx.author.id}> Reminder: {message_text}")
        
        # Send SMS reminder using email-to-SMS gateway
        phone_number = os.getenv("RECIPIENT_PHONE_NUMBER")  # e.g., "1234567890"
        carrier = os.getenv("RECIPIENT_CARRIER")            # e.g., "att"
        send_sms_via_email(phone_number, carrier, f"Reminder: {message_text}")
    except asyncio.CancelledError:
        await ctx.send("❌ Reminder was cancelled.")


async def summarize_messages(channel):
    messages = "\n".join(message_history.get(channel.id, [])[-50:])
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Summarize the following conversation:"},
                      {"role": "user", "content": messages}]
        )
        summary = response.choices[0].message.content.strip()
        await channel.send(f"📌 **Summary:**\n{summary}")
        message_history[channel.id] = []
    except Exception as e:
        await channel.send(f"❌ Error generating summary: {e}")

async def generate_suggestion(channel):
    messages = "\n".join(message_history.get(channel.id, [])[-10:])
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Suggest a reply to the following messages:"},
                      {"role": "user", "content": messages}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {e}"

# ----- Event -----
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    ch_id = message.channel.id
    message_history.setdefault(ch_id, []).append(message.content)

    if len(message_history[ch_id]) >= 50:
        await summarize_messages(message.channel)

    if bot.user in message.mentions:
        suggestion = await generate_suggestion(message.channel)
        await message.channel.send(f"💬 **Suggested Reply:**\n{suggestion}")

    await bot.process_commands(message)

# ----- Commands -----

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
@bot.command()
async def remind(ctx, *, time_and_message: str):
    parts = time_and_message.strip().split()
    time_expr = []
    message = []
    for part in parts:
        if re.match(r"^\d+[hms]$", part.lower()):
            time_expr.append(part)
        else:
            message.append(part)
    if not time_expr:
        seconds = parse_natural_time(time_and_message)
        message_text = re.sub(r"(\d+[hms])+", "", time_and_message).strip()
    else:
        time_str = ''.join(time_expr)
        seconds = parse_natural_time(time_str)
        message_text = " ".join(message) if message else "Reminder!"
    if not seconds:
        await ctx.send("❌ Invalid time format.")
        return
    await ctx.send(f"⏰ Reminder set for **{time_str if time_expr else time_and_message.split()[0]}** from now.")
    bot.loop.create_task(schedule_reminder(ctx, seconds, message_text))

@bot.command()
async def ask(ctx, *, question: str):
    response = await ask_ai(question)
    await ctx.send(f"🤖 **AI Assistant:** {response}")

@bot.command()
async def todo(ctx, action: str, *, item: str = None):
    user_id = ctx.author.id
    todo_lists.setdefault(user_id, [])
    if action == "add" and item:
        todo_lists[user_id].append(item)
        await ctx.send(f"✅ Added: `{item}` to your To-Do List.")
    elif action == "remove" and item:
        if item in todo_lists[user_id]:
            todo_lists[user_id].remove(item)
            await ctx.send(f"❌ Removed: `{item}` from your To-Do List.")
        else:
            await ctx.send(f"⚠ `{item}` not found in your To-Do List.")
    elif action == "list":
        if not todo_lists[user_id]:
            await ctx.send("📝 Your To-Do List is empty.")
        else:
            tasks = "\n".join([f"- {task}" for task in todo_lists[user_id]])
            await ctx.send(f"📝 **Your To-Do List:**\n{tasks}")
    else:
        await ctx.send("❌ Invalid usage! Use `/todo add Task`, `/todo remove Task`, or `/todo list`.")

@bot.command()
async def translate(ctx, lang: str, *, text: str):
    try:
        url = "https://libretranslate.com/translate"
        payload = {"q": text, "source": "auto", "target": lang, "format": "text"}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers).json()
        if "translatedText" in response:
            await ctx.send(f"🌍 **Translation ({lang}):**\n{response['translatedText']}")
        else:
            await ctx.send(f"❌ Translation failed: {response}")
    except Exception as e:
        await ctx.send(f"❌ Translation failed! Error: {e}")

@bot.command()
async def weather(ctx, *, city: str):
    await ctx.send(get_weather(city))

@bot.command()
async def news(ctx, category="general"):
    valid_categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    if category.lower() not in valid_categories:
        await ctx.send(f"❌ Invalid category! Use one of: {', '.join(valid_categories)}")
        return
    await ctx.send(get_news(category))

@bot.command()
async def currency(ctx, amount: float, from_currency: str, to_currency: str):
    await ctx.send(convert_currency(amount, from_currency, to_currency))

@bot.command()
async def ocr(ctx):
    if ctx.message.attachments:
        image_url = ctx.message.attachments[0].url
        image_data = requests.get(image_url).content
        await ctx.send(f"📝 **Extracted Text:**\n{extract_text_from_image(image_data)}")
    else:
        await ctx.send("❌ Please upload an image with the command.")

@bot.command()
async def summarize(ctx):
    await summarize_messages(ctx.channel)

@bot.command()
async def suggest(ctx):
    suggestion = await generate_suggestion(ctx.channel)
    await ctx.send(f"💬 **Suggested Reply:**\n{suggestion}")

@bot.command()
async def summarize_image(ctx):
    """
    Summarizes the text in an uploaded image (such as a meme) using OCR and GPT.
    """
    if ctx.message.attachments:
        image_url = ctx.message.attachments[0].url
        # Get image data
        image_data = requests.get(image_url).content
        # Extract text from the image using OCR
        extracted_text = extract_text_from_image(image_data)
        
        if not extracted_text:
            await ctx.send("❌ No readable text found in the image.")
            return
        
        # Create a prompt for summarization
        prompt = f"Summarize the following text from a meme in a concise and fun way:\n\n{extracted_text}"
        summary = await ask_ai(prompt)
        await ctx.send(f"📝 **Summary:** {summary}")
    else:
        await ctx.send("❌ Please attach an image to summarize.")


@bot.command()
async def search(ctx, *, keyword: str):
    messages = message_history.get(ctx.channel.id, [])
    results = [m for m in messages if keyword.lower() in m.lower()]
    if results:
        await ctx.send("🔍 **Search Results:**\n" + "\n".join(results[-5:]))
    else:
        await ctx.send("🔍 No matching messages found.")
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! I'm alive.")
bot.run(DISCORD_TOKEN)
