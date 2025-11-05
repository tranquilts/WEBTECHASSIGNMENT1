# ISS Tracker + Webex Space Bot

# Import libraries for API requests, JSON formatting, epoch time conversion, and iso3166.
import requests
import json
import time
from iso3166 import countries


#Use Webex Token
def get_access_token():
    choice = input("Do you wish to use the hard-coded Webex token? (y/n):  ")
    if choice.lower() == "y":
        return "Bearer " + input("Enter your Webex Access Token: ")
    else:
        return "Bearer MGVkYjVhZmQtZGY2Ni00YjgwLWFiZWMtNDRmNjhiNzRjZWIyYTZkNGU1ZjktMDhi_P0A1_251b8f7b-fbc7-4534-b240-867707e063a8"


#Get Webex rooms
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


# Choose a room
def choose_room(rooms):
    print("\nAvailable rooms:")
    for i, room in enumerate(rooms):
        print(f"{i + 1}. {room['title']}")

    while True:
        room_name = input("Enter room number or title to monitor: ")
        # Allow user input by number
        if room_name.isdigit():
            index = int(room_name) - 1
            if 0 <= index < len(rooms):
                return rooms[index]["id"]

        # Or by user input of the title text given
        for room in rooms:
            if room_name.lower() in room["title"].lower():
                return room["id"]

        print("Room not found. Please try again.")


# Get latest message from Webex Rooms
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

    message_data = data["items"][0]

    #Ignore messages sent by the bot itself
    if "bot" in message_data["personEmail"]:
        return None

    return message_data["text"]


# 6. Get ISS location
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


# 7. Convert coordinates to readable location
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


# 8. Post to Webex
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
        print("Incorrect posting to Webex:", r.text)


# 9. Main bot logic
def main():
    access_token = get_access_token()
    rooms = get_webex_rooms(access_token)
    room_id = choose_room(rooms)
    geo_key = "KwKBVRqxrNymzfugaM6M5nhUSxNYwIYY"

    print("\nMonitoring room for /seconds messages....\n")

    while True:
        time.sleep(2)
        message = get_latest_message(room_id, access_token)
        if not message:
            continue

        print(f"Received message: {message}")

        if message.startswith("/"):
            seconds = int(message[1:])
            if seconds > 5:
                seconds = 5

            time.sleep(seconds)
            lat, lng, timestamp = get_iss_location()
            if not lat or not lng:
                continue

            timeString = time.ctime(timestamp)
            country, state, city = get_location_from_coords(lat, lng, geo_key)

            # Formats clear ISS message output
            if country == "??":
                response = (
                    f"🌌 **ISS Tracker Update** 🌌\n"
                    f"🕒 Time: {timeString}\n"
                    f"🌊 The ISS was flying over a body of water.\n"
                    f"📍 Coordinates: ({lat}°, {lng}°)"
                )
            else:
                response = (
                    f"🌌 **ISS Tracker Update** 🌌\n"
                    f"🕒 Time: {timeString}\n"
                    f"📍 Location: {city}, {state}, {country}\n"
                    f"🛰 Coordinates: ({lat}°, {lng}°)"
                )

            print("Sending to Webex:", response)
            post_to_webex(room_id, access_token, response)
#Error message for messages not /seconds given from the provided range /1-/5
        else:
            reminder = "Please use `/seconds` (e.g., `/5`) to get the ISS location update."
            print("Sending reminder:", reminder)
            post_to_webex(room_id, access_token, reminder)


# 10. Run the bot and stops if user stops 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
