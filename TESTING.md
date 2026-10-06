# Testing Plan - Real-Time Weather Information System

**Tester:** Mojeed Orunsolu (Group 4)

## Features to Test
| # | Feature | Test Action | Expected Result | Pass/Fail |
|---|---------|-------------|-----------------|-----------|
| 1 | City Search | Search "Lagos" | Current weather conditions displayed correctly | |
| 2 | Weather Details | Inspect search output | Temperature, feels-like, humidity, wind, condition, and icon shown | |
| 3 | 5-Day Forecast | Search "Abuja" | 5 daily min/max forecast cards displayed | |
| 4 | Favourites | Add/remove city & click favourite button | City persists across sessions in `favourites.json`; clicking button triggers search | |
| 5 | History | Search 3 cities | Last 50 searches stored in `history.json` and recent 5 displayed in sidebar | |
| 6 | Theme Switcher | Toggle Light/Dark mode | Application background and text styling update immediately | |
| 7 | AI Assistant | Ask "Do I need an umbrella?" | Plain-language answer generated using current weather context | |

## Error Cases
| # | Test Scenario / Input | Expected Result | Pass/Fail |
|---|-----------------------|-----------------|-----------|
| 1 | Empty city search | Rejection message: "City name must be 2-50 characters" | |
| 2 | Invalid characters ("12345", "@@@") | Rejection message via `InvalidCityNameError` | |
| 3 | Unknown city ("Xyzabcland") | Displays `CityNotFoundError`: "Could not find a city named..." | |
| 4 | Network/Offline state | Displays `WeatherAPIError`: Network connection failure | |
| 5a | Missing API key (not set) | Error message: "OPENWEATHER_API_KEY is not set" | |
| 5b | Wrong API key | Error message: "Something went wrong... unexpected status: 401" | |
| 6 | Missing Gemini Key / AI Failure | Core weather still loads; AI fallback message shown | |
| 7 | Corrupted `favourites.json` | App safely defaults to empty list without crashing | |
| 8 | Valid names with accents or dots ("São Paulo", "St. Louis") | Search accepted and weather shown | |
| 9 | Save same city twice | No duplicate in favourites | |

## Bug Reporting Workflow
Log bugs under the GitHub **Issues** tab including:
1. **Steps to Reproduce:** Exact inputs/actions taken.
2. **Expected Behavior:** What should have happened.
3. **Actual Result:** Error stack trace or unexpected visual state.
4. **Assignee:** Teammate responsible for that component (Ahmad, Divine, Favour, Nathan, or Daniel).
