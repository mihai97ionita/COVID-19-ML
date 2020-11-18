import dateutil.parser
import pandas
from country_converter import country_converter


def to_date(value: str):
    return dateutil.parser.parse(value).date()


def to_country_code(value: str) -> str:
    return country_converter.convert(names=value, to='ISO3', not_found='NOT_FOUND')


def match(country: str, un_formatted_country: str, province: str, code_country: dict) -> str:
    new_code = code_country[f'{country}']
    if new_code == 'NOT_FOUND':
        return f'NON_STANDARD_{un_formatted_country} {province}'
    else:
        return new_code


input = pandas.read_csv('input.csv')

our_columns = pandas.DataFrame(columns=['timestamp', 'cases', 'deaths', 'country', 'un_formatted_country', 'province'],
                               data=input[['Date', 'Confirmed', 'Deaths', 'Country/Region', 'Country/Region',
                                           'Province/State']].values)

our_columns['timestamp'] = our_columns['timestamp'].map(to_date)

# this operation is really expensive!!!!!
unique_countries = our_columns['country'].unique()
dict_code_country = {i: to_country_code(i) for i in unique_countries}
print(dict_code_country)
# GOD.. creating maps just for this :)..

new_countries = our_columns.apply(
    lambda input: match(input['country'], input['un_formatted_country'], input['province'],
                        dict_code_country), axis=1)

matched_countries = our_columns
matched_countries['country'] = new_countries

pre_output = matched_countries.drop(columns=['un_formatted_country', 'province'])

# group by date and country

NON_STANDARD_position = pre_output['country'].str.startswith('NON_STANDARD_')

filtered_pre_output = pre_output[~NON_STANDARD_position]
output = filtered_pre_output.groupby(['timestamp', 'country']).sum()
output.to_csv('dataset.csv')

left_pre_output = pre_output[NON_STANDARD_position].copy()
left_pre_output['country'] = left_pre_output['country'].map(lambda x: x.split("NON_STANDARD_", 1)[1])
output_left = left_pre_output.groupby(['timestamp', 'country']).sum()
output_left.to_csv('output_usa_left_overs.csv')
