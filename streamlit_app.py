import time
import folium
import streamlit as st
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
from nltk import PunktTokenizer
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')
# Function to extract cities
def extract_cities(text):
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    named_entities = ne_chunk(pos_tags)

    cities = []
    for subtree in named_entities:
        if isinstance(subtree, Tree) and subtree.label() == "GPE":
            cities.append(" ".join([token for token, pos in subtree]))
    return list(set(cities))  # Remove duplicates

# Function to create a map with caching and delays
def create_map(cities):
    geolocator = Nominatim(user_agent="city_map")
    coordinates_cache = {}  # Cache to store city coordinates
    
    m = folium.Map(location=[20.0, 0.0], zoom_start=2)
    for city in cities:
        if city not in coordinates_cache:  # Check if not already cached
            try:
                location = geolocator.geocode(city, timeout=10)
                if location:
                    coordinates_cache[city] = (location.latitude, location.longitude)
                    time.sleep(1)  
            except Exception as e:
                st.warning(f"Could not geocode city: {city}. Error: {e}")
        
        # Add marker if city has coordinates
        if city in coordinates_cache:
            lat, lon = coordinates_cache[city]
            folium.Marker(
                location=[lat, lon],
                popup=city,
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(m)
    return m
para='''New York is a bustling city. People from Paris, Tokyo, and Delhi often visit it.
Many tech companies have offices in San Francisco and Bangalore.'''
# Streamlit app
st.title("City Extraction and Map")
paragraph = st.text_area("Enter a paragraph:", para)

if paragraph:
    cities = extract_cities(paragraph)
    st.subheader("Extracted Cities:")
    st.write(cities)
    
    if cities:
        st.subheader("Map of Extracted Cities:")
        city_map = create_map(cities)
        st_folium(city_map, width=800, height=500)
