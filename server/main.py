from flask import Flask, render_template
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
    timestamp = db.Column(db.Float)  # Changed to Float
    room = db.Column(db.Integer)

with app.app_context():
    db.create_all()

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def listen_for_data():
    while True:
        data, addr = sock.recvfrom(1024)
        temp, humidity, timestamp, room = map(float, data.decode().split(","))
        temp = round(temp, 2)
        humidity = round(humidity, 2)
        timestamp = round(timestamp, 2)
        new_data = Data(client=str(addr), temperature=temp, humidity=humidity, timestamp=timestamp, room=room)
        with app.app_context():
            db.session.add(new_data)
            db.session.commit()

        print(f"Data received from client: {str(addr)}")
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")

@app.route('/')
def index():
    rooms_data = {}
    room_ids = db.session.query(Data.room).distinct().all()
    for room_id in room_ids:
        latest_entry = Data.query.filter_by(room=room_id[0]).order_by(Data.timestamp.desc()).first()
        rooms_data[latest_entry.room] = latest_entry

    temps = [data.temperature for data in Data.query.order_by(Data.timestamp).all()]
    times = [str(data.timestamp) for data in Data.query.order_by(Data.timestamp).all()]

    return render_template('index.html', rooms=rooms_data, temps=temps, times=times)

def run_flask():
    app.run(host="0.0.0.0", port=8888)

if __name__ == "__main__":
    thread = threading.Thread(target=run_flask)
    thread.start()
    listen_for_data()
