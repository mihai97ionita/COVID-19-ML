from datetime import datetime
import pandas


def to_date(value: str):
    return datetime.strptime(value, '%Y-%m-%d').date()


# def to_country_code(value: str) -> str:
#     return country_converter.convert(names=value, to='ISO3', not_found='NOT_FOUND')


# def match(country: str, un_formatted_country: str, province: str, code_country: dict) -> str:
#     new_code = code_country[f'{country}']
#     if new_code == 'NOT_FOUND':
#         return f'NON_STANDARD_{un_formatted_country} {province}'
#     else:
#         return new_code


input = pandas.read_csv('input.csv')

our_columns = pandas.DataFrame(columns=['timestamp', 'cases', 'deaths', 'country'],
                               data=input[['Date', 'Confirmed', 'Deaths', 'Country/Region']].values)

our_columns['timestamp'] = our_columns['timestamp'].map(to_date)

# group by date and country
output = our_columns.groupby(['timestamp', 'country']).sum()

print(output)

output.to_csv('output_usa2.csv')
