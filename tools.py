import datetime
import calendar
import math
import random
import re

def fetch_date() -> str:
    return str(datetime.datetime.now())

def maths(x: float, y: float, operation: str) -> float:
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation == "multiply":
        return x * y
    elif operation == "divide":
        return x / y
    # For math functions like sin, cos, sqrt
    elif operation.startswith("math."):
        return eval(f"{operation}({x})")  # only apply to x
    else:
        raise ValueError("Unsupported operation")


def generate_rand(end: int, start: int = 0) -> int:
    return random.randint(start, end)

def show_calender(year: int | None = None) -> str:
    if year is None:
        year = datetime.datetime.now().year
    return calendar.calendar(year)
