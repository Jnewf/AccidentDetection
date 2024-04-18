import numpy as np
import traci

def kalman_filter_predict(vehicle_id, initial_state, initial_covariance, time_delta, acceleration=0):
    """
    Predicts the future state of a vehicle using the Kalman Filter and real-time data from SUMO via TraCI.

    Args:
        vehicle_id (str): The ID of the vehicle in the SUMO simulation.
        initial_state (np.array): The initial state vector of the vehicle [position, speed].
        initial_covariance (np.array): The initial covariance matrix of the state.
        time_delta (float): The time interval for prediction in seconds.
        acceleration (float): The acceleration of the vehicle (assumed to be constant).

    Returns:
        np.array: The predicted state vector of the vehicle.
        np.array: The predicted covariance matrix of the state.
    """
    # State transition matrix
    A = np.array([[1, time_delta], [0, 1]])

    # Control input model
    B = np.array([0.5 * (time_delta ** 2), time_delta])

    # Measurement matrix
    H = np.array([[1, 0]])

    # Process noise covariance
    Q = np.array([[1e-4, 0], [0, 1e-4]])

    # Measurement noise covariance
    R = np.array([[1e-2]])

    # Predict state estimate
    predicted_state = np.dot(A, initial_state) + B * acceleration

    # Predict covariance estimate
    predicted_covariance = np.dot(np.dot(A, initial_covariance), A.T) + Q

    # Get measurement (position)
    measurement = np.array([traci.vehicle.getPosition(vehicle_id)[0]])

    # Calculate Kalman gain
    innovation_covariance = np.dot(np.dot(H, predicted_covariance), H.T) + R
    kalman_gain = np.dot(np.dot(predicted_covariance, H.T), np.linalg.inv(innovation_covariance))

    # Update state estimate with measurement
    innovation = measurement - np.dot(H, predicted_state)
    updated_state = predicted_state + np.dot(kalman_gain, innovation)

    # Update covariance estimate
    updated_covariance = np.dot(np.eye(2) - np.dot(kalman_gain, H), predicted_covariance)

    return updated_state, updated_covariance