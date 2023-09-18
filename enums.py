from enum import Enum


class IncomeTaxBorder(Enum):  # tuple[0]: border under in EUR, tuple[1]: income tax rate
    BORDER_19_PERCENT = (12450, 19)
    BORDER_24_PERCENT = (20200, 24)
    BORDER_30_PERCENT = (35200, 30)
    BORDER_37_PERCENT = (60000, 37)
    BORDER_45_PERCENT = (300000, 45)
    BORDER_47_PERCENT = (
        float("inf"),
        47,
    )  # Salary over 300 000 EUR annual is taxed 47%.


class Month(Enum):
    JAN = "January"
    FEB = "February"
    MAR = "March"
    APR = "April"
    MAY = "May"
    JUN = "June"
    JUL = "July"
    AUG = "August"
    SEP = "September"
    OCT = "October"
    NOV = "November"
    DEC = "December"


class Currency(Enum):
    EUR = "EUR"
    OTHER = "other currency"
