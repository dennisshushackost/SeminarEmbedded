# SeminarEmbedded


## Clinet
For the client application the following technology stack was used:
1. Adafruit Python SSD1306 library for Using the oled screen for the pico board 
2. Smbus for the temperture & humidty sensor

The client grabs the current temp & humidty every 5 seconds, displays it on the screen and sends this information to a central server via a UDP socket. Each client represents a specific room.

## Server:
The server receives the data from the different clients and displays it on a webinterface. The technology stack includes:
1. A persistent Sqlite db.
2. Uses flask for displaying the data and running an API.
3. SQLAlchemy is used to simplify the database generation and querying.
4. The Flask application runs in parallel with the Socket connection (via Thread)
