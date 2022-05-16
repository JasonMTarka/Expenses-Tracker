from enum import Enum


class ComponentNames(Enum):
    NAME = "name"
    COST = "cost"
    DATE = "date"
    TAGS = "tags"
    CURRENCY = "currency"
    CREATE = "create_button"


class Lookup(Enum):
    NAME_FROM_ID = "name_from_id"
    ID_FROM_NAME = "id_From_name"


class Currencies(Enum):
    YEN = "Yen"
    DOLLARS = "Dollars"


DOLLAR_TO_YEN = 0.0077
