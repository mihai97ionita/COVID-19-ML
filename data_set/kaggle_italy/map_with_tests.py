from datetime import datetime

import pandas


def to_date(value: str):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').date()


input = pandas.read_csv('input.csv')

our_columns = pandas.DataFrame(columns=['timestamp', 'cases', 'deaths', 'tests'],
                               data=input[['Date', 'NewPositiveCases', 'Deaths', 'TestsPerformed']].values)

our_columns['timestamp'] = our_columns['timestamp'].map(to_date)

our_columns = our_columns[~our_columns['tests'].isna()]

print(our_columns.head(5))
output = our_columns.groupby(['timestamp']).sum()

output = output.sort_values(by='timestamp')
initial_value = output.iloc[0]
output['deaths'] = output['deaths'].diff()
output['tests'] = output['tests'].diff()
output.iloc[0] = initial_value
output['country'] = 'ITA'
output.to_csv('dataset_with_tests.csv')
