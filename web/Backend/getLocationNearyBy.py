import requests

def getLocFun(latitude,longitude,radius,type):

# Replace with your actual Google Maps API key
    API_KEY = 'AIzaSyAe1B0CgdZI5hfPA9-ooDPYqRPeoYLRtw4'

# Define the API endpoint and parameters

    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

# Set up the parameters for the API request
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'type': type,
        'key': API_KEY
    }

# Make the request to the Google Maps API
    response = requests.get(url, params=params)

# Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Print out the results
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    return data['results'][:5]
#getLocationNearyBy.py