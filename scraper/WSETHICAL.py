'''
Created on Jan 18, 2025

@author: kevin
'''

import requests

API_KEY = "YOUR_API_KEY"
PLACE_ID = "YOUR_PLACE_ID"

# Fetch place details + find place id in google API
url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=name,rating,reviews&key={API_KEY}"
response = requests.get(url)
'''
{
  "result": {
    "name": "Coffee Corner",
    "rating": 4.5,
    "reviews": [
      {
        "author_name": "John Doe",
        "rating": 5,
        "text": "Great coffee and cozy atmosphere!"
      },
      {
        "author_name": "Jane Smith",
        "rating": 4,
        "text": "Nice place, but it could be a bit quieter."
      }
    ]
  }
}
'''

data = response.json()

# Display reviews
if "result" in data:
    print(f"Business Name: {data['result']['name']}") #accesses name field inside result directory
    print(f"Rating: {data['result']['rating']}")
    print("Reviews:")
    for review in data["result"]["reviews"]:
        print(f"- {review['author_name']} ({review['rating']}/5): {review['text']}")
else:
    print("No reviews found.")