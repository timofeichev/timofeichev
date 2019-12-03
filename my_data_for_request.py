import re
from datetime import datetime


def my_dep_and_dest_cities():
    departure_cities = ('AUH', 'DXB', 'ISB', 'JED', 'KHI', 'LHE', 'MED', 'MUX', 'PEW', 'UET', 'RUH', 'SHJ')
    arrival_cities = (
    'AUH', 'DMM', 'DXB', 'ISB', 'JED', 'KHI', 'LHE', 'MED', 'MUX', 'MCT', 'PEW', 'RYK', 'RUH', 'SHJ', 'SKT')
    my_dep_and_dest_cities = {}

    while True:
        dep_city = input('Please,enter your departure city:').strip()
        if dep_city in departure_cities:
            my_dep_and_dest_cities['departure_city'] = dep_city
            break
        else:
            print('Try again. Your departure city must be one of{}:'.format(departure_cities))

    while True:
        dest_city = input('Please,enter your destination city:').strip()
        if dest_city != dep_city and dest_city in arrival_cities:
            my_dep_and_dest_cities['destination_city'] = dest_city
            break
        else:
            print('Try again. Your destination city must be one of{}:'.format(arrival_cities))

    return my_dep_and_dest_cities


def my_dep_and_dest_dates():
    my_dep_and_dest_dates = {}

    while True:
        try:
            dep_date = input('Please,enter your departure date in (YYYY-MM-DD) format:').strip()
            match = re.search(r'^\d{4}\-\d{2}\-\d{2}$', dep_date)
            if match:
                dep_date_datetime = datetime.strptime(dep_date, '%Y-%m-%d')
                now_time = datetime.now()
                if dep_date_datetime > now_time:
                    my_dep_and_dest_dates['departure_date'] = dep_date
                    break
                else:
                    print('Try again.The date of departure you entered cannot be earlier than the current date')
            else:
                print('Try again.The date of departure you entered is incorrect format')
        except ValueError:
            print('Try again.Attention:MM values range from 1 to 12, DD values from 1 to 31')

    while True:
        try:
            dest_date = input(
                'Please,enter your destination date in (YYYY-MM-DD) format or enter nothing if it is not necessary:').strip()
            match = re.search(r'^\d{4}\-\d{2}\-\d{2}$', dest_date)
            if match:
                dest_date_datetime = datetime.strptime(dest_date, '%Y-%m-%d')
                if dep_date_datetime < dest_date_datetime:
                    my_dep_and_dest_dates['destination_date'] = dest_date
                    my_dep_and_dest_dates['type'] = 'RT'
                    break
                else:
                    print('Try again.The date of destination you entered cannot be earlier than the departure date')
            elif dest_date == '':
                my_dep_and_dest_dates['destination_date'] = dest_date
                my_dep_and_dest_dates['type'] = 'OW'
                break
            else:
                print('Try again.The date of destination you entered is incorrect format')
        except ValueError:
            print('Try again.Attention:MM values range from 1 to 12, DD values from 1 to 31')

    return my_dep_and_dest_dates


def my_data_for_request():
    my_data_for_request = my_dep_and_dest_cities()
    my_data_for_request.update(my_dep_and_dest_dates())

    return my_data_for_request


my_data_for_request = my_data_for_request()
