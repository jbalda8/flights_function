import requests
import json
import pandas as pd

def getFlights(airport, iata_par):
    params = {
    'access_key': '0cc2b789f9e1e75e1b006cbe872ff884',
    iata_par: airport
    }

    r = requests.get('http://api.aviationstack.com/v1/flights', params)

    api_response = r.json()

    data = []
    for flight in api_response['data']:
        if (flight['flight_status'] == 'active'):
            estimated_arr = flight['arrival']['estimated']
            estimated_arr_split = estimated_arr[11:16]
            data.append([flight['airline']['name'], flight['flight']['iata'], flight['departure']['airport'],
                        flight['departure']['iata'], flight['arrival']['airport'], flight['arrival']['iata'],
                        estimated_arr_split])

    df = pd.DataFrame(data, columns=['airline', 'flight_iata', 'departure_airport', 'departure_iata', 'arrival_airport',
                                    'arrival_iata', 'arrival_estimated'])

    df_json = df.to_json(orient='split')
    parsed = json.loads(df_json)
    json.dumps(parsed, indent=4)

    if iata_par == 'dep_iata':
        json_name = flight['departure']['iata'] + '_flights_dep.json'
    else:
        json_name = flight['arrival']['iata'] + '_flights_arr.json'

    with open(json_name, 'w') as json_file:
        json.dump(parsed, json_file)

if __name__ == "__main__":
    getFlights('IND', 'dep_iata')
    getFlights('IND', 'arr_iata')