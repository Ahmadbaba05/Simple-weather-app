# favourites.py
# This saves the favourite cities and search history into json files
# so we dont lose them when the app restarts
# Favour 

import os
import json
from datetime import datetime
import streamlit as st

FAVOURITES_FILE = "favourites.json"
HISTORY_FILE = "history.json"


class FavouritesManager:
    def __init__(self):
        self.favourites_path = FAVOURITES_FILE
        self.history_path = HISTORY_FILE

    def load_file(self, path):
        if os.path.exists(path) == False:
            return []
        try:
            f = open(path, "r")
            data = json.load(f)
            f.close()
            return data
        except:
            return []

    def save_file(self, path, items):
        try:
            f = open(path, "w")
            json.dump(items, f, indent=2)
            f.close()
        except Exception as e:
            st.warning("Could not save file: " + str(e))

    def get_favourites(self):
        return self.load_file(self.favourites_path)

    def add_favourite(self, city_name):
        favs = self.get_favourites()
        if city_name not in favs:
            favs.append(city_name)
            self.save_file(self.favourites_path, favs)

    def remove_favourite(self, city_name):
        favs = self.get_favourites()
        new_favs = []
        for c in favs:
            if c != city_name:
                new_favs.append(c)
        self.save_file(self.favourites_path, new_favs)

    def get_history(self):
        return self.load_file(self.history_path)

    def log_search(self, city_name):
        history = self.get_history()
        entry = {"city": city_name, "timestamp": str(datetime.now())[:16]}
        history.insert(0, entry)
        history = history[:50]
        self.save_file(self.history_path, history)
