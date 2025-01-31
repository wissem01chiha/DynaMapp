import numpy as np 
from scipy.linalg import solve_discrete_are
from scipy.signal import place_poles

def solveAlgebraicRiccatiEquation(A, B, Q, R):
    """
    Solve the discrete time algebric riccati equation given by :
    
    Args: 
        - A, B  : System
    Returns:
        - P ARE solution. 
    """
    assert A.shape[0] == A.shape[1],"Matrix A must be square."
    assert B.shape[0] == A.shape[0],"Matrix B must have the same number of rows as A."
    assert Q.shape[0] == Q.shape[1] == A.shape[0],"Matrix Q must be square and match the dimensions of A."
    assert R.shape[0] == R.shape[1] == B.shape[1],"Matrix R must be square and match the number of columns of B."
    
    P  =  solve_discrete_are(A, B, R, Q)
    return P

def solve_discrete_state_depend_are(A, B, Q, R):
    """ 
    Solve the discrete state depend Riccati equation 
    Ref:
    
    """

def luenbergerObserver(A, B, C, desired_poles):
    """
    Computes the Luenberger Observer gain matrix L.

    Args::
        A (np.ndarray): System matrix.
        B (np.ndarray): Input matrix.
        C (np.ndarray): Output matrix.
        desired_poles (list): Desired poles for the observer.

    Returns:
        L (np.ndarray): Observer gain matrix.
    """
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    assert A.shape[0] == A.shape[1], "Matrix A must be square."
    assert B.shape[0] == A.shape[0], "The number of rows in B must match the number of rows in A."
    assert C.shape[1] == A.shape[0], "The number of columns in C must match the number of rows in A."
    At = A.T
    Ct = C.T
    placed_poles = place_poles(At, Ct, desired_poles)
    Lt = placed_poles.gain_matrix
    L = Lt.T
    
    return L

