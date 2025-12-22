import datetime
import calendar
import math
import random
import re
import sympy as sp
from requests import get
from bs4 import BeautifulSoup

def fetch_date() -> str:
    return str(datetime.datetime.now())

def maths(x: float, y: float, operation: str) -> float:
    SAFE_FUNCS = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt
    }

    if operation == "add":
        return x + y
    if operation == "subtract":
        return x - y
    if operation == "multiply":
        return x * y
    if operation == "divide":
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return x / y

    if operation in SAFE_FUNCS:
        return SAFE_FUNCS[operation](x)

    raise ValueError("Unsupported operation")
    
# auto insert * – example: 3x => 3*x
def add_mulsign(expression: str) -> str:
    return re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", expression)

# solve x=…
def solve_equation(equation: str, *variables: str) -> str:
    equation = add_mulsign(equation)
    equation = equation.replace("^", "**")
    
    if "=" in equation:
        equation = equation.replace("=", ",")

    symbols = sp.symbols(variables)

    left = sp.sympify(equation.split(',')[0])
    right = sp.sympify(equation.split(',')[1])

    eq = sp.Eq(left, right)
    solutions = sp.solve(eq, symbols)

    return (
        f"Solutions for {', '.join(variables)}:\n"
        f"{', '.join(str(sol) for sol in solutions)}\n"
        f"As float:\n{', '.join(str(float(sol)) for sol in solutions)}"
    )

# simplify expression
def simplify(expression: str) -> str:
    expression = add_mulsign(expression)
    expression = expression.replace("^", "**")

    simplified = sp.simplify(sp.sympify(expression))
    return f"Simplified expression:\n{str(simplified).replace('**', '^').replace('*', '')}"

def repeat(chars: str) -> str:
    return chars

def generate_rand(start: int, end: int) -> int:
    return random.randint(start, end)

def show_calender(year: int | None = None) -> str:
    if year is None:
        year = datetime.datetime.now().year
    return calendar.calendar(year)

def weather() -> str:
    url = "https://api.open-meteo.com/v1/forecast?latitude=51.50&longitude=-0.12&current_weather=true"
    response = get(url)
    data = response.json()
    current = data['current_weather']

    # A simplified map of WMO codes to human text
    # Source: https://open-meteo.com/en/docs
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Drizzle: Light", 53: "Drizzle: Moderate", 55: "Drizzle: Dense",
        61: "Rain: Slight", 63: "Rain: Moderate", 65: "Rain: Heavy",
        71: "Snow: Slight", 73: "Snow: Moderate", 75: "Snow: Heavy",
        80: "Rain showers: Slight", 81: "Rain showers: Moderate", 82: "Rain showers: Violent",
        95: "Thunderstorm: Slight or moderate",
        99: "Thunderstorm with heavy hail"
    }

    # Get the description, default to "Unknown" if code isn't in list
    condition = weather_codes.get(current['weathercode'], "Unknown")

    return (
        f"It is currently: {current['temperature']}°C "
        f"Condition:       {condition}"
    )

def get_news(url: str = "https://edition.cnn.com/") -> str:
    response = get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    span_data = soup.find_all("span", attrs={"class": "container__headline-text"})
    h_data = soup.find_all(["h1", "h2", "h3"])

    data = h_data + span_data

    news_to_return = ""

    for news in data:
        text = news.get_text("\n", True)

        if text:
            news_to_return += text
            news_to_return += "\n"

    return news_to_return
