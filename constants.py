from enum import Enum


class ComponentNames(Enum):
    NAME = "name"
    COST = "cost"
    DATE = "date"
    TAGS = "tags"
    CURRENCY = "currency"
    CREATE = "create_button"


class Currencies(Enum):
    YEN = "Yen"
    DOLLARS = "Dollars"


TAG_NAMES = [
    "Groceries",
    "Dining",
    "Household",
    "Jason",
    "Xiaochen",
    "Social",
    "Travel",
    "Games",
    "Alcohol",
    "Big Purchases",
    "Bento",
    "Car",
    "Clothing",
    "Uber Eats",
]

DOLLAR_TO_YEN = 0.0077
