from datetime import datetime

import pandas
from pandas import DataFrame


input: DataFrame = pandas.read_csv('..///data_vaccine.csv')

# only ALL TargetGroup
filtered_temp = input[input["TargetGroup"] == "ALL"]
# only Region as Country
filtered = filtered_temp[filtered_temp["Region"] == filtered_temp["ReportingCountry"]]

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
merged = pandas.merge(left=summed_all_vac_types, right=values, on=keys_columns)

# write tmp dataset for some reason
dataset_name = 'dataset_vaccine_and_testing.csv'
merged.to_csv(dataset_name)

# index by YearWeekISO
merged: DataFrame = pandas.read_csv(dataset_name)

# only keep the essential columns
essential = merged[["YearWeekISO","ReportingCountry", "TotalDoses"]].copy()

# having YearWeekISO as index (ordered)... cumulative sum for each ReportingCountry
essential["TotalDosesSum"] = essential.groupby(['ReportingCountry'])["TotalDoses"].cumsum()

# read data regrading tests
data_testing = pandas.read_csv('..///data_testing.csv')

# keep essential
testing_essentials = data_testing[["year_week", "country_code", "positivity_rate"]].copy()

# merge vaccine and tests
final_merge = pandas.merge(left=essential, right=testing_essentials, left_on=['YearWeekISO','ReportingCountry'], right_on=['year_week','country_code'])

# remove duplicates columns
final_merge = final_merge[["YearWeekISO","ReportingCountry", "TotalDosesSum", "positivity_rate"]].copy()

# set index to date
final_merge.set_index('YearWeekISO', inplace=True)

# you can read it yourself :)
final_merge.to_csv(dataset_name)