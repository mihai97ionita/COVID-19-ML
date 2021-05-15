from datetime import datetime

import pandas
from pandas import DataFrame

dataset_name_icu = "dataset_total_icu.csv"
dataset_name_hospital = "dataset_total_hospital.csv"
dataset_name_admissions_hospital = "dataset_admissions_hospital_100k.csv"
dataset_name_admissions_icu = "dataset_admissions_icu_100k.csv"

input: DataFrame = pandas.read_csv('..///data_hospital.csv')

print(input["indicator"].unique())

# only ALL TargetGroup
filtered_icu = input[input["indicator"] == "Daily ICU occupancy"]
filtered_hospital = input[input["indicator"] == "Daily hospital occupancy"]
filtered_hospital_admissions = input[input["indicator"] == "Weekly new hospital admissions per 100k"]
filtered_icu_admissions = input[input["indicator"] == "Weekly new ICU admissions per 100k"]

key_columns = ['year_week', 'country']

# having YearWeekISO as index (ordered)... cumulative sum for each ReportingCountry
filtered_icu["WeekValue"] = filtered_icu.groupby(key_columns)["value"].cumsum()
filtered_hospital["WeekValue"] = filtered_hospital.groupby(key_columns)["value"].cumsum()
filtered_hospital_admissions["WeekValue"] = filtered_hospital_admissions.groupby(key_columns)["value"].cumsum()
filtered_icu_admissions["WeekValue"] = filtered_icu_admissions.groupby(key_columns)["value"].cumsum()

final_merge_icu = filtered_icu[["year_week","country", "WeekValue"]].copy()
icu_values = final_merge_icu.groupby(key_columns).tail(1)
icu_values.set_index('year_week', inplace=True)
icu_values.to_csv(dataset_name_icu)

final_merge_hospital = filtered_hospital[["year_week","country", "WeekValue"]].copy()
hospital_values = final_merge_hospital.groupby(key_columns).tail(1)
hospital_values.set_index('year_week', inplace=True)
hospital_values.to_csv(dataset_name_hospital)

final_merge_hospital_admissions = filtered_hospital_admissions[["year_week","country", "WeekValue"]].copy()
hospital_admissions_values = final_merge_hospital_admissions.groupby(key_columns).tail(1)
hospital_admissions_values.set_index('year_week', inplace=True)
hospital_admissions_values.to_csv(dataset_name_admissions_hospital)

final_merge_icu_admissions = filtered_icu_admissions[["year_week","country", "WeekValue"]].copy()
icu_admissions_values = final_merge_icu_admissions.groupby(key_columns).tail(1)
icu_admissions_values.set_index('year_week', inplace=True)
icu_admissions_values.to_csv(dataset_name_admissions_icu)
