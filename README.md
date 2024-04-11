# AccidentDetection

Our project aims to address the critical issue of road safety in the fast-paced world of vehicular transportation by developing an advanced crash analysis module. This module leverages trajectory information from remote vehicle systems and utilizes various crash detection algorithms to predict and prevent vehicular accidents effectively.

## Progress Summary:
Data Collection: We have set up a simulation environment using SUMO to generate and collect trajectory data from virtual vehicles under various traffic conditions.

Algorithm Implementation: Two vehicle tracking methods have been implemented for state estimation: the Constant Speed Model and the Kalman Filter. These models are crucial for predicting vehicle positions and assessing crash risks.

Crash Detection Logic: Preliminary crash detection logic has been integrated to evaluate the efficacy of the tracking models in detecting potential collisions.

Simulation and Testing: The implemented models and crash detection logic have been tested in the simulation environment, providing initial insights into their performance and effectiveness.

## Files and Scripts:
accident_detection_compare_tracking_methods.py: Main script for running the simulation and comparing tracking methods. (note - not needed, can compare tracking methods using the logs from the following two scripts)

accident_detection_kalman.py: Main script for running the simulation with Kalman filter as the chosen vehicle tracking method.

accident_detection_constant.py: Main script for running the simulation with Kalman filter as the chosen vehicle tracking method.

constant_speed_model.py & kalman_filter.py: Implementation of the Constant Speed Model and the Kalman Filter, respectively.

accident.net.xml, accident.rou.xml, accident.settings.xml, accident.sumocfg: SUMO configuration files defining the network, vehicle routes, settings, and overall simulation setup.

## Challenges Encountered:
Model Differentiation: The predictions from the Constant Speed Model and the Kalman Filter have been found to be identical under the current simulation settings, indicating a need for further refinement to introduce more variability in traffic scenarios.

## Next Steps:

### Refine Tracking Models:

Enhance the Kalman Filter to more effectively utilize acceleration data and process noise, ensuring it captures the dynamics of vehicle motion more accurately than the simpler Constant Speed Model.
Review and adjust the Constant Speed Model to ensure it operates under its intended assumptions.

### Enhance Traffic Scenarios:

Introduce more variability in the simulation environment, such as dynamic traffic light changes, road closures, and variable speed limits, to test the models under more diverse and challenging conditions.

### Advanced Crash Detection Logic:

Develop more sophisticated crash detection algorithms that can utilize the state estimates from the tracking models to predict collisions more accurately.
Incorporate machine learning techniques to analyze the trajectory data, aiming to improve prediction accuracy and reduce false negatives.

### Data Analysis and Model Comparison:

Conduct a thorough analysis of the simulation data to compare the performance of the Constant Speed Model and the Kalman Filter in various traffic scenarios.
Utilize metrics such as prediction accuracy, false positive rates, and computational efficiency to evaluate and compare the models.

### Prototype Development:

Focus on integrating the refined tracking models and crash detection algorithms into a cohesive prototype that can be easily demonstrated within the SUMO simulation environment. The emphasis should be on illustrating how the models work in concert to predict and detect potential crash scenarios.

Prioritize testing and validation within the simulation environment to ensure the prototype effectively demonstrates the desired functionalities, such as vehicle tracking accuracy, collision prediction, and the effectiveness of crash detection under various simulated traffic conditions.

Develop a set of predefined scenarios within the simulation that highlight the strengths and capabilities of the prototype. These scenarios could include challenging traffic conditions, such as high-density traffic, rapid speed variations, and complex intersection dynamics, to showcase how the system performs under different conditions.

### Documentation and Reporting:

Document all developments, including code changes, algorithm designs, and test results.
Prepare a comprehensive report detailing the project methodology, findings, and recommendations for future enhancements.

## Conclusion:
The foundation laid by the current project efforts provides a solid basis for further development and refinement. By addressing the outlined next steps, the project aims to achieve a sophisticated crash analysis module capable of effectively predicting and preventing vehicular accidents, contributing to safer roads and saving lives.
