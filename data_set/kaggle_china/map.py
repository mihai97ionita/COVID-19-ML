import pandas
import dateutil.parser

# formats date automatically, TODO may not be good

def to_date(value: str):
    return dateutil.parser.parse(value).date()


input = pandas.read_csv('input.csv')

our_columns = pandas.DataFrame(columns=['timestamp', 'cases', 'deaths', 'country'],
                               data=input[['update_time', 'confirmed_cases', 'deaths', 'country_code']].values)

our_columns['timestamp'] = our_columns['timestamp'].map(to_date)


# group by date and country
output = our_columns.groupby(['timestamp', 'country']).sum()

print(output)
output = output.sort_values(by='timestamp')
output.to_csv('dataset.csv')
