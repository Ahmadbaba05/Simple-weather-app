# ai_weather_assistant.py
# Favour Onu - AI Weather Assistant component

import os
import google.generativeai as genai


class AIWeatherAssistant:
    def __init__(self, api_key=None):
        # Prefer key from environment, fall back to the one passed in
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def _build_context(self, weather_data):
        """Turn the weather data into a short text the model can understand."""
        if not weather_data:
            return "No weather data available."

        lines = []
        if "city" in weather_data:
            lines.append(f"City: {weather_data['city']}")
        if "temp" in weather_data:
            lines.append(f"Temperature: {weather_data['temp']}°C")
        if "feels_like" in weather_data:
            lines.append(f"Feels like: {weather_data['feels_like']}°C")
        if "humidity" in weather_data:
            lines.append(f"Humidity: {weather_data['humidity']}%")
        if "wind_speed" in weather_data:
            lines.append(f"Wind speed: {weather_data['wind_speed']} m/s")
        if "description" in weather_data:
            lines.append(f"Condition: {weather_data['description']}")
        if "forecast" in weather_data:
            lines.append("5-day forecast:")
            for day in weather_data["forecast"]:
                lines.append(
                    f"  {day.get('date', '')}: "
                    f"{day.get('temp', '')}°C, {day.get('description', '')}"
                )

        return "\n".join(lines)

    def explain_weather(self, weather_data):
        """Give a plain-language summary of the current weather + forecast."""
        context = self._build_context(weather_data)

        prompt = (
            "You are a helpful weather assistant. "
            "Explain the following weather information in simple everyday language. "
            "Keep it short and easy to understand.\n\n"
            f"{context}"
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Sorry, I could not generate an explanation right now. ({e})"

    def answer_question(self, weather_data, question):
        """Answer a user question using the current weather data as context."""
        if not question or not question.strip():
            return "Please ask a weather-related question."

        context = self._build_context(weather_data)

        prompt = (
            "You are a friendly weather assistant. "
            "Use the weather data below to answer the user's question. "
            "If the question is not about weather, politely say so.\n\n"
            f"Weather data:\n{context}\n\n"
            f"User question: {question}"
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Sorry, I could not answer that right now. ({e})"
