from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import socket
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temperature_data.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    timestamp = db.Column(db.Float)
    room = db.Column(db.Integer)


# Moved db.create_all() inside the app context
with app.app_context():
    db.create_all()

UDP_IP = "192.168.46.66"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def listen_for_data():
    while True:
        data, addr = sock.recvfrom(1024) 
        temp, humidity, timestamp, room = map(float, data.decode().split(","))        
        new_data = Data(client=str(addr), temperature=temp, humidity=humidity, timestamp=timestamp, room=room)
        with app.app_context():  # also wrap database operations inside the app context
            db.session.add(new_data)
            db.session.commit()

        # Prints the data to the console
        print(f"Data received from client: {str(addr)}")
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")

@app.route('/')
def index():
    # Query all data from the database
    all_data = Data.query.all()

    # Group by room
    rooms = {}
    for entry in all_data:
        if entry.room not in rooms:
            rooms[entry.room] = []
        rooms[entry.room].append(entry)

    # Render the data using a template
    return render_template('index.html', rooms=rooms)


def run_flask():
    app.run(host="192.168.46.66", port=8888)
    
if __name__ == "__main__":
    # Starting Flask on a separate thread
    thread = threading.Thread(target=run_flask)
    thread.start()
    
    # Running the UDP listener
    listen_for_data()