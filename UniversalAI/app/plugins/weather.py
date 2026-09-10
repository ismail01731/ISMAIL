from app.tools.weather import run

plugin = {
    "name": "weather",
    "description": "Weather Information",
    "capabilities": [
        "weather",
        "forecast",
        "temperature",
        "আবহাওয়া",
        "তাপমাত্রা",
        "বৃষ্টি"
    ],
    "run": run
}