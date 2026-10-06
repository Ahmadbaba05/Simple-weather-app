# theme.py
# simple light and dark theme switch for the app

import streamlit as st

THEMES = {
    "Light": {"bg": "#FFFFFF", "text": "#1A1A1A", "card": "#F2F4F7"},
    "Dark": {"bg": "#0E1117", "text": "#FAFAFA", "card": "#1E2430"},
}


class ThemeManager:
    def apply(theme_name):
        if theme_name in THEMES:
            theme = THEMES[theme_name]
        else:
            theme = THEMES["Light"]

        css = "<style>.stApp {background-color: " + theme["bg"] + "; color: " + theme["text"] + ";}"
        css = css + " .weather-card {background-color: " + theme["card"] + "; padding: 1.2rem; "
        css = css + "border-radius: 0.75rem; margin-bottom: 0.75rem;}</style>"
        st.markdown(css, unsafe_allow_html=True)
