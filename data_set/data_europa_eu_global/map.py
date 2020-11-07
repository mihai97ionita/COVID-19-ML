from datetime import datetime

import pandas


def to_date(value: str):
    return datetime.strptime(value, '%d/%m/%Y').date()


input = pandas.read_csv('input.csv')

our_columns = pandas.DataFrame(columns=['timestamp', 'cases', 'deaths', 'country'],
                               data=input[['dateRep', 'cases', 'deaths', 'countryterritoryCode']].values)

our_columns['timestamp'] = our_columns['timestamp'].map(to_date)

# fix Taiwan code
our_columns['country'] = our_columns['country'].replace('CNG1925', 'TWN')

# group by date and country
output = our_columns.groupby(['timestamp', 'country']).sum()

print(output)

output.to_csv('output_eu_global.csv')
