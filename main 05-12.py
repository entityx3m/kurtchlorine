import time
from phsensor import read_ph_level
from test_water_level import water_distance
from test_flow_rate import water_flow
from chlorineAI import predict_solenoid_opening_time

def open_solenoid_valve(open_time_seconds):
    print(f"Opening solenoid valve for {open_time_seconds} seconds.")

def main():
    timer_duration = 3
    timer_start = time.time()
    rain_detected = False

    while True:
        # Check if rainwater is pouring (using flowrate sensor)
        if water_flow() > 0.5:
            rain_detected = True
            timer_start = time.time()  # Reset timer
            print("Rainwater detected. Timer reset.")

        # If rain detected and timer expired, perform AI prediction and open solenoid valve
        if rain_detected and time.time() - timer_start >= timer_duration:
            print("Timer expired. Performing AI prediction.")

            # Read sensor data
            water_level = water_distance()
            ph_level = read_ph_level()

            # Perform AI prediction for solenoid opening time based on water level
            predicted_time = predict_solenoid_opening_time(water_level, ph_level)
            print(f'Water Level: {water_level} L')
            print(f'pH Level: {ph_level}')
            print(f'Predicted Solenoid Opening Time: {predicted_time} seconds')

            # Open solenoid valve for the predicted time
            open_solenoid_valve(predicted_time)

            # Reset rain detection and timer
            rain_detected = False
            timer_start = time.time()
            print("Process Complete.")

        time.sleep(1)


if __name__ == "__main__":
    main()