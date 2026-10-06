# ai_assistant.py
# This is the AI Weather Assistant, it uses Google Gemini
# Favour 

try:
    from google import genai
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False


class AIWeatherAssistant:
    def __init__(self, api_key):
        self.enabled = False
        if api_key and GEMINI_AVAILABLE:
            self.enabled = True
            self.client = genai.Client(api_key=api_key)
            self.model_name = "gemini-3.8-flash"

    def explain_weather(self, city, forecast=None):
        if self.enabled == False:
            return "AI explanation is not available right now (no gemini key set)"

        prompt = "You are a friendly weather assistant. In 3-4 simple sentences, "
        prompt = prompt + "explain the current weather below to someone with no technical "
        prompt = prompt + "background, and suggest one practical tip.\n\n"
        prompt = prompt + "Data: " + city.summary()

        if forecast != None and len(forecast.days) > 0:
            prompt = prompt + "\nUpcoming days: "
            for d in forecast.days:
                prompt = prompt + d.date + ": " + d.condition + ", "
                prompt = prompt + str(round(d.temp_min)) + "-" + str(round(d.temp_max)) + "C; "

        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return "Sorry, could not generate explanation right now (" + str(e) + ")"

    def answer_question(self, city, question):
        if self.enabled == False:
            return "AI Q&A is not available right now (no gemini key set)"

        prompt = "Weather data for " + city.name + ": " + city.summary()
        prompt = prompt + "\n\nAnswer this question in 2-3 sentences using the data above: " + question

        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return "Sorry, could not answer that right now (" + str(e) + ")"
