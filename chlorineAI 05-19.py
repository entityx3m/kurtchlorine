import pandas as pd
from sklearn.tree import DecisionTreeRegressor

def predict_solenoid_opening_time(water_level_difference, ph_level):
    data = pd.read_csv('C:/Users/Kurt/PycharmProjects/pythonProject1/venv/chlorinepH.csv')
    X = data[['water_level_distance', 'pH_level']]
    y = data['chlorine']

    model = DecisionTreeRegressor()
    model.fit(X, y)

    new_data = pd.DataFrame({'water_level_distance': [water_level_difference], 'pH_level': [ph_level]})

    predicted_opening_time = model.predict(new_data)[0]

    return water_level_difference, ph_level, predicted_opening_time
