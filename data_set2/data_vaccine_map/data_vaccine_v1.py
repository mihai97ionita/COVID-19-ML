from datetime import datetime

import pandas
from pandas import DataFrame


input: DataFrame = pandas.read_csv('..///data_vaccine.csv')

# only ALL TargetGroup
filtered = input[input["TargetGroup"] == "ALL"]

# todo do we want so sum all regions?.. if so remove 'Region' from below
keys_columns = ['YearWeekISO', 'Region', 'ReportingCountry']
grouped_by_time_location: DataFrame = filtered.groupby(keys_columns)

columns_to_group_by = ["FirstDose", "FirstDoseRefused", "SecondDose", "UnknownDose"]
summed_all_vac_types: DataFrame = grouped_by_time_location[columns_to_group_by].sum()


columns_to_keep = ["Population", "Denominator"]
# pick one of multiples values (should be the same..)
values: DataFrame = grouped_by_time_location[columns_to_keep].max()

# select FirstDose, SecondDose, UnknownDose then axis 1 will sum all values in the each row and place them in a new column
summed_all_vac_types["TotalDoses"] = summed_all_vac_types[["FirstDose", "SecondDose", "UnknownDose"]].sum(axis=1)

# merge sum operations with values using keys_columns as keys to merge by
output = pandas.merge(left=summed_all_vac_types, right=values, on=keys_columns)

output.to_csv('dataset.csv')
