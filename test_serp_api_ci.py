import requests

# ================= CONFIG =================
BASE_URL = "https://serpapi.com/search.json"
API_KEY = "c5e97aaf4902c99623fda258c0b668b7c9e54b70f0636bd271d15414d6870c60"
PLACE_ID = "ChIJTyvs2l3DwjsR0TOBDRcqQyM"


# ================= API METHOD =================
def get_place_details():
    params = {
        "engine": "google_maps",
        "type": "place",
        "api_key": API_KEY,
        "place_id": PLACE_ID
    }
    return requests.get(BASE_URL, params=params)


# ================= TEST CASES =================
def test_serp_api_status_code():
    response = get_place_details()
    assert response.status_code == 200


def test_serp_api_response_schema():
    response = get_place_details()
    data = response.json()

    assert "search_metadata" in data
    assert "place_results" in data
