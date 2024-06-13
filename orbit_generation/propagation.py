# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/07_propagation.ipynb.

# %% auto 0
__all__ = ['RELATIVE_TOLERANCE', 'ABSOLUTE_TOLERANCE', 'jacobi_constant', 'eom_cr3bp', 'prop_node', 'jacobi_test',
           'dynamics_defect', 'calculate_errors']

# %% ../nbs/07_propagation.ipynb 3
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from typing import Tuple, List, Dict, Optional

# %% ../nbs/07_propagation.ipynb 6
RELATIVE_TOLERANCE = 1e-8
ABSOLUTE_TOLERANCE = 1e-8

# %% ../nbs/07_propagation.ipynb 8
def jacobi_constant(X: np.ndarray,  # Cartesian state vector with 6 components (x, y, z, xp, yp, zp)
                    mu: float  # Gravitational parameter
                   ) -> Tuple[float, float]:
    """
    State-dependent Jacobi constant for a given state vector X and gravitational parameter mu.

    Parameters:
    X (np.ndarray): Cartesian state vector with 6 components (x, y, z, xp, yp, zp).
    mu (float): Gravitational parameter.

    Returns:
    Tuple[float, float]: Jacobi constant (J) and total energy (E).
    """
    if len(X) != 6:
        raise TypeError("Define a state vector of length 6")

    # Unpack state vector components
    x, y, z, xp, yp, zp = X
    
    # Compute distances to the primary and secondary bodies
    mu1 = 1 - mu
    mu2 = mu
    r1 = np.sqrt((x + mu2)**2 + y**2 + z**2)
    r2 = np.sqrt((x - mu1)**2 + y**2 + z**2)

    # Calculate kinetic energy
    K = 0.5 * (xp**2 + yp**2 + zp**2)

    # Calculate the effective potential energy
    Ubar = -0.5 * (x**2 + y**2) - mu1 / r1 - mu2 / r2 - 0.5 * mu1 * mu2
    # Note: The last term is not used in the NASA database for the Jacobi constant computation. We adopt the complete convention.

    # Total energy
    E = K + Ubar

    # Jacobi constant
    J = -2 * E

    return J, E

# %% ../nbs/07_propagation.ipynb 12
def eom_cr3bp(t: float,  # Time variable (not used in this formulation)
              X: np.ndarray,  # State vector with 6 components (x, y, z, v_x, v_y, v_z)
              mu: float  # Gravitational parameter
             ) -> List[float]:
    """
    Equations of motion for the Circular Restricted 3 Body Problem (CR3BP). 
    The form is X_dot = f(t, X, (parameters,)). This formulation is time-independent 
    as it does not depend explicitly on t.
    
    Parameters:
    t (float): Time variable (not used in this formulation).
    X (np.ndarray): State vector with 6 components (x, y, z, v_x, v_y, v_z).
    mu (float): Gravitational parameter.

    Returns:
    List[float]: Derivatives of the state vector.
    """
    
    # Unpack state vector components
    x, y, z, v_x, v_y, v_z = X

    # Position of spacecraft with respect to primary bodies
    r1 = np.sqrt((x + mu)**2 + y**2 + z**2)
    r2 = np.sqrt((x - (1 - mu))**2 + y**2 + z**2)
    
    # State ODE:
    x_dot  = v_x
    y_dot  = v_y
    z_dot  = v_z
    x_ddot = x + 2 * v_y - (1 - mu) * (x + mu) / r1**3 - mu * (x - (1 - mu)) / r2**3
    y_ddot = y - 2 * v_x - y * ((1 - mu) / r1**3 + mu / r2**3)
    z_ddot = -z * ((1 - mu) / r1**3 + mu / r2**3)

    # Return the state derivatives as a list
    Xdot = [x_dot, y_dot, z_dot, x_ddot, y_ddot, z_ddot]
   
    return Xdot

