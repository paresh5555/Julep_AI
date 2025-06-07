🍽️ Foodie Tour Generator

A smart CLI app that generates a one-day foodie tour for multiple cities based on their weather, iconic local dishes, and top-rated restaurants. It uses intelligent agents (via Julep) and live weather data to recommend indoor/outdoor dining experiences and save results in a text file.

───────────────────────────────
🚀 FEATURES
───────────────────────────────

- ✅ Real-time weather-based indoor/outdoor dining suggestions
- 🍛 Local dish recommendations
- 🏆 Top-rated restaurants for each dish
- 📍 AI-generated one-day foodie itinerary
- 🔁 Works for multiple cities in parallel (async)
- 💾 Saves output to `output.txt`

───────────────────────────────
📦 DEPENDENCIES
───────────────────────────────

- Python 3.8+
- Julep SDK
- WeatherAPI
- python-dotenv

───────────────────────────────
🔐 ENVIRONMENT VARIABLES
───────────────────────────────

Create a `.env` file in the root directory and add:

JULEP_API_KEY=your_julep_api_key_here  
WEATHER_API_KEY=your_weatherapi_key_here

───────────────────────────────
🗂 FILE STRUCTURE
───────────────────────────────

.
├── main.py             → Main async script
├── tasks.yaml          → Julep task definitions
├── .env                → API keys (keep secret)
├── .gitignore          → Ignore .env/output.txt
├── output.txt          → Saved tour results
└── README.txt          → You're reading it!

───────────────────────────────
📋 HOW TO USE
───────────────────────────────

1. Install dependencies:
   pip install -r requirements.txt

2. Add your API keys to a `.env` file

3. Run the app:
   python main.py

4. Enter city names when prompted (e.g.):
   Mumbai, Delhi, Pune

5. View your foodie tours:
   - On-screen
   - In `output.txt`

───────────────────────────────
🛠 BUILT WITH
───────────────────────────────

- Julep Agents (OpenAI + Claude)
- WeatherAPI
- Python AsyncIO

───────────────────────────────
📄 LICENSE
───────────────────────────────

This project is licensed under the MIT License.

───────────────────────────────
✨ FUTURE IMPROVEMENTS
───────────────────────────────

- Deploy as a web app (Flask/Streamlit)
- Add voice input
- Vernacular language UX
- Offline-first support for rural use-cases

───────────────────────────────
MADE WITH ❤️ BY PARESH PATIL
───────────────────────────────
