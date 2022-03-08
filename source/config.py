import pandas as pd

DATA_PATH = [
    "C:/Users/Viabl/Correlation Time Series Anaylsis/data/electricity.csv",
    "C:/Users/Viabl/Correlation Time Series Anaylsis/data/HOUST.csv",
    "C:/Users/Viabl/Correlation Time Series Anaylsis/data/unemployment.csv",
    "C:/Users/Viabl/Correlation Time Series Anaylsis/data/NASDAQ.csv",
    "C:/Users/Viabl/Correlation Time Series Anaylsis/data/DOW.csv",
    #"C:/Users/Viabl/Correlation Time Series Anaylsis/data/GDP.csv",
    "C:/Users/Viabl/Correlation Time Series Anaylsis/data/WTI.csv"
]

PUBLIC_COLUMN = [
    "DOW Close",
    "NASDAQ Close",
    #"GDP"
    "WTI"
]

PRIVATE_COLUMN = [
    "Unemployment rate",
    "Electricity Price",
    "Total Housing Units Started"
]

PERIOD_DICTIONARY = {
    "Unemployment rate": None,
    "DOW Close": None,
    "Electricity Price": 12,
    #"GDP": None,
    "WTI": None,
    "Total Housing Units Started": None,
    "NASDAQ Close": None
}

START_DATE = pd.to_datetime("2010-11", format='%Y-%m')

BOUND_FACTOR = .75