# %% ../nbs/07_propagation.ipynb 15
def prop_node(X: np.ndarray,  # Initial state vector with 6 components (x, y, z, v_x, v_y, v_z)
              dt: float,  # Time step for propagation
              mu: float  # Gravitational parameter
             ) -> np.ndarray:
    """
    Return the state X after a given time step dt = T_end - T_start.
    
    Parameters:
    X (np.ndarray): Initial state vector with 6 components (x, y, z, v_x, v_y, v_z).
    dt (float): Time step for propagation.
    mu (float): Gravitational parameter.
    
    Returns:
    np.ndarray: Final state vector after time step dt.
    """
    # Solve the initial value problem using the eom_cr3bp function
    sol = solve_ivp(
        eom_cr3bp, [0, dt], X, args=(mu,), dense_output=True,
        rtol=RELATIVE_TOLERANCE, atol=ABSOLUTE_TOLERANCE, method='Radau'
    )
    
    # Return the final state vector
    return sol.y.T[-1]

# %% ../nbs/07_propagation.ipynb 18
def jacobi_test(X: np.ndarray,  # State vector with shape (n, 6) or (n, 7), where n is the number of samples
                mu: float  # Gravitational parameter
               ) -> float:
    """
    Compute the energy error. X can have either 6 columns (state vector) or 7 columns (time + state vector).
    The returned quantity is the cumulative error with respect to the initial value. If propagation is perfect, err = 0 (or very small).
    
    Parameters:
    X (np.ndarray): State vector with shape (n, 6) or (n, 7), where n is the number of samples.
    mu (float): Gravitational parameter.
    
    Returns:
    float: Cumulative energy error with respect to the initial value.
    """
    n, k = np.shape(X)
    
    # Initial Jacobi constant
    J0 = jacobi_constant(X[0, (k-6):k], mu)[0]
    
    err = 0.0
    # Compute cumulative error
    for i in range(n):
        Ji = jacobi_constant(X[i, (k-6):k], mu)[0]
        err += np.abs(J0 - Ji)
    
    return err

# %% ../nbs/07_propagation.ipynb 19
def dynamics_defect(X: np.ndarray,  # Time-state vector with shape (n, 7), where the first column is the time vector
                    mu: float  # Gravitational parameter
                   ) -> Tuple[float, float]:
    """
    Compute the dynamical defect for the generated time-state sequence. 
    The returned quantity is the cumulative error on the position and velocity components.
    The overall metrics can be a combination of these two last errors.
    
    Parameters:
    X (np.ndarray): Time-state vector with shape (n, 7), where the first column is the time vector.
    mu (float): Gravitational parameter.
    
    Returns:
    Tuple[float, float]: Cumulative errors in position and velocity.
    """
    n, m = np.shape(X)
    if m != 7:
        raise TypeError("X must be of size (n, 7). The first column is the time vector.")
    
    errX = 0.0  # Error in the position vector
    errV = 0.0  # Error in the velocity vector

    for i in range(n - 1):
        X_start = X[i, 1:7]
        X_end = X[i + 1, 1:7]
        dt = X[i + 1, 0] - X[i, 0]
        X_test = prop_node(X_start, dt, mu)
        err = X_test - X_end

        errX += np.linalg.norm(err[0:3])
        errV += np.linalg.norm(err[3:6])
    
    return errX, errV

