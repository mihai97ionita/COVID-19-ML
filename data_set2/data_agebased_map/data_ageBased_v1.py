from datetime import datetime

import pandas
from pandas import DataFrame

dataset_name = "dataset_ageBased.csv"

input: DataFrame = pandas.read_csv('..///data_age_based.csv')

# having YearWeekISO as index (ordered)... cumulative sum for each ReportingCountry

final = input[["country_code","year_week", "age_group", "new_cases"]].copy()
final.set_index('year_week', inplace=True)
final.to_csv(dataset_name)

print(final["age_group"].unique())