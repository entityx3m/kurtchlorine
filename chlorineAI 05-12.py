import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from phsensor import read_ph_level
from test_water_level import water_distance
import time

def predict_solenoid_opening_time():

    data = pd.read_csv('C:/Users/Kurt/PycharmProjects/pythonProject1/venv/chlorinepH.csv')
    X = data[['water_level_distance', 'pH_level']]
    y = data['chlorine']

    model = DecisionTreeRegressor()
    model.fit(X, y)

    water_level = water_distance()
    ph_level = read_ph_level()

    new_data = pd.DataFrame({'water_level_distance': [water_level], 'pH_level': [ph_level]})

    predicted_opening_time = model.predict(new_data)[0]

    time.sleep(1)

    return water_level, ph_level, predicted_opening_time

 # Example usage
water_level, ph_level, predicted_time = predict_solenoid_opening_time()
print(f'Water Level: {water_level} L')
print(f'pH Level: {ph_level}')
print(f'Predicted Solenoid Opening Time: {predicted_time} seconds')