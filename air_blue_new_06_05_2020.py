import sys
import argparse
import datetime
import requests
from lxml import html
import re

def my_request(my_data_for_request):
    try:
        url = '''https://www.airblue.com/bookings/flight_selection.aspx?'''
        if my_data_for_request['destination_date'] == '':
            payload = {'TT': my_data_for_request['type'],
                       'DC': my_data_for_request['departure_city'],
                       'AC': my_data_for_request['destination_city'],
                       'AM': my_data_for_request['departure_date'].isoformat()[0:7],
                       'AD': my_data_for_request['departure_date'].isoformat()[8:],
                       'RM': my_data_for_request['destination_date'],
                       'RD': my_data_for_request['destination_date'],
                       'PA': my_data_for_request['adults'],
                       'PC': my_data_for_request['children'],
                       'PI': my_data_for_request['infants']
                       }
        else:
            payload = {'TT': my_data_for_request['type'],
                       'DC': my_data_for_request['departure_city'],
                       'AC': my_data_for_request['destination_city'],
                       'AM': my_data_for_request['departure_date'].isoformat()[0:7],
                       'AD': my_data_for_request['departure_date'].isoformat()[8:],
                       'RM': my_data_for_request['destination_date'].isoformat()[0:7],
                       'RD': my_data_for_request['destination_date'].isoformat()[8:],
                       'PA': my_data_for_request['adults'],
                       'PC': my_data_for_request['children'],
                       'PI': my_data_for_request['infants']
                       }
        response = requests.get(url, params = payload)
        parsed_body = html.fromstring(response.text)
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout occured!')
        sys.exit()
    except requests.exceptions.ReadTimeout:
        print('Read timeout occured!')
        sys.exit()
    except requests.exceptions.ConnectionError:
        print('Seems like dns lookup failed')
        sys.exit()
    except requests.exceptions.HTTPError:
        print('HTTP Error occured')
        sys.exit()
    else:
        return parsed_body

class My_Flights():
    def __init__(self, parsed_body, my_data_for_request):
        self.parsed_body = parsed_body
        self.my_data_for_request = my_data_for_request

    def my_trips(self, trip_id):
        if trip_id == 1:
            trip = 'From {} To {}-{}'.format(self.my_data_for_request['departure_city'],
                                             self.my_data_for_request['destination_city'],
                                             self.my_data_for_request['departure_date'].strftime('%A,%d %B %Y'))
        else:
            trip = 'From {} To {}-{}'.format(self.my_data_for_request['destination_city'],
                                             self.my_data_for_request['departure_city'],
                                             self.my_data_for_request['destination_date'].strftime('%A,%d %B %Y'))
        return trip

    def my_flights(self, trip_id):
        flights = self.parsed_body.xpath('//div[@id="trip_{}"]//td[@class="flight"]/text()'.format(trip_id))
        for flight in range(len(flights)):
            flights[flight] = flights[flight].strip()
        return flights

    def my_departure_times(self, trip_id):
        departure_times = self.parsed_body.xpath(
            '//div[@id="trip_{}"]//td[@class="time leaving"]/text()'.format(trip_id))
        return departure_times

    def my_destination_times(self, trip_id):
        destination_times = self.parsed_body.xpath(
            '//div[@id="trip_{}"]//td[@class="time landing"]/text()'.format(trip_id))
        return destination_times

    def my_aircraft_brands(self, trip_id):
        aircraft_brands = self.parsed_body.xpath(
            '//div[@id="trip_{}"]//td[@class="route"]/span[2]/text()'.format(trip_id))
        return aircraft_brands

    def my_prices_no_bag(self, trip_id, flight):
        prices_no_bag = self.parsed_body.xpath(
            '//div[@id="trip_{}"]//tbody[{}]//td[@class="family family-ED family-group-Y "]/label/@data-title'.format(
                trip_id, flight))
        if prices_no_bag:
            for price in range(len(prices_no_bag)):
                prices_no_bag[price] = re.search(r'\w+\s\d+\,*\d+', prices_no_bag[price]).group()
        else:
            prices_no_bag = self.parsed_body.xpath(
                '//div[@id="trip_{}"]//tbody[{}]//td[@class="family family-ED family-group-Y "]/label/text()'.format(
                    trip_id, flight))
        return prices_no_bag

    def my_prices_with_bag(self, trip_id, flight):
        prices_with_bag = self.parsed_body.xpath(
            '//div[@id="trip_{}"]//tbody[{}]//td[@class="family family-ES family-group-Y "]/label/@data-title'.format(
                trip_id, flight))
        if prices_with_bag:
            for price in range(len(prices_with_bag)):
                prices_with_bag[price] = re.search(r'\w+\s\d+\,*\d+', prices_with_bag[price]).group()
        else:
            prices_with_bag = self.parsed_body.xpath(
                '//div[@id="trip_{}"]//tbody[{}]//td[@class="family family-ES family-group-Y "]/label/text()'.format(
                    trip_id, flight))
        return prices_with_bag

    def my_data_from_request(self):
        if self.my_data_for_request['type'] == 'OW':
            trips_id = [1]
        else:
            trips_id = [1, 2]

        my_data_from_request = []
        for trip_id in trips_id:
            my_flights = {}
            for flight in range(len(self.my_flights(trip_id))):
                my_flight = {}
                if self.my_departure_times(trip_id):
                    my_departure_times = {}
                    my_departure_times['DEPARTURE TIME'] = self.my_departure_times(trip_id)[flight]
                    my_flight.update(my_departure_times)
                if self.my_destination_times(trip_id):
                    my_destination_times = {}
                    my_destination_times['DESTINATION TIME'] = self.my_destination_times(trip_id)[flight]
                    my_flight.update(my_destination_times)
                if self.my_aircraft_brands(trip_id):
                    my_aircraft_brands = {}
                    my_aircraft_brands['AIRCRAFT BRAND'] = self.my_aircraft_brands(trip_id)[flight]
                    my_flight.update(my_aircraft_brands)
                if self.my_prices_no_bag(trip_id, flight + 1):
                    my_prices_no_bag = {}
                    my_prices_no_bag['PRICE WITHOUT BAGGAGE'] = ''.join(self.my_prices_no_bag(trip_id, flight + 1))
                    my_flight.update(my_prices_no_bag)
                else:
                    my_prices_no_bag = {}
                    my_prices_no_bag['PRICE WITHOUT BAGGAGE'] = 'not available'
                    my_flight.update(my_prices_no_bag)
                if self.my_prices_with_bag(trip_id, flight + 1):
                    my_prices_with_bag = {}
                    my_prices_with_bag['BAGGAGE PRICE'] = ''.join(self.my_prices_with_bag(trip_id, flight + 1))
                    my_flight.update(my_prices_with_bag)
                else:
                    my_prices_with_bag = {}
                    my_prices_with_bag['BAGGAGE PRICE'] = 'not available'
                    my_flight.update(my_prices_with_bag)

                my_flights[self.my_flights(trip_id)[flight]] = my_flight
            my_data_from_request_dict = {}
            my_data_from_request_dict[self.my_trips(trip_id)] = my_flights
            my_data_from_request.append(my_data_from_request_dict)
        return my_data_from_request

