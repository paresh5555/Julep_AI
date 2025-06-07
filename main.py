import time
import requests
import yaml
from julep import Julep
from dotenv import load_dotenv
import os
import asyncio


# === CONFIG ===
load_dotenv()

JULEP_API_KEY = os.getenv("JULEP_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
# CITIES = ["Mumbai", "New Delhi", "Bangalore", "Nandurbar"]

# Load task definitions
with open("tasks.yaml", "r") as file:
    tasks = yaml.safe_load(file)

client = Julep(api_key=JULEP_API_KEY)

# === AGENTS ===
weather_agent = client.agents.create(
    name="Weather Advisor",
    model="gpt-4o",
    about="Suggests indoor or outdoor dining based on weather"
)

food_agent = client.agents.create(
    name="Dish Picker",
    model="gpt-4o",
    about="Selects 3 iconic local dishes for a given city"
)

restaurant_agent = client.agents.create(
    name="Restaurant Recommender",
    model="gpt-4o",
    about="Finds top-rated restaurants for given dishes in that particular city"
)

tour_agent = client.agents.create(
    name="Foodie Tour Creator",
    model="claude-3.5-sonnet",
    about="Crafts a delightful one-day foodie tour using the food and city inputs"
)

# === HELPERS ===
def fetch_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    response = requests.get(url).json()

    # Check if API returned an error
    if 'error' in response:
        print(f"❌ Weather API error for {city}: {response['error']['message']}")
        return None

    try:
        return {
            "city": city,
            "temp_c": response['current']['temp_c'],
            "rain_chance": response['current'].get('precip_mm', 0),
            "weather_desc": response['current']['condition']['text']
        }
    except KeyError:
        print(f"❌ Unexpected response format for city: {city}")
        print(response)
        return None

def run_task(agent_id, task_def, input_data):
    task = client.tasks.create(agent_id=agent_id, **task_def)
    execution = client.executions.create(task_id=task.id, input=input_data)

    last_status = None
    while True:
        result = client.executions.get(execution.id)
        if result.status != last_status:
            print(f"⏳ Status: {result.status}")
            last_status = result.status
        if result.status in ['succeeded', 'failed']:
            break
        time.sleep(1)

    if result.status == "succeeded":
        return result.output['choices'][0]['message']['content']
    else:
        print(f"❌ Error: {result.error}")
        return None


city_input = input("Enter cities separated by commas (e.g., Mumbai, Delhi, Pune): ")
CITIES = [city.strip() for city in city_input.split(",")]

# === MAIN EXECUTION FLOW ===

for city in CITIES:
    print(f"\n🌆 Generating foodie tour for {city}...")

    # Step 1: Weather
    weather_data = fetch_weather(city)
    if not weather_data:
        print(f"⚠️ Skipping {city} due to weather data error.\n")
        continue

    weather_type = run_task(weather_agent.id, tasks['weather_task'], weather_data)

    # 🔧 Print temperature and indoor/outdoor choice
    print(f"🌡️ Temperature in {city}: {weather_data['temp_c']}°C")
    print(f"🏠 Based on weather, we recommend an **{weather_type.strip().lower()}** dining experience.")

    # Step 2: Dishes
    dishes_response = run_task(food_agent.id, tasks["food_task"], {"city": city})
    dish_list = [line.strip("1234567890). ").strip() for line in dishes_response.split("\n") if line.strip()]
    dishes_str = ", ".join(dish_list[:3])

    # Step 3: Restaurants
    restaurant_info = run_task(restaurant_agent.id, tasks["restaurant_task"], {
        "city": city,
        "dishes_str": dishes_str
    })

    # Step 4: Tour Narrative
    tour_narrative = run_task(tour_agent.id, tasks["tour_task"], {
        "city": city,
        "weather_type": weather_type,
        "dishes_str": dishes_str,
        "restaurants": restaurant_info
    })

    print(f"\n🍽️ Foodie Tour for {city}:\n{tour_narrative}")

    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(f"\n🌆 City: {city}\n")
        f.write(f"🌡️ Temperature: {weather_data['temp_c']}°C\n")
        f.write(f"🏠 Recommended: {weather_type.strip().lower()} dining experience\n\n")
        f.write(f"🍽️ Foodie Tour for {city}:\n{tour_narrative}\n")
        f.write("=" * 60 + "\n")



# async def process_city(city):
#     print(f"\n🌆 Generating foodie tour for {city}...")
#
#     # Step 1: Weather
#     weather_data = await asyncio.to_thread(fetch_weather, city)
#     if not weather_data:
#         print(f"⚠️ Skipping {city} due to weather data error.\n")
#         return
#
#     weather_type = await asyncio.to_thread(run_task, weather_agent.id, tasks['weather_task'], weather_data)
#
#     print(f"🌡️ Temperature in {city}: {weather_data['temp_c']}°C")
#     print(f"🏠 Based on weather, we recommend an **{weather_type.strip().lower()}** dining experience.")
#
#     # Step 2: Dishes
#     dishes_response = await asyncio.to_thread(run_task, food_agent.id, tasks["food_task"], {"city": city})
#     dish_list = [line.strip("1234567890). ").strip() for line in dishes_response.split("\n") if line.strip()]
#     dishes_str = ", ".join(dish_list[:3])
#
#     # Step 3: Restaurants
#     restaurant_info = await asyncio.to_thread(run_task, restaurant_agent.id, tasks["restaurant_task"], {
#         "city": city,
#         "dishes_str": dishes_str
#     })
#
#     # Step 4: Tour Narrative
#     tour_narrative = await asyncio.to_thread(run_task, tour_agent.id, tasks["tour_task"], {
#         "city": city,
#         "weather_type": weather_type,
#         "dishes_str": dishes_str,
#         "restaurants": restaurant_info
#     })
#
#     print(f"\n🍽️ Foodie Tour for {city}:\n{tour_narrative}")
# async def main():
#     tasks_list = [process_city(city) for city in CITIES]
#     await asyncio.gather(*tasks_list)
#
# # Run the event loop
# asyncio.run(main())
#
