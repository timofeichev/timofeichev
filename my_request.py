from my_data_for_request import my_data_for_request
import requests
from lxml import html


def my_request(my_data_for_request):
    try:
        url = '''https://www.airblue.com/bookings/flight_selection.aspx?'''
        payload = {
                   'TT': my_data_for_request['type'],
                   'DC': my_data_for_request['departure_city'],
                   'AC': my_data_for_request['destination_city'],
                   'AM': my_data_for_request['departure_date'][0:7],
                   'AD': my_data_for_request['departure_date'][8:],
                   'RM': my_data_for_request['destination_date'][0:7],
                   'RD': my_data_for_request['destination_date'][8:],
                   'PA': '1'
                  }
        request = requests.get(url, params = payload)
        parsed_body = html.fromstring(request.text)

        return parsed_body

    except requests.exceptions.ConnectTimeout:
        print('Connection timeout occured!')
    except requests.exceptions.ReadTimeout:
        print('Read timeout occured!')
    except requests.exceptions.ConnectionError:
        print('Seems like dns lookup failed')
    except requests.exceptions.HTTPError:
        print('HTTP Error occured')


def my_data_from_request(parsed_body, my_data_for_request):
    if my_data_for_request['type'] == 'OW':
        trip_id = [1]
    if my_data_for_request['type'] == 'RT':
        trip_id = [1, 2]

    my_searching_data = [[{'flight_numbers':'td[@class="flight"]'}],
                         [{'departure_times':'td[@class="time leaving"]'}],
                         [{'destination_times':'td[@class="time landing"]'}],
                         [{'aircraft_brands':'td[@class="route"]/span[2]'}],
                         [{'prices':'td[@class="family family-ES family-group-Y "]/label/span'}],
                         [{'currencies':'td[@class="family family-ES family-group-Y "]/label/span/b'}]
                        ]

    my_data_from_request = []
    trip_1 = []
    trip_2 = []
    for id in trip_id:
        for list in my_searching_data:
            for dict in list:
                for key in dict:
                    results = parsed_body.xpath('//div[@id="trip_{}"]//{}/text()'.format(id, dict[key]))
                    if results:
                        for result in range(len(results)):
                            results[result] = results[result].strip()
                        if id == 1:
                            trip_1.append(dict.fromkeys(dict, results))
                        if id == 2:
                            trip_2.append(dict.fromkeys(dict, results))

    if trip_1:
        trip_1.append({'trip':'trip_1'})
        my_data_from_request.append(trip_1)

    if trip_2:
        trip_2.append({'trip':'trip_2'})
        my_data_from_request.append(trip_2)

    if my_data_from_request:
        return my_data_from_request


def my_all_data_print(my_data_for_request, my_data_from_request):
    if my_data_from_request:
        if my_data_for_request['type'] == 'OW':
            print('''FLIGHT DATA:
                     FLIGHT TYPE:{}
                     DEPARTURE DATE:{}
                     DEPARTURE CITY:{}
                     DESTINATION CITY:{}
                  '''.format(my_data_for_request['type'],
                             my_data_for_request['departure_date'],
                             my_data_for_request['departure_city'],
                             my_data_for_request['destination_city'])
                  )

        if my_data_for_request['type'] == 'RT':
            print('''FLIGHT DATA:
                     FLIGHT TYPE:{}
                     DEPARTURE DATE:{}
                     DESTINATION DATE {}
                     DEPARTURE CITY:{}
                     DESTINATION CITY:{}
                  '''.format(my_data_for_request['type'],
                             my_data_for_request['departure_date'],
                             my_data_for_request['destination_date'],
                             my_data_for_request['departure_city'],
                             my_data_for_request['destination_city'])
                  )


        for i in range(len(my_data_from_request)):
            if my_data_for_request['type'] == 'OW':
                print('FLIGHTS from {} to {} on {}:'.format(my_data_for_request['departure_city'],
                                                            my_data_for_request['destination_city'],
                                                            my_data_for_request['departure_date']))
            if my_data_for_request['type'] == 'RT':
                if len(my_data_from_request) == 2:
                    if i == 0:
                        print('FLIGHTS from {} to {} on {}:'.format(my_data_for_request['departure_city'],
                                                                    my_data_for_request['destination_city'],
                                                                    my_data_for_request['departure_date']))
                    if i == 1:
                        print('FLIGHTS from {} to {} on {}:'.format(my_data_for_request['destination_city'],
                                                                    my_data_for_request['departure_city'],
                                                                    my_data_for_request['destination_date']))
                if len(my_data_from_request) == 1:
                    if my_data_from_request[0][6]['trip'] == 'trip_1':
                        print('NO FLIGHTS FOUND from {} to {} on {}.\nFLIGHTS from {} to {} on {}:'
                              .format(my_data_for_request['destination_city'],
                                      my_data_for_request['departure_city'],
                                      my_data_for_request['destination_date'],
                                      my_data_for_request['departure_city'],
                                      my_data_for_request['destination_city'],
                                      my_data_for_request['departure_date']))

                    if my_data_from_request[0][6]['trip'] == 'trip_2':
                        print('NO FLIGHTS FOUND from {} to {} on {}.\nFLIGHTS from {} to {} on {}:'
                              .format(my_data_for_request['departure_city'],
                                      my_data_for_request['destination_city'],
                                      my_data_for_request['departure_date'],
                                      my_data_for_request['destination_city'],
                                      my_data_for_request['departure_city'],
                                      my_data_for_request['destination_date']))

            for k in range(len(my_data_from_request[0][0]['flight_numbers'])):
                print('''
                     FLIGHT NUMBER:{}
                     DEPARTURE TIME:{}
                     DESTINATION TIME:{}
                     AIRCRAFT BRAND:{}
                     PRICE:{},{}
                      '''.format(my_data_from_request[i][0]['flight_numbers'][k],
                                 my_data_from_request[i][1]['departure_times'][k],
                                 my_data_from_request[i][2]['destination_times'][k],
                                 my_data_from_request[i][3]['aircraft_brands'][k],
                                 my_data_from_request[i][4]['prices'][k],
                                 my_data_from_request[i][5]['currencies'][k])
                      )

    else:
        print('NO FLIGHTS FOUND')

if __name__ == '__main__':
    parsed_body = my_request(my_data_for_request)
    my_data_from_request = my_data_from_request(parsed_body, my_data_for_request)
    my_all_data_print = my_all_data_print(my_data_for_request, my_data_from_request)