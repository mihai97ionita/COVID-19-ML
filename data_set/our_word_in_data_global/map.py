from datetime import datetime

import pandas


def to_date(value: str):
    return datetime.strptime(value, '%Y-%m-%d').date()

def to_int(value):
    try:
        return int(value)
    except:
        return value

input = pandas.read_csv('input.csv')

our_columns = pandas.DataFrame(columns=['timestamp', 'cases', 'deaths', 'country'],
                               data=input[['date', 'new_cases', 'new_deaths', 'iso_code']].values)

our_columns['timestamp'] = our_columns['timestamp'].map(to_date)

output = our_columns.groupby(['timestamp', 'country']).sum()

print(output)

output.to_csv('output_world_global.csv')