# %% ../nbs/07_propagation.ipynb 21
def calculate_errors(orbit_data: np.ndarray,  # 3D array of orbit data
                     mu: float,  # Gravitational parameter
                     orbit_indices: List[int] = None,  # List of integers referring to the orbits to analyze
                     error_types: List[str] = ['position', 'velocity', 'energy'],  # Types of errors to calculate
                     time_step: Optional[float] = None,  # Optional time step if time dimension is not included
                     display_results: bool = True  # Boolean to control whether to display the results
                    ) -> Dict[str, Tuple[float, float]]:
    """
    Calculate and return the cumulative error and the average error per time step
    for the selected orbits together. Optionally, display the evolution of each error as a chart.
    
    Parameters:
    orbit_data (np.ndarray): 3D array of orbit data.
    mu (float): Gravitational parameter.
    orbit_indices (List[int], optional): List of integers referring to the orbits to analyze. 
                                         If None, analyze all orbits. Default is None.
    error_types (List[str]): List of types of errors to calculate: 'position', 'velocity', and/or 'energy'.
    time_step (float, optional): Optional time step if time dimension is not included. Default is None.
    display_results (bool, optional): Whether to display the results as charts. Default is True.
    
    Returns:
    Dict[str, Tuple[float, float]]: A dictionary with keys being the error types and values being
                                     tuples of cumulative error and average error per time step.
    """
    if orbit_indices is None:
        orbit_indices = list(range(orbit_data.shape[0]))

    # Check if the time dimension is included in the data
    if orbit_data.shape[1] == 6 and time_step is not None:
        num_time_points = orbit_data.shape[2]
        tvec = np.linspace(0, num_time_points * time_step, num_time_points + 1)
        orbit_data_with_time = np.zeros((orbit_data.shape[0], 7, num_time_points))
        orbit_data_with_time[:, 1:, :] = orbit_data
        for i in range(num_time_points):
            orbit_data_with_time[:, 0, i] = tvec[i]
        orbit_data = orbit_data_with_time
    elif orbit_data.shape[1] != 7:
        raise ValueError("Invalid orbit_data shape. Must be (n, 6, m) or (n, 7, m)")

    errors = {}
    
    for error_type in error_types:
        cumulative_error = 0.0
        error_evolution = np.zeros(orbit_data.shape[2] - 1)
        
        for idx in orbit_indices:
            selected_orbit = orbit_data[idx, :, :].T  # Transpose to shape (num_time_points, 7)
            tvec = selected_orbit[:, 0]  # Time vector for the current orbit

            # Ensure the time vector is strictly increasing
            if not np.all(np.diff(tvec) > 0):
                raise ValueError("Time vector is not strictly increasing.")

            if error_type == 'position':
                pos_error, _ = dynamics_defect(selected_orbit, mu)
                cumulative_error += pos_error
                for i in range(len(tvec) - 1):
                    dt = tvec[i + 1] - tvec[i]
                    X_start = selected_orbit[i, 1:]
                    X_end = selected_orbit[i + 1, 1:]
                    X_test = prop_node(X_start, dt, mu)
                    error_evolution[i] += np.linalg.norm(X_test[:3] - X_end[:3])
                    
            elif error_type == 'velocity':
                _, vel_error = dynamics_defect(selected_orbit, mu)
                cumulative_error += vel_error
                for i in range(len(tvec) - 1):
                    dt = tvec[i + 1] - tvec[i]
                    X_start = selected_orbit[i, 1:]
                    X_end = selected_orbit[i + 1, 1:]
                    X_test = prop_node(X_start, dt, mu)
                    error_evolution[i] += np.linalg.norm(X_test[3:] - X_end[3:])
                    
            elif error_type == 'energy':
                energy_error = jacobi_test(selected_orbit[:, 1:], mu)
                cumulative_error += energy_error
                for i in range(len(tvec) - 1):
                    Ji_start = jacobi_constant(selected_orbit[i, 1:], mu)[0]
                    Ji_end = jacobi_constant(selected_orbit[i + 1, 1:], mu)[0]
                    error_evolution[i] += np.abs(Ji_start - Ji_end)
                    
            else:
                raise ValueError("Invalid error type. Choose from 'position', 'velocity', or 'energy'.")
        
        avg_error_per_timestep = cumulative_error / (orbit_data.shape[2] - 1)
        
        if display_results:
            print(f"Cumulative {error_type} error for selected orbits: {cumulative_error}")
            print(f"Average {error_type} error per time step: {avg_error_per_timestep}")
            
            # Display the error evolution as a chart
            plt.figure(figsize=(10, 6))
            plt.plot(range(len(error_evolution)), error_evolution, label=f'{error_type.capitalize()} Error Evolution')
            plt.xlabel('Timestep Index')
            plt.ylabel(f'{error_type.capitalize()} Error')
            plt.title(f'{error_type.capitalize()} Error Evolution Over Timesteps')
            plt.legend()
            plt.grid(True)
            plt.show()
        
        errors[error_type] = (cumulative_error, avg_error_per_timestep)
    
    return errors
