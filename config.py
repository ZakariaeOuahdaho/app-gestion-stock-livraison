import googlemaps
from config import GOOGLE_MAPS_API_KEY

def test_api():
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    try:
        result = gmaps.geocode("Paris, France")
        print("API fonctionne :", result)
    except Exception as e:
        print("Erreur API :", str(e))

if __name__ == "__main__":
    test_api()