import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from dht11 import read_dht11_sensor_data
from Sensor import distance
import time

def predict_solenoid_opening_time():

data = pd.read_csv('chlorinerevamp.csv')
X = data[['water_level_distance', 'temperature', 'humidity']]
y = data['chlorine']

model = DecisionTreeRegressor(random_state=42)
model.fit(X, y)

    water_level = distance()
    temperature, humidity = read_dht11_sensor_data()

    new_data = pd.DataFrame({'water_level_distance': [water_level], 'temperature': [temperature], 'humidity': [humidity]})

    predicted_opening_time = model.predict(new_data)[0]

    time.sleep(1)

    return predicted_opening_time

# Example usage
predicted_time = predict_solenoid_opening_time()
print(f'Predicted Solenoid Opening Time: {predicted_time} seconds')
