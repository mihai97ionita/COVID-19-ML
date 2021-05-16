from datetime import datetime

import pandas
from pandas import DataFrame

dataset_name = "dataset_ageBased.csv"

input: DataFrame = pandas.read_csv('..///data_age_based.csv')

# having YearWeekISO as index (ordered)... cumulative sum for each ReportingCountry

essential = input[["country_code", "year_week", "age_group", "new_cases"]].copy()

# filter out <15yr
filtered = essential[essential["age_group"] != "<15yr"]

temp1 = filtered[filtered['age_group'] == "50-64yr"].copy()
temp2 = filtered[filtered['age_group'] == "65-79yr"].copy()
age_50_79 = pandas.concat([temp1, temp2])

temp1 = filtered[filtered['age_group'] != "50-64yr"].copy()
not_age_50_79 = temp1[temp1['age_group'] != "65-79yr"].copy()

keys_columns = ['year_week', 'country_code']
age_50_79_summed = age_50_79.groupby(keys_columns).sum()
age_50_79_summed["age_group"] = "50-79yr"

# hack :)
age_50_79_summed.to_csv(dataset_name)
age_50_79_summed: DataFrame = pandas.read_csv(dataset_name)

age_all = pandas.concat([not_age_50_79, age_50_79_summed])

print(age_all['age_group'].unique())


final = age_all
final.set_index("year_week", inplace=True)
final.to_csv(dataset_name)