import pygame
import serial
import time

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()

# Initialize serial connection to Arduino (replace with your serial port)
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # Wait for Arduino to initialize

# Initialize joystick (use first joystick if connected)
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Function to map joystick input to motor commands
def map_joystick_to_command():
    x_axis = joystick.get_axis(0)  # Get X axis (left-right)
    y_axis = joystick.get_axis(1)  # Get Y axis (forward-backward)
    
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

# Main loop
try:
    while True:
        pygame.event.pump()  # Process joystick events
        command = map_joystick_to_command()

        if command != 'S':  # Don't send 'S' if nothing changed
            arduino.write(command.encode())  # Send command to Arduino
            print(f"Sent command: {command}")

        time.sleep(0.1)  # Poll every 100 ms

except KeyboardInterrupt:
    print("Exiting...")

finally:
    arduino.close()
    pygame.quit()
