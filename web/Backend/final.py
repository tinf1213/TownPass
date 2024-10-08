import os
import base64
import requests
from getLocationNearyBy import getLocFun
from LocationToLL import get_lat_lng

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
import logging
import sys

from dotenv import load_dotenv

# Initialize FastAPI app
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Setup logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Configuration for Llama Index and Gemini API

load_dotenv()
PERSIST_DIR = "./storage"
GEMINI_API = "AIzaSyA6aZMqy25exL1J1QHzDme1RfPpLclbdgQ"
GOOGLE_VISION_API_KEY = os.getenv('GOOGLE_VISION_API_KEY')

Settings.embed_model = GeminiEmbedding(model_name="models/embedding-001", api_key=GEMINI_API)
Settings.llm = Gemini(api_key=GEMINI_API)

# Load or create index
if not os.path.exists(PERSIST_DIR):
    documents = SimpleDirectoryReader("docs").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()


# Function to query location using the query engine
@app.post("/query-location")
async def query_location(location_name: str = Form(...)):
    response = query_engine.query("You're a local guide now, please give me detail introduction and history story about" + location_name + " as I'm a visitor never been to here, and very interest in it's history also explain all your content in chinese please.")
    return PlainTextResponse(str(response))


# Function to detect landmarks using Google Cloud Vision API
def detect_landmarks(image_path, api_key):
    """Use Google Cloud Vision API and API Key to detect landmarks in the image."""
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"

    # Read image in binary mode and encode as base64
    with open(image_path, "rb") as image_file:
        image_content = base64.b64encode(image_file.read()).decode("utf-8")

    # Build request body
    request_body = {
        "requests": [
            {
                "image": {"content": image_content},
                "features": [{"type": "LANDMARK_DETECTION", "maxResults": 1}],
            }
        ]
    }

    # Send request to Google Vision API
    response = requests.post(url, json=request_body)

    if response.status_code == 200:
        return extract_first_landmark(response.json())
    else:
        return f"Error: {response.status_code}, {response.text}"


# Function to extract the first detected landmark
def extract_first_landmark(landmarks_data):
    """Extract the first landmark's information from API response."""
    if landmarks_data and 'responses' in landmarks_data:
        landmarks = landmarks_data['responses'][0].get('landmarkAnnotations', [])
        if landmarks:
            first_landmark = landmarks[0]
            description = first_landmark['description']  # Landmark name
            return description
        else:
            return "No landmarks detected."
    return "Invalid response."


# Route to handle image upload, detect landmarks, and query the result
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Save the uploaded image temporarily
    try:
        image_content = await file.read()
        temp_image_path = f"./uploaded_{file.filename}"

        # Save image to disk
        with open(temp_image_path, "wb") as temp_file:
            temp_file.write(image_content)

        # Detect landmarks in the image
        landmark_name = detect_landmarks(temp_image_path, GOOGLE_VISION_API_KEY)

        # If no landmark detected, return an error
        if "Error" in landmark_name or "No landmarks detected" in landmark_name:
            raise HTTPException(status_code=400, detail=landmark_name)

        # Query the detected landmark using the query engine
        response = query_engine.query("You're a local guide now, please give me detail introduction and history story about" + landmark_name + " as I'm a visitor never been to here, and very interest in it's history also explain all your content in chinese please.")

        print(response)
        return PlainTextResponse(f"Landmark: {landmark_name}\nQuery Result: {response}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        # Clean up temporary image file
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)


@app.post("/api/data")
async def get_nearby_places(
    lat: float = Form(...),
    lon: float = Form(...),
    radius: int = Form(...),
    place_type: str = Form(...)
):
    # Get the data from the function
    data = getLocFun(lat, lon, radius, place_type)
    urls=[]
    # Create a list of Google Maps URLs based on the locations
    for i in data:
        urls.append((
            {"link": f"https://www.google.com/maps?q={float(i['geometry']['location']['lat'])},{float(i['geometry']['location']['lng'])}"},
            {"name": i['name']}
        ))
        #print(f"https://www.google.com/maps?q={place['geometry']['location']['lat']},{place['geometry']['location']['lng']}")
    print("testing")
    return {"places": urls}

@app.post("/api/getLL")
async def getLLfun(location_name: str = Form(...)):
    latitude, longitude = get_lat_lng(location_name)
    print(f"纬度: {latitude}, 经度: {longitude}")
    return {"places": {"latitude": latitude, "longitude": longitude}}

@app.post("/api/getLocationName")
async def getLocationName(lat: float = Form(...), lon: float = Form(...)):
    location_name = get_location_name(lat, lon)
    return {"location_name": location_name}

# Function to get the location name based on latitude and longitude
def get_location_name(latitude, longitude):
    """Use Google Maps Geocoding API to get the location name based on latitude and longitude."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_VISION_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            location_name = data["results"][0]["formatted_address"]
            return location_name
        else:
            return "Location not found."
    else:
        return f"Error: {response.status_code}, {response.text}"
# To run the app, use `uvicorn final:app --reload` in the terminal

