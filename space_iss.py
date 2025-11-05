# ISS Tracker + Webex Space Bot

# 1. Import libraries
import requests
import json
import time
from iso3166 import countries


# 2. Webex Token
def get_access_token():
    choice = input("Do you wish to use the hard-coded Webex token? (y/n): ")
    if choice.lower() == "y":
        return "Bearer " + input("Enter your Webex Access Token: ")
    else:
        return "Bearer MGVkYjVhZmQtZGY2Ni00YjgwLWFiZWMtNDRmNjhiNzRjZWIyYTZkNGU1ZjktMDhi_P0A1_251b8f7b-fbc7-4534-b240-867707e063a8"


# 3. Get Webex rooms
def get_webex_rooms(access_token):
    response = requests.get(
        "https://webexapis.com/v1/rooms",
        headers={"Authorization": access_token}
    )

    if response.status_code != 200:
        raise Exception(f"Webex API error: {response.status_code} - {response.text}")

    rooms = response.json()["items"]
    print("List of available rooms:")
    for room in rooms:
        print(f"Room Type: {room['type']} | Title: {room['title']}")
    return rooms


# Choose room to monitor
def choose_room(rooms):
    print("List of available rooms:")
    for i, room in enumerate(rooms):
        print(f"{i + 1}. {room['title']}")

    while True:
        room_name = input("Which room should be monitored? ")
        for room in rooms:
            if room_name.lower() in room["title"].lower():
                print("Found room:", room["title"])
                return room["id"]
        print("Room not found. Please try again.")


# Get the latest message
def get_latest_message(room_id, access_token):
    params = {"roomId": room_id, "max": 1}
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=params,
        headers={"Authorization": access_token}
    )
    if r.status_code != 200:
        print("Error fetching messages:", r.text)
        return None

    data = r.json()
    if len(data["items"]) == 0:
        return None
    return data["items"][0]["text"]


# Get ISS current location
def get_iss_location():
    r = requests.get("http://api.open-notify.org/iss-now.json")
    if r.status_code != 200:
        print("Error fetching ISS data:", r.text)
        return None, None, None

    data = r.json()
    lat = data["iss_position"]["latitude"]
    lng = data["iss_position"]["longitude"]
    timestamp = data["timestamp"]
    return lat, lng, timestamp


# Get location from coordinates
def get_location_from_coords(lat, lng, api_key):
    params = {"key": api_key, "location": f"{lat},{lng}"}
    r = requests.get("https://www.mapquestapi.com/geocoding/v1/reverse", params=params)

    if r.status_code != 200:
        print("Incorrect data from GeoLocation API:", r.text)
        return "XZ", "Unknown", "Unknown"

    data = r.json()
    location = data["results"][0]["locations"][0]
    country = location["adminArea1"]
    state = location["adminArea3"]
    city = location["adminArea5"]
    return country, state, city


# Post message to Webex
def post_to_webex(room_id, access_token, message):
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    data = {"roomId": room_id, "text": message}
    r = requests.post(
        "https://webexapis.com/v1/messages",
        data=json.dumps(data),
        headers=headers
    )
    if r.status_code != 200:
        print("Error posting to Webex:", r.text)


# Main program
def main():
    access_token = get_access_token()
    rooms = get_webex_rooms(access_token)
    room_id = choose_room(rooms)
    geo_key = "KwKBVRqxrNymzfugaM6M5nhUSxNYwIYY"

    print("Monitoring room for /seconds messages....\n")

    while True:
        time.sleep(2)
        message = get_latest_message(room_id, access_token)
        if not message:
            continue

        print(f"Received message: {message}")

        if message.startswith("/"):
            if message[1:].isdigit():
                seconds = int(message[1:])
                if seconds > 5:
                    seconds = 5

                time.sleep(seconds)
                lat, lng, timestamp = get_iss_location()
                if not lat or not lng:
                    continue

                timeString = time.ctime(timestamp)
                country, state, city = get_location_from_coords(lat, lng, geo_key)

                if country == "XZ":
                    response = f"On {timeString}, the ISS was flying over a body of water at latitude {lat}° and longitude {lng}°."
                else:
                    response = f"On {timeString}, the ISS was flying over {city}, {state}, {country} ({lat}°, {lng}°)."

                print("Sending to Webex:", response)
                post_to_webex(room_id, access_token, response)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped by user.")