#Different type of activation function and their derivatives to be used in the Artificial Neural Network

import numpy as np

##############################################################################

def sigmoid(x):
    """Definition of the sigmoid function
    
    Parameters
    ----------
    x : float
        Input of the sigmoid function.

    Returns
    -------
    TYPE : float
        Output of the sigmoid function.

    """
    x = np.where(x > -709, x, -709)    # Avoid problem of inf value in np.exp(x)
    return 1 / (1 + np.exp(-x))


def deriv_sigmoid(x):
    """Definition of the jacobian (trivial) of the sigmoid function
    
    Parameters
    ----------
    x : array-like
        Input of the derivative/jacobian of the sigmoid function. If the input is an integer or a float, convert it to a list.

    Returns
    -------
    jacobian : numpy array
        Jacobian matrix of the sigmoid function, evaluated for the input x; it is trivial because all the elements outside the principal diagonal are equal to zero.
        In the particular case of a float as input, the ouput will be a numpy mono-dimensional array with one element (the simple derivative).

    """
    lenght = np.size(x)
    x = np.array(x)
    i, j = np.indices((lenght, lenght))
    jacobian = np.where(i==j, sigmoid(x[i]) * (1 - sigmoid(x[i])), 0)
    return jacobian

##############################################################################

def softmax(x):
    """Definition of the softmax activation function
    
    Parameters
    ----------
    x : array-like
        Input of the softmax function.

    Returns
    -------
    TYPE : numpy array
        Output of the softmax function, same dimension of the input.

    """
    num = np.exp(x - np.max(x))
    den = np.sum(num)
    return num / den


def deriv_softmax(x):
    """Definition of the softmax function jacobian

    Parameters
    ----------
    x : array-like
        Input of the softmax function jacobian.

    Returns
    -------
    jacobian : numpy array
        Jacobian matrix of the softmax function, evaluated for the input x.

    """
    lenght = np.size(x)
    a = softmax(x)
    i, j = np.indices((lenght, lenght))
    jacobian = np.where(i==j, a[i] * (1 - a[i]), - a[i] * a[j])
    
    return jacobian

###############################################################################
