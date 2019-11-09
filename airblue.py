import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def my_dep_and_dest_cities():
    departure_cities = ('AUH', 'DXB', 'ISB', 'JED', 'KHI', 'LHE', 'MED', 'MUX', 'PEW', 'UET', 'RUH', 'SHJ')
    arrival_cities = ('AUH', 'DMM', 'DXB', 'ISB', 'JED', 'KHI', 'LHE', 'MED', 'MUX', 'MCT', 'PEW', 'RYK',
                      'RUH', 'SHJ', 'SKT')
    my_dep_and_dest_cities = {}

    while True:
        dep_city = input('Please,enter your departure city:')
        if dep_city in departure_cities:
            my_dep_and_dest_cities['departure_city'] = dep_city
            break
        else:
            print('Try again. Your departure city is incorrect')

    while True:
        dest_city = input('Please,enter your destination city:')
        if dest_city != dep_city and dest_city in arrival_cities:
            my_dep_and_dest_cities['destination_city'] = dest_city
            break
        else:
            print('Try again. Your destination city is incorrect')

    return my_dep_and_dest_cities


def my_dep_and_dest_dates():
    my_dep_and_dest_dates = {}

    while True:
        try:
            dep_date = input('Please,enter your departure date in (YYYY-MM-DD) format:')
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
                'Please,enter your destination date in (YYYY-MM-DD) format or enter Exit if this is not necessary:')
            match = re.search(r'^\d{4}\-\d{2}\-\d{2}$', dest_date)
            if match:
                dest_date_datetime = datetime.strptime(dest_date, '%Y-%m-%d')
                if dep_date_datetime < dest_date_datetime:
                    my_dep_and_dest_dates['destination_date'] = dest_date
                    my_dep_and_dest_dates['type'] = 'ROUND_TRIP'
                    break
                else:
                    print('Try again.The date of destination you entered cannot be earlier than the departure date')
            elif dest_date == 'EXIT':
                my_dep_and_dest_dates['type'] = 'ONE_WAY'
                break
            else:
                print('Try again.The date of destination you entered is incorrect format')
        except ValueError:
            print('Try again.Attention:MM values range from 1 to 12, DD values from 1 to 31')

    return my_dep_and_dest_dates


def my_collecting_data():
    my_collecting_data = my_dep_and_dest_cities()
    my_collecting_data.update(my_dep_and_dest_dates())
    return my_collecting_data


my_collecting_data = my_collecting_data()


def my_data_for_request(my_collecting_data):
    my_data_for_request = []
    if my_collecting_data['type'] == 'ONE_WAY':
        my_data_for_request.append(my_collecting_data)

    elif my_collecting_data['type'] == 'ROUND_TRIP':
        my_forward_trip = {}
        my_forward_trip['departure_city'] = my_collecting_data['departure_city']
        my_forward_trip['destination_city'] = my_collecting_data['destination_city']
        my_forward_trip['departure_date'] = my_collecting_data['departure_date']
        my_data_for_request.append(my_forward_trip)

        my_return_trip = {}
        my_return_trip['departure_city'] = my_collecting_data['destination_city']
        my_return_trip['destination_city'] = my_collecting_data['departure_city']
        my_return_trip['departure_date'] = my_collecting_data['destination_date']
        my_data_for_request.append(my_return_trip)

    return my_data_for_request


my_data_for_request = my_data_for_request(my_collecting_data)


def my_request(data):
    try:
        url = '''https://www.airblue.com/bookings/flight_selection.aspx?TT=OW&DC={}&AC={}&AM={}&AD={}&CC=Y&CD=&PA=1&PC=&PI=&x=48&y=5
              '''.format(data['departure_city'],
                         data['destination_city'],
                         data['departure_date'][0:7],
                         data['departure_date'][8:])

        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')

        flight_numbers = soup.find_all('td', {'class': 'flight'})
        if flight_numbers:
            my_flight_numbers = []
            for flight_number in flight_numbers:
                match = re.search(r'\w+\-\d*', flight_number.text)
                my_flight_numbers.append(match.group())

            departure_times = soup.find_all('td', {'class': 'time leaving'})
            my_departure_times = []
            for departure_time in departure_times:
                my_departure_times.append(departure_time.text)

            destination_times = soup.find_all('td', {'class': 'time landing'})
            my_destination_times = []
            for destination_time in destination_times:
                my_destination_times.append(destination_time.text)

            my_dep_and_dest_times = list(zip(my_departure_times, my_destination_times))
            my_list_dep_and_dest_times = []
            for times in my_dep_and_dest_times:
                my_list_dep_and_dest_times.append(list(times))

            for times in my_list_dep_and_dest_times:
                for time in range(len(times)):
                    times[time] = datetime.strptime(times[time], '%I:%M %p')

            my_flight_times = []
            for times_datetimes in my_list_dep_and_dest_times:
                my_flight_times.append(str(times_datetimes[1] - times_datetimes[0]))

            aircraft_brands = soup.find_all('td', {'class': 'route'})
            my_aircraft_brands = []
            for aircraft_brand in aircraft_brands:
                match = re.search(r'\w+\n(\w+\d*)', aircraft_brand.text)
                my_aircraft_brands.append(match.group(1))

            prices = soup.find_all('td', {'class': 'family family-ES family-group-Y'})
            my_prices = []
            for price in prices:
                match = re.search(r'\w+\s\d*\S\d*', price.text)
                my_prices.append(match.group())

            my_data_from_request = list(zip(my_flight_numbers, my_departure_times,
                                            my_destination_times, my_flight_times,
                                            my_aircraft_brands,my_prices))
            return my_data_from_request

        else:
            print('No flights found for your selected flight data')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout occured!')
    except requests.exceptions.ReadTimeout:
        print('Read timeout occured!')
    except requests.exceptions.ConnectionError:
        print('Seems like dns lookup failed')
    except requests.exceptions.HTTPError:
        print('HTTP Error occured')


def print_my_all_data(my_data_for_request):
    for data in my_data_for_request:
        my_data_from_request = my_request(data)
        if my_data_from_request:
            print('''FLIGHT DATA:
                         DEPARTURE DATE:{}
                         DEPARTURE CITY:{}
                         DESTINATION CITY:{}
                  '''.format(data['departure_date'],
                             data['departure_city'],
                             data['destination_city']))

            for data in my_data_from_request:
                print('''FLIGHT NUMBER:{}
                         DEPARTURE TIME:{}
                         DESTINATION TIME:{}
                         FLIGHT TIME:{}
                         AIRCRAFT BRAND:{}
                         PRICE:{}
                      '''.format(data[0], data[1], data[2], data[3], data[4], data[5]))


print_my_all_data(my_data_for_request)
