import threading
import time
import pygame
import serial
import cv2
from flask import Flask, render_template, Response, request

# Initialize Flask app for video streaming
app = Flask(__name__)

# Serial setup for Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)  # Adjust to your serial port
time.sleep(2)  # Wait for Arduino to initialize

# Initialize pygame and attempt joystick setup
joystick_connected = False
pygame.init()
pygame.joystick.init()

try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    joystick_connected = True
    print("Joystick initialized.")
except pygame.error as e:
    print("No joystick detected. Web-only control enabled.")

# Camera setup (USB camera)
video_capture = cv2.VideoCapture(0)

# Define functions for video streaming
def generate_frames():
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/monitor')
def monitor_view():
    return render_template('monitor.html')

# Define function for joystick control
def joystick_control():
    def map_joystick_to_command():
        y_axis = joystick.get_axis(1)
        x_axis = joystick.get_axis(0)

        if y_axis < -0.5:
            return 'F'
        elif y_axis > 0.5:
            return 'B'
        elif x_axis < -0.5:
            return 'L'
        elif x_axis > 0.5:
            return 'R'
        else:
            return 'S'

    while True:
        pygame.event.pump()
        command = map_joystick_to_command()
        if command != 'S':
            arduino.write(command.encode())
            print(f"Sent command: {command}")
        time.sleep(0.1)

# Start joystick thread only if joystick is connected
if joystick_connected:
    joystick_thread = threading.Thread(target=joystick_control)
    joystick_thread.daemon = True
    joystick_thread.start()

# Handle motion control from web app (HTTP requests)
@app.route('/move', methods=['POST'])
def move_robot():
    action = request.form['action']
    print(f"Received action: {action}")
    arduino.write(action.encode())  # Send command to Arduino
    return '', 204

# Run the Flask app in the main thread
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
