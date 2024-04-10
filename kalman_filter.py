import numpy as np
import traci

def kalman_filter_predict(vehicle_id, initial_covariance, time_delta, acceleration=0):
    """
    Predicts the future state of a vehicle using the Kalman Filter and real-time data from SUMO via TraCI.

    Args:
    vehicle_id (str): The ID of the vehicle in the SUMO simulation.
    initial_covariance (np.array): The initial covariance matrix of the state.
    time_delta (float): The time interval for prediction in seconds.
    acceleration (float): The acceleration of the vehicle (assumed to be constant).

    Returns:
    np.array: The predicted state vector of the vehicle.
    np.array: The predicted covariance matrix of the state.
    """
    initial_position = traci.vehicle.getPosition(vehicle_id)[0]  # X-axis position
    initial_speed = traci.vehicle.getSpeed(vehicle_id)
    initial_state = np.array([initial_position, initial_speed])

    # State transition matrix
    A = np.array([[1, time_delta], [0, 1]])
    # Control input model
    B = np.array([0.5 * (time_delta ** 2), time_delta])
    # Update state estimate
    updated_state = np.dot(A, initial_state) + B * acceleration
    # Simplified covariance update
    updated_covariance = np.dot(np.dot(A, initial_covariance), A.T)

    return updated_state, updated_covariance

