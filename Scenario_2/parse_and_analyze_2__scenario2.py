import xml.etree.ElementTree as ET
import logging
import pandas as pd
import matplotlib.pyplot as plt  # Import matplotlib for plotting
# Set option to display all columns
pd.set_option('display.max_columns', None)
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def parse_collision_log(filename):
    """
    Parses the collision log XML to extract collision events.
    Args:
    filename (str): Path to the XML file containing collision data.
    Returns:
    list: A list of dictionaries, each representing a collision event.
    """
    collisions = []
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        for collision in root.findall('.//collision'):
            # TODO: Convert to numeric values
            collisions.append({
                "time": float(collision.get("time")),
                "type": collision.get("type"),
                "lane": collision.get("lane"),
                "pos": float(collision.get("pos")),
                "collider": collision.get("collider"),
                "victim": collision.get("victim"),
                "colliderType": collision.get("colliderType"),
                "victimType": collision.get("victimType"),
                "colliderSpeed": float(collision.get("colliderSpeed")),
                "victimSpeed": float(collision.get("victimSpeed"))
            })
    except ET.ParseError as e:
        logging.error(f"Error parsing the collision log file: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return collisions

def parse_simulation_log(filename):
    """
    Parses the simulation log to extract warnings about potential collisions.
    Args:
    filename (str): Path to the log file containing simulation data.
    Returns:
    list: A list of dictionaries, each containing information about a warning.
    """
    warnings = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if "collision warning" in line:
                    victim = None
                    collider = None

                    message = line[24:len(line)-1]

                    warning_info, vehicles = message.strip().split(":", 1)
                    collision_type = warning_info.replace("collision warning", "").strip()

                    if "leading" in vehicles:
                        vehicle_list = vehicles.split("leading") #rear-end
                    elif "and" in vehicles:
                        vehicle_list = vehicles.split("and") #side-swipe

                    for index, car in enumerate(vehicle_list):
                        vehicle_list[index] = car.replace(" ", "").strip()

                    if len(vehicle_list) < 3:
                        victim = vehicle_list[0]
                        collider = vehicle_list[1]
                    else:
                        logging.ERROR("Multi Car accident...")

                    date, time, number, *_ = time_extract(line)
                    # TODO: Convert these into numeric values
                    warnings.append({"date": date,
                                     "time":time,
                                     "number": number,
                                     "warning_info": warning_info,
                                     "victim": victim,
                                     "collider": collider,
                                     "collision_type": collision_type})

    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
    except Exception as e:
        logging.error(f"Error reading the simulation log file: {e}")

    return warnings

def parse_data_tracking_log(filename):
    """
    Parses the simulation data tracking methods log.
    Args:
    filename (str): Path to the log file containing simulation data.
    Returns:
    list: A list of dictionaries, each containing information about a warning.
    """
    warnings = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                message = line[24:len(line)-1]

                # Split the string by commas to separate the key-value pairs
                pairs = message.split(',')

                # Initialize variables to store parsed values
                vehicle_id = None
                cs_prediction = None
                kf_prediction = None

                # Iterate over each key-value pair
                for pair in pairs:
                    # Split each pair by colon to separate the key and value
                    key, value = pair.split(':')
                    
                    # Remove leading and trailing spaces from key and value
                    key = key.strip()
                    value = value.strip()
                    
                    # Check the key and assign the corresponding value to the appropriate variable
                    if key == 'vehicle_id':
                        vehicle_id = value
                    elif key == 'cs_prediction':
                        cs_prediction = float(value)
                    elif key == 'kf_prediction':
                        kf_prediction = float(value)

                date, time, number = time_extract(line)
                # TODO: Convert to numeric values
                warnings.append({"date": date,
                                 "time":time,
                                 "number": number,
                                 "vehicle_id": vehicle_id,
                                 "cs_prediction": cs_prediction,
                                 "kf_prediction": kf_prediction})

    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
    except Exception as e:
        logging.error(f"Error reading the simulation log file: {e}")
    return warnings

def time_extract(line):
    """
    Helper function to extract time from an input file, i.e.:
    2024-04-14 17:20:30,049
    """
    time_str = line[:19]
    number = line[20:23]

    timestamp_parsed = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

    year = timestamp_parsed.year
    month = timestamp_parsed.month
    day = timestamp_parsed.day

    hour = timestamp_parsed.hour
    minute = timestamp_parsed.minute
    second = timestamp_parsed.second
    # TODO: Maybe use the datetime.strptime to convert into a single time format, such as overall minutes or something
    date = "{}-{}-{}".format(year,month,day)
    time = "{}:{}:{}".format(hour,minute,second)

    return date, time, number

def analyze_algorithm(collisions, warnings):
    """
    Analyzes the effectiveness of the collision detection algorithm.
    Args:
    collisions (list): List of actual collisions parsed from the collision log.
    warnings (list): List of warnings generated by the simulation.
    """
    detected_collisions = 0
    for collision in collisions:
        for warning in warnings:
            if collision['collider'] in warning['collider'] and collision['victim'] in warning['victim']:
                detected_collisions += 1
                break
    total_collisions = len(collisions)
    precision = detected_collisions / total_collisions if total_collisions > 0 else 0
    print(f"Detected Collisions: {detected_collisions}")
    print(f"Total Collisions: {total_collisions}")
    print(f"Precision: {precision:.2f}")



def create_data_frame(data, graph=False):
    """
    Helper function to help create a dataframe.
    Args:
    data (list): List of the data intended to be used for the data frame
    graph (boolean): Variable used to plot the data frame
    """
    if data is None:
        print("No data provided.")
        return None

    data_frame = pd.DataFrame(data)
    print(data_frame)

    if graph:
        if 'time' in data_frame.columns and 'pos' in data_frame.columns:  # Ensure columns exist for plotting
            data_frame.plot(x='pos', y='time', kind='line', title='Time vs Position Plot')
            plt.show()  # Display the plot
        else:
            print("Required columns for plotting are missing.")

    return data_frame

def collisions_ML_model(data):
    """
    Collisions ML model, reads the collisions input file to make a prediction
    Args:
    data (list): List of the data intended to be used for the data frame
    """
    if data is None:
        print("No data provided.")
        return

    collision_df = create_data_frame(data)
    if collision_df is None or not {'time', 'pos', 'colliderSpeed', 'victimSpeed', 'type'}.issubset(collision_df.columns):
        print("Dataframe is missing one or more required columns.")
        return

    # Encode 'type' as numeric: 'accident' = 1, 'collision' = 0
    collision_df['type'] = (collision_df['type'] == 'accident').astype(int)

    # Selecting features and target
    X = collision_df[['time', 'pos', 'colliderSpeed', 'victimSpeed']]
    y = collision_df['type']

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize and train the Logistic Regression model
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)

    # Predictions and evaluation
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)



