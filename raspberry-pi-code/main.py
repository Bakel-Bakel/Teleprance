import threading
import time
import pygame
import serial
import cv2
from flask import Flask, render_template, Response

# Initialize Flask app for video streaming
app = Flask(__name__)

# Serial setup for Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)  # Adjust to your serial port
time.sleep(2)  # Wait for Arduino to initialize

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

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

# Define function for joystick control
def joystick_control():
    def map_joystick_to_command():
        y_axis = joystick.get_axis(1)  # Y-axis (up-down)
        x_axis = joystick.get_axis(0)  # X-axis (left-right)

        if y_axis < -0.5:  # Move Forward
            return 'F'
        elif y_axis > 0.5:  # Move Backward
            return 'B'
        elif x_axis < -0.5:  # Turn Left
            return 'L'
        elif x_axis > 0.5:  # Turn Right
            return 'R'
        else:  # Stop
            return 'S'

    while True:
        pygame.event.pump()
        command = map_joystick_to_command()
        if command != 'S':
            arduino.write(command.encode())  # Send command to Arduino
            print(f"Sent command: {command}")
        time.sleep(0.1)  # Poll every 100 ms

# Run the joystick control function in a separate thread
joystick_thread = threading.Thread(target=joystick_control)
joystick_thread.daemon = True  # Ensure it exits when the main program exits
joystick_thread.start()

# Run the Flask app in the main thread
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
