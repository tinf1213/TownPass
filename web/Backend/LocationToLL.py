import requests

def get_lat_lng(location_name):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location_name}&key=AIzaSyAe1B0CgdZI5hfPA9-ooDPYqRPeoYLRtw4"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        raise Exception("Error: " + data['status'])