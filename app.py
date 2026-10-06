# app.py
# Main streamlit app for the Real-Time Weather Information System
# Ahmad is building this (and weather_client.py too)
#
# Run with: streamlit run app.py
# Needs OPENWEATHER_API_KEY and GEMINI_API_KEY set as environment variables
# before you run the app (we do not put the keys in the code because we're uploading it as a repository on github)

import os
import streamlit as st

from weather_client import WeatherClient
from favourites import FavouritesManager
from theme import ThemeManager
from ai_assistant import AIWeatherAssistant
from models import InvalidCityNameError, CityNotFoundError, WeatherAPIError

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def init_session_state():
    if "theme" not in st.session_state:
        st.session_state.theme = "Light"
    if "last_city" not in st.session_state:
        st.session_state.last_city = None
    if "last_forecast" not in st.session_state:
        st.session_state.last_forecast = None


def render_sidebar(favourites_mgr):
    st.sidebar.title("Settings")

    theme_choice = st.sidebar.radio("Theme", ["Light", "Dark"])
    st.session_state.theme = theme_choice

    st.sidebar.markdown("### Favourite Cities")
    favs = favourites_mgr.get_favourites()
    if len(favs) == 0:
        st.sidebar.caption("No favourites saved yet.")
    for fav_city in favs:
        col1, col2 = st.sidebar.columns([3, 1])
        if col1.button(fav_city, key="fav_" + fav_city):
            st.session_state.search_trigger = fav_city
        if col2.button("x", key="remove_" + fav_city):
            favourites_mgr.remove_favourite(fav_city)
            st.rerun()

    st.sidebar.markdown("### Recent Searches")
    history = favourites_mgr.get_history()
    count = 0
    for item in history:
        if count >= 5:
            break
        st.sidebar.caption(item["city"] + " - " + item["timestamp"])
        count = count + 1


def render_current_weather(city):
    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(city.icon_url(), width=80)
    with col2:
        st.subheader(city.name + ", " + city.country)
        st.write(str(round(city.temperature, 1)) + " C - " + city.condition)
        st.caption("Feels like " + str(round(city.feels_like, 1)) + " C")

    m1, m2 = st.columns(2)
    m1.metric("Humidity", str(city.humidity) + "%")
    m2.metric("Wind Speed", str(city.wind_speed) + " m/s")
    st.markdown('</div>', unsafe_allow_html=True)


def render_forecast(forecast):
    st.markdown("#### 5-Day Forecast")
    if len(forecast.days) == 0:
        return
    cols = st.columns(len(forecast.days))
    i = 0
    for day in forecast.days:
        with cols[i]:
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            st.caption(day.date)
            st.image("https://openweathermap.org/img/wn/" + day.icon_code + ".png", width=50)
            st.write(str(round(day.temp_min)) + " / " + str(round(day.temp_max)) + " C")
            st.caption(day.condition)
            st.markdown('</div>', unsafe_allow_html=True)
        i = i + 1


def main():
    st.set_page_config(page_title="Real-Time Weather Information System", layout="wide")
    init_session_state()
    ThemeManager.apply(st.session_state.theme)

    weather_client = WeatherClient(OPENWEATHER_API_KEY)
    favourites_mgr = FavouritesManager()
    ai_assistant = AIWeatherAssistant(GEMINI_API_KEY)

    render_sidebar(favourites_mgr)

    st.title("Real-Time Weather Information System")
    st.caption("Search any city for live weather, a 5-day forecast, and an AI explanation.")

    default_value = st.session_state.pop("search_trigger", "")
    search_input = st.text_input("Enter a city name", value=default_value)
    search_clicked = st.button("Search")

    if search_clicked or default_value:
        if OPENWEATHER_API_KEY == "":
            st.error("OPENWEATHER_API_KEY is not set. Please set it before running the app.")
            return

        try:
            city = weather_client.get_current_weather(search_input)
            forecast = weather_client.get_forecast(search_input)

            st.session_state.last_city = city
            st.session_state.last_forecast = forecast
            favourites_mgr.log_search(city.name)

        except InvalidCityNameError as e:
            st.error("Invalid input: " + str(e))
        except CityNotFoundError as e:
            st.error(str(e))
        except WeatherAPIError as e:
            st.error("Something went wrong: " + str(e))

    city = st.session_state.last_city
    forecast = st.session_state.last_forecast

    if city != None:
        render_current_weather(city)

        if st.button("Save " + city.name + " to favourites"):
            favourites_mgr.add_favourite(city.name)
            st.success(city.name + " added to favourites!")

        if forecast != None:
            render_forecast(forecast)

        st.markdown("#### AI Weather Assistant")
        with st.spinner("Generating explanation..."):
            explanation = ai_assistant.explain_weather(city, forecast)
        st.info(explanation)

        question = st.text_input("Ask the AI assistant a question about this weather")
        if st.button("Ask") and question:
            with st.spinner("Thinking..."):
                answer = ai_assistant.answer_question(city, question)
            st.write(answer)
    else:
        st.info("Search for a city above to get started.")


if __name__ == "__main__":
    main()