def my_print(my_data_from_request):
    for my_data_from_request_dict in my_data_from_request:
        for trip in my_data_from_request_dict:
            print('\n{}'.format(trip))
            if my_data_from_request_dict[trip]:
                for flight in sorted(my_data_from_request_dict[trip]):
                    print('\nFLIGHT:{}'.format(flight))
                    print('''\rDEPARTURE TIME:{}
                             \rDESTINATION TIME:{}
                             \rAIRCRAFT BRAND:{}
                             \rPRICE WITHOUT BAGGAGE:{}
                             \rBAGGAGE PRICE:{}'''.format(my_data_from_request_dict[trip][flight]['DEPARTURE TIME'],
                                                          my_data_from_request_dict[trip][flight]['DESTINATION TIME'],
                                                          my_data_from_request_dict[trip][flight]['AIRCRAFT BRAND'],
                                                          my_data_from_request_dict[trip][flight]['PRICE WITHOUT BAGGAGE'],
                                                          my_data_from_request_dict[trip][flight]['BAGGAGE PRICE']))
            else:
                print('NO TICKETS FOUND')

def main():
    def my_dep_and_dest_cities(**kwargs):
        departure_cities = ('AUH', 'DXB', 'ISB', 'JED', 'KHI', 'LHE', 'MED', 'MUX', 'PEW', 'UET', 'RUH', 'SHJ')
        arrival_cities = (
            'AUH', 'DMM', 'DXB', 'ISB', 'JED', 'KHI', 'LHE', 'MED', 'MUX', 'MCT', 'PEW', 'RYK', 'RUH', 'SHJ', 'SKT')
        my_dep_and_dest_cities = {}
        if kwargs:
            dep_city = kwargs['dep_city']
            if dep_city in departure_cities:
                my_dep_and_dest_cities['departure_city'] = dep_city
            else:
                print('Try again.You entered incorrect data.Please enter the departure city by selecting it from the following:{}'.format(
                            ', '.join(departure_cities)))
                sys.exit()
            dest_city = kwargs['dest_city']
            if dest_city != dep_city and dest_city in arrival_cities:
                my_dep_and_dest_cities['destination_city'] = dest_city
            elif dest_city == dep_city:
                print('Try again. Your destination city should not be equal to departure city')
                sys.exit()
            else:
                print(
                    'Try again.You entered incorrect data.Please enter the destination city by selecting it from the following:{}'.format(
                        ', '.join(arrival_cities)))
                sys.exit()
        else:
            while True:
                dep_city = input('Please enter the departure city by selecting it from the following:{}:'.format(
                    ', '.join(departure_cities))).strip()
                if dep_city in departure_cities:
                    my_dep_and_dest_cities['departure_city'] = dep_city
                    break
                else:
                    print('Try again.You entered incorrect data')
            while True:
                dest_city = input('Please enter the destination city by selecting it from the following:{}:'.format(
                    ', '.join(arrival_cities))).strip()
                if dest_city != dep_city and dest_city in arrival_cities:
                    my_dep_and_dest_cities['destination_city'] = dest_city
                    break
                elif dest_city == dep_city:
                    print('Try again. Your destination city should not be equal to departure city')
                else:
                    print('Try again.You entered incorrect data')
        return my_dep_and_dest_cities

    def my_dep_and_dest_dates(**kwargs):
        my_dep_and_dest_dates = {}
        if kwargs:
            try:
                dep_date = kwargs['dates']['dep_date']
                dep_date_datetime = datetime.datetime.strptime(dep_date, '%Y-%m-%d').date()
                now_time = datetime.datetime.now().date()
                if dep_date_datetime >= now_time:
                    my_dep_and_dest_dates['departure_date'] = dep_date_datetime
                else:
                    print('Try again.The date of departure you entered cannot be earlier than the current date')
                    sys.exit()
                if 'dest_date' in kwargs['dates']:
                    dest_date = kwargs['dates']['dest_date']
                    dest_date_datetime = datetime.datetime.strptime(dest_date, '%Y-%m-%d').date()
                    if dep_date_datetime <= dest_date_datetime:
                        my_dep_and_dest_dates['destination_date'] = dest_date_datetime
                        my_dep_and_dest_dates['type'] = 'RT'
                    else:
                        print('Try again.The date of destination you entered cannot be earlier than the departure date')
                        sys.exit()
                else:
                    my_dep_and_dest_dates['destination_date'] = ''
                    my_dep_and_dest_dates['type'] = 'OW'
            except ValueError:
                print(
                    'Try again.Attention:YYYY values should start from 2020, MM values range from 1 to 12, DD values from 1 to 31')
                sys.exit()
        else:
            while True:
                try:
                    dep_date = input('Please,enter your departure date in (YYYY-MM-DD) format:').strip()
                    dep_date_datetime = datetime.datetime.strptime(dep_date, '%Y-%m-%d').date()
                    now_time = datetime.datetime.now().date()
                    if dep_date_datetime >= now_time:
                        my_dep_and_dest_dates['departure_date'] = dep_date_datetime
                        break
                    else:
                        print('Try again.The date of departure you entered cannot be earlier than the current date')
                except ValueError:
                    print(
                        'Try again.Attention:YYYY values should start from 2020, MM values range from 1 to 12, DD values from 1 to 31')
            while True:
                try:
                    dest_date = input(
                        '''Please,enter your destination date in (YYYY-MM-DD) format or enter nothing if it is not necessary:''').strip()
                    dest_date_datetime = datetime.datetime.strptime(dest_date, '%Y-%m-%d').date()
                    if dep_date_datetime <= dest_date_datetime:
                        my_dep_and_dest_dates['destination_date'] = dest_date_datetime
                        my_dep_and_dest_dates['type'] = 'RT'
                        break
                    else:
                        print('Try again.The date of destination you entered cannot be earlier than the departure date')
                except ValueError:
                    if dest_date == '':
                        my_dep_and_dest_dates['destination_date'] = dest_date
                        my_dep_and_dest_dates['type'] = 'OW'
                        break
                    else:
                        print(
                            'Try again.Attention:YYYY values should start from 2020, MM values range from 1 to 12, DD values from 1 to 31')
        return my_dep_and_dest_dates

    def my_passengers(**kwargs):
        adult_passengers = ('1', '2', '3', '4', '5', '6')
        children_passengers = ('1', '2', '3', '4', '5')
        my_passengers = {}
        if kwargs:
            adults = kwargs['passengers']['adults']
            if adults in adult_passengers:
                my_passengers['adults'] = adults
                if 'children' in kwargs['passengers']:
                    if adults == '6':
                        print('Since you have selected the maximum allowable number of adult passengers,'
                              'the choice of child passengers is not possible')
                        sys.exit()
                    else:
                        children = kwargs['passengers']['children']
                        index_adults = adult_passengers.index(adults)
                        children_passengers = children_passengers[0:len(children_passengers) - index_adults]
                        if children in children_passengers:
                            my_passengers['children'] = children
                        else:
                            print('You entered the wrong number of child passengers.It should match the following values:{}'.format(
                                ', '.join(children_passengers)))
                            sys.exit()
                else:
                    my_passengers['children'] = ''
                if 'infants' in kwargs['passengers']:
                    infants = kwargs['passengers']['infants']
                    if infants in adult_passengers[0:int(adults)]:
                        my_passengers['infants'] = infants
                    else:
                        print('You entered the wrong number of infants passengers.It should match the following values:{}'.format(
                                    ', '.join(adult_passengers[0:int(adults)])))
                        sys.exit()
                else:
                    my_passengers['infants'] = ''
            else:
                print('You entered the wrong number of adult passengers.It should match the following values:{}'.format(
                    ', '.join(adult_passengers)))
                sys.exit()
        else:
            while True:
                adults = input(
                    '''Please enter the number of adult passengers corresponding to the following values:{}:'''.format(
                        ', '.join(adult_passengers))).strip()
                if adults in adult_passengers:
                    index_adults = adult_passengers.index(adults)
                    children_passengers = children_passengers[0:len(children_passengers) - index_adults]
                    my_passengers['adults'] = adults
                    break
                else:
                    print('You entered the wrong number of adult passengers')
            while True:
                if adults == '6':
                    my_passengers['children'] = ''
                    print('Since you have selected the maximum allowable number of adult passengers,'
                          'the choice of child passengers is not possible')
                    break
                else:
                    children = input(
                        '''Please enter the number of child passengers corresponding to the following values:{}, or leave the field empty if there are no children:'''.format(
                            ', '.join(children_passengers))).strip()
                    if children in children_passengers or children == '':
                        my_passengers['children'] = children
                        break
                    else:
                        print('You entered the wrong number of child passengers')
            while True:
                infants = input(
                    '''Please enter the number of infants passengers corresponding to the following values:{} or leave the field empty if there are no infants:'''.format(
                        ', '.join(adult_passengers[0:int(adults)]))).strip()
                if infants in adult_passengers[0:int(adults)] or infants == '':
                    my_passengers['infants'] = infants
                    break
                else:
                    print('You entered the wrong number of infants passengers')
        return my_passengers

    def createParser():
        parser = argparse.ArgumentParser(description = '''Enter the following positional parameters in strict order:'
            DEPARTURE_CITY:three-digit code in capital letters.
            DESTINATION_CITY:three-digit code in capital letters.
            DEPARTURE_DATE:in format'YYYY-MM-DD'.
            ADULTS:number of adult passengers(from 1 to 6).
            Enter the following optional parameters if necessary:
            --dest_date:selectable if return flight is required(in format-'YYYY-MM-DD')
            --children:selected to add children as passengers(from 1 to 5, but depends on the number of adult passengers)
            --infants:selected to add infants as passengers(from 1 to 6,but not more than the number of adult passengers)''')
        parser.add_argument('dep_city', metavar = 'DEPARTURE_CITY')
        parser.add_argument('dest_city', metavar = 'DESTINATION_CITY')
        parser.add_argument('dep_date', metavar = 'DEPARTURE_DATE')
        parser.add_argument('adults', metavar = 'ADULTS')
        parser.add_argument('--dest_date',  metavar = 'DESTINATION_DATE')
        parser.add_argument('--children')
        parser.add_argument('--infants')
        return parser

    if len(sys.argv) == 1:
        print('Now the program will start without arguments.If you want to run the program with arguments,'
              'then usage:[-h, --help]')
        my_data_for_request = my_dep_and_dest_cities()
        my_data_for_request.update(my_dep_and_dest_dates())
        my_data_for_request.update(my_passengers())
    else:
        parser = createParser()
        namespace = parser.parse_args()
        my_arguments = {}
        my_arguments['dep_city'] = namespace.dep_city
        my_arguments['dest_city'] = namespace.dest_city
        my_arguments['dep_date'] = namespace.dep_date
        my_arguments['adults'] = namespace.adults
        if namespace.dest_date:
            my_arguments['dest_date'] = namespace.dest_date
        if namespace.children:
            my_arguments['children'] = namespace.children
        if namespace.infants:
            my_arguments['infants'] = namespace.infants
        my_data_for_request = my_dep_and_dest_cities(dep_city = namespace.dep_city, dest_city = namespace.dest_city)
        my_data_for_request.update(my_dep_and_dest_dates(dates = my_arguments))
        my_data_for_request.update(my_passengers(passengers = my_arguments))
    return my_data_for_request


if __name__ == '__main__':
    my_data_for_request = main()
    parsed_body = my_request(my_data_for_request)
    TRIP = My_Flights(parsed_body, my_data_for_request)
    my_data_from_request = TRIP.my_data_from_request()
    my_print(my_data_from_request)
