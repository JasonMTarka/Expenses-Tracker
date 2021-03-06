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

DOLLAR_TO_YEN = 0.0077
