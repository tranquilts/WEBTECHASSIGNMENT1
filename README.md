# Space Bot

# Webex Messaging API 
|Criteria |Details|
----------|-------|
|API Base URL |https://webexapis.com
|Authentication Method| Bearer Token (Auth2.0)
|Endpoint in list rooms| /rooms
|Endpoint to get messages |GET /messages?roomID=<room_id
|Explanation | roomID is a query parameter to extract messages from and rooms creates Webex rooms for users to be invited to and collaborate.                                                  
|Endpoint to send messages |POST /messages
|Required headers |Authorization: Bearer <access_token>, Content Type: application/JSON
|Sample full GET or POST request | <img width="971" height="179" alt="image" src="https://github.com/user-attachments/assets/a3324878-c1ec-4d5d-8f9a-46971894d44b" >
|Explanation | The code extracts a list of all Webex rooms the user is a member of. This is used in Space Bot to show room options for monitoring purposes.


## ISS Current Location API 
|Criteria | Details |
----------|---------|
|API Base URL|api.open-notify.org
|Endpoint for current ISS location | http://api.open-notify.org/iss-now.json
|Sample response format |<img width="683" height="179" alt="image" src="https://github.com/user-attachments/assets/2d58774d-b899-4166-aadf-91ed74eb7496" />
|Explanation | Longitude and latitude are given to the API. Space Bot reads it and sends co-ordinates to the Geocoding API for location data. 



## Section 3: Geocoding API

|Criteria |Details |
----------|--------|
|Provider used | MapQuest
|API Base URL |https://www.mapquestapi.com/geocoding/v1/address
|Endpoint for reverse geocoding |http://www.mapquestapi.com/geocoding/v1/reverse
|Authentication method | Users must set up a free MapQuest Developer account and get an API key.
|Required query parameters |Key - the api key. Location - Co-ordinates for latitude, longitude
|Sample request with latitude/longitude|<img width="340" height="198" alt="image" src="https://github.com/user-attachments/assets/4dccb2d5-c54d-4df9-a460-7793382f3f1b" />
|Sample JSON response (formatted example) |<img width="340" height="893" alt="image" src="https://github.com/user-attachments/assets/8ead11f7-aac6-4801-9ac8-f0c584d82131" />
|Explanation | ISS GPS co-ordinates converts into a human-readable addresses (city, state, country) to format messages sent to Webex rooms. 


## Epoch to Time Conversion (Python time module)

|Criteria | Details|
----------|--------|
|Library used | Time
|Function used to convert epoch |time.localtime(), time.strftime()
|Sample code to convert timestamp|<img width="962" height="317" alt="image" src="https://github.com/user-attachments/assets/9c387b3a-8ca0-442c-aa52-0e8535d10a9e" />
|Output (human-readable code)|<img width="979" height="135" alt="image" src="https://github.com/user-attachments/assets/e52eb2cc-a864-4107-84b7-cc6a112ba7e1" />
|Explanation | The time library converts epoch timestamps from the ISS API into human-readable dates and times for messages. 


Web Architecture & MVC Design 
### Web Architecture - Server Client Model
Client Layer: Webex platform where hsers send /seconds commands.
Application Layer: Python script plays the role of a bot handling logic and API requests.
Presentation Layer: Webex room messages displays results to users. 


MVC Design

| Component | Description |
------------|-------------|
|Model       | Data handling (API responses for ISS and Geocoding).
|View        | Output messages displayed in Webex room.
|Controller  | Python code processes commands, manages timing and shows results.

  
