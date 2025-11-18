# ================================
# IMPORTS
# ================================
import os
import requests
import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


# ================================
# GEMINI CLIENT SETUP
# ================================
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API key missing in .env")

client = genai.Client(api_key=api_key)



# ================================
# WEATHER (Actual API Call)
# ================================
def get_weather(city: str):
    try:
        api_key = os.getenv("OPENWEATHER_API")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        return response.json()
    except:
        return {"error": "Failed to fetch weather"}



# ================================
# WEATHER → NATURAL LANGUAGE SUMMARY
# ================================
def temperature_of_city(city):
    weather_data = get_weather(city)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Convert this weather JSON into a clean simple report.

        JSON:
        {weather_data}

        Include:
        - Temperature (°C)
        - Feels like
        - Humidity
        - Wind speed
        - Sunrise & sunset
        - Clothing suggestion
        """
    )

    return response.text



# ================================
# NEWS + SUMMARIZER
# ================================
def get_news(topic: str):
    try:
        key = os.getenv("NEWS_API")
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={key}&pageSize=5&sortBy=publishedAt"
        return requests.get(url).json().get("articles", [])
    except:
        return []


def news_summarizer(url: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Summarize this news: {url}. Keep it short and clean."
    )
    return response.text



# ================================
# FORECAST (Google Search API → via Gemini)
# ================================
def get_forcasted_weather(city: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Search the internet and give me:

        1. Today's weather forecast for {city}
        2. Best places to visit in {city} today

        Keep it clean.
        """,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )

    return response.text



# ================================
# EVENTS (SerpAPI)
# ================================
def find_local_events(city: str):
    try:
        api = os.getenv("SERP_API")
        url = f"https://serpapi.com/search.json?engine=google_events&q=Events in {city}&api_key={api}"
        return requests.get(url).json()
    except:
        return {"events": []}



# ================================
# SMART PLANNER (NO TOOL HANDLERS)
# ================================
def smart_plan(city):

    forecast = get_forcasted_weather(city)
    events = find_local_events(city)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Create a smart day plan for {city} using:

        WEATHER FORECAST:
        {forecast}

        EVENTS:
        {events}

        RULES:
        - Morning → Afternoon → Evening
        - Recommend events with timings + links
        - Suggest places to visit
        - Suggest lunch/dinner time
        - Keep tone friendly & helpful
        """
    )

    return response.text
