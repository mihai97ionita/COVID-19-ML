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


aged_based = age_all
aged_based.set_index("year_week", inplace=True)
aged_based.to_csv(dataset_name)

#####################################################

dataset_name = "vaccine.csv"

input: DataFrame = pandas.read_csv('..///data_vaccine_map///dataset_vaccine_v2.csv')



filtered = input[["YearWeekISO", "ReportingCountry", "TargetGroup", "TotalDosesSum" ]].copy()

temp1 = filtered[filtered['TargetGroup'] == "Age18_24"].copy()
temp2 = filtered[filtered['TargetGroup'] == "Age25_49"].copy()

sum_tmp1 = filtered[filtered['TargetGroup'] == "Age50_59"].copy()
sum_tmp2 = filtered[filtered['TargetGroup'] == "Age70_79"].copy()
age_50_79 = pandas.concat([sum_tmp1, sum_tmp2])

keys_columns = ['YearWeekISO', 'ReportingCountry']
temp3 = age_50_79.groupby(keys_columns).sum()
temp3["TargetGroup"] = "50-79yr"

# hack :)
temp3.to_csv(dataset_name)
temp3: DataFrame = pandas.read_csv(dataset_name)

temp4 = filtered[filtered['TargetGroup'] == "Age80+"].copy()


all = pandas.concat([temp1, temp2, temp3,temp4])
print(all['TargetGroup'].unique())

all['TargetGroup'] = all['TargetGroup'].map({'Age18_24': '15-24yr', 'Age25_49': '25-49yr', 'Age80+': '80+yr', '50-79yr': '50-79yr' })
replace = lambda x: x.replace("W", "")
all['YearWeekISO'] = all['YearWeekISO'].map(replace)



merged = pandas.merge(left=all, right=aged_based, left_on=['YearWeekISO','ReportingCountry', 'TargetGroup'], right_on=['year_week','country_code', 'age_group'])

all.set_index('YearWeekISO', inplace=True)
all.to_csv(dataset_name)

merged.set_index('YearWeekISO', inplace=True)
merged = merged.drop(columns=["country_code","age_group"])
merged.to_csv("vaccine_ageBased_merged.csv")