if __name__ == "__main__":
    collisions = parse_collision_log('collision_log_scenario2.txt')
    kalman_warnings = parse_simulation_log('simulation_data_kalman_scenario2.log')
    constant_warnings = parse_simulation_log('simulation_data_constant_scenario2.log')
    data_tracking_log = parse_data_tracking_log('simulation_data_tracking_methods_scenario2.log')

    print("Kalman Filter Analysis:")
    analyze_algorithm(collisions, kalman_warnings)

    print("\nConstant Speed Model Analysis:")
    analyze_algorithm(collisions, constant_warnings)

    # using pandas
    print("\n\nCollision Dataframe:")
    collisions_df = pd.DataFrame(collisions)
    print(collisions_df)
    
    print("Simulation Data Kalman Dataframe:")
    kalman_df = pd.DataFrame(kalman_warnings)
    print(kalman_df)

    print("Simulation Data Constant Dataframe:")
    constant_df = pd.DataFrame(constant_warnings)
    print(constant_df)

    print("Simulation Data Tracking Dataframe:")
    data_tracking_df = pd.DataFrame(data_tracking_log)
    print(data_tracking_df)

    # print("\n\nCollision Dataframe:")
    # collisions_df = create_data_frame(collisions, graph=True)  # Set graph=True to display the plot

    collisions_ML_model(collisions) # TODO: Not working, need to fix input data to be numeric values