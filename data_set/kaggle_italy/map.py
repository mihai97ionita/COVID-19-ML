from datetime import datetime

import pandas


def to_date(value: str):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').date()


input = pandas.read_csv('input.csv')

our_columns = pandas.DataFrame(columns=['timestamp', 'cases', 'deaths'],
                               data=input[['Date', 'NewPositiveCases', 'Deaths']].values)

our_columns['timestamp'] = our_columns['timestamp'].map(to_date)

output = our_columns.groupby(['timestamp']).sum()
output['country'] = 'ITA'
output.to_csv('output_IT.csv')
