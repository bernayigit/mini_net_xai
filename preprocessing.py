import numpy as np
from sklearn import preprocessing

def dig_holes(matrix, positions, center):
    '''
    Replace values at specified positions with noise value -1, extracts the truth value at position to predict.
    
    Parameters
    ----------
    matrix: list or NDArray
        single traffic matrix to modify.
    positions: list
        list of tuples specifiying the positions whose value to replace with -1.
    center: tuple
        single position to be replaced with -1 and whose value is to be returned as truth value.
    
    Returns
    -------
    tuple
        tuple in the form of (missing_value_truth, new_matrix). the first is the ground truth value to serve as y in the training process,
        the second is the modified matrix representing the x.
    '''
    new_matrix = np.copy(matrix)
    missing_value_truth = new_matrix[center[0]][center[1]]
    for ((empty_i, empty_j)) in positions:
        new_matrix[empty_i][empty_j] = -1
    return missing_value_truth, new_matrix

def roll_around_coordinate(matrix, new_center):
    '''
    Center matrix around new_center.

    Parameters
    ----------
    matrix : list or NDArray
        single traffic matrix to recenter.
    new_center : tuple
        position to center matrix around.

    Returns
    -------
    numpy array
        recentered matrix
    '''
    matrix = np.array(matrix)
    old_center = (matrix.shape[0]//2, matrix.shape[1]//2)
    shift_y = (old_center[0]-new_center[0])
    shift_x = (old_center[1]-new_center[1])
    matrix = np.roll(matrix, shift_y, axis=0)
    matrix = np.roll(matrix, shift_x, axis=1)
    return matrix

def get_matrix_subset(matrix, y_coordinate, subset_coordinates):
    '''
    Collects a subset of values from the amtrix into a smaller one and extracts truth value from specified y coordinate.

    Parameters
    ----------
    matrix : list or NDArray
        original matrix.
    y_coordinate : tuple
        position (i,j) in original matrix to extract truth value from. 
    subset_coordinates : list
        list of tuples representing coordinates of value that constitute the new matrix.

    Returns
    -------
    tuple
        a tuple having y,x, where y is the truth value and x is the subset matrix.
    '''
    y = matrix[y_coordinate[0]][y_coordinate[1]]
    x = [matrix[coordinate[0]][coordinate[1]] for coordinate in subset_coordinates]
    return y, x

def fit_scaler(data):
    '''
    Fit a scaler to scale matrix data down to (1,10) range.

    Parameters
    ----------
    data: NDArray
        matrix data used to fit the scaler.

    Returns
    -------
    object
        fitted scaler.
    '''
    transformer = preprocessing.MinMaxScaler(feature_range=(1,10))
    nsamples, nx, ny = data.shape
    return transformer.fit(data.reshape(nsamples, nx * ny))  

def scale_data(scaler, data):
    '''
    Scale data down to (1,10) range

    Parameters
    ----------
    scaler: object
        sklearn preprocessing Scaler
    data: NDArray
        matrix data to scale down.

    Returns
    -------
    NDArray
        scaled data.
    '''
    nsamples, nx, ny = data.shape
    return scaler.transform(data.reshape(nsamples, nx * ny)).reshape((nsamples, nx, ny))  

def process_data(data, y_coordinate, missing_values_coordinates, train_test_split = 0.2, shuffle = True):
    '''
    Preprocess the list of traffic matrices, by extracting the value in the coordinate to predict, and centering the matrices around it. 

    Parameters
    ----------
    data : NDArray
        numpy array of traffic matrices.
    y_coordinate : tuple
        coordinate of the value to predict.
    missing_values_coordinates: list
        list of coordinates missing value measurement. Useful when testing performance in presence of noise or lack of more than one flow measurement.
        Should always include y_coordinate.
    train_test_split : float
        portion of data dedicated to testing purposes.  
    shuffle : bool
        whether to shuffle the data or not.

    Returns
    -------
    tuple
        a 4-tuple of numpy arrays in the form of (train_X, train_Y, test_X, test_Y).
    '''
    data_X = []
    data_Y = []
    for position in missing_values_coordinates:
        if position[0] >= data.shape[1] or position[1] >= data.shape[2]:
            raise ValueError(f'Specified position {y_coordinate} is out of bounds (matrix_shape = {data.shape}).')
    if shuffle == True:
        matrices = np.random.permutation(data)
    else:
        matrices = data
    for matrix in matrices:
        y, x = dig_holes(matrix, missing_values_coordinates, y_coordinate)
        data_Y.append(y)
        data_X.append(np.reshape(roll_around_coordinate(x, y_coordinate), (x.shape[0]*x.shape[1])))
    size = int(len(data_X) * (1-train_test_split))
    train_X = np.squeeze(data_X[0:size])
    train_Y = np.squeeze(data_Y[0:size])
    test_X = np.squeeze(data_X[size:len(data_X)])
    test_Y = np.squeeze(data_Y[size:len(data_Y)])
    return (train_X, train_Y, test_X, test_Y)

def process_data_reduced(data, y_coordinate, most_relevant_coordinates, train_test_split = 0.2, shuffle = True):
    '''
    Preprocess the list of traffic matrices, by extracting the value in the coordinate to predict, and centering the matrices around it. 

    Parameters
    ----------
    data : NDArray
        numpy array of traffic matrices.
    y_coordinate : tuple
        coordinate of the value to predict.
    most_relevant_coordinates: list
        list of coordinates (tuples) to include in the reduced matrices.
    train_test_split : float
        portion of data dedicated to testing purposes.  
    shuffle : bool
        whether to shuffle the data or not.

    Returns
    -------
    tuple
        a 4-tuple of numpy arrays in the form of (train_X, train_Y, test_X, test_Y).
    '''
    data_X = []
    data_Y = []
    for position in most_relevant_coordinates:
        if position[0] >= data.shape[1] or position[1] >= data.shape[2]:
            raise ValueError(f'Specified position {y_coordinate} is out of bounds (matrix_shape = {data.shape}).')
    if shuffle == True:
        matrices = np.random.permutation(data)
    else:
        matrices = data
    for matrix in matrices:
        y, x = get_matrix_subset(matrix, y_coordinate, most_relevant_coordinates)
        data_Y.append(y)
        data_X.append(x)
    size = int(len(data_X) * (1-train_test_split))
    data_X = np.array(data_X)
    data_Y = np.array(data_Y)
    train_X = data_X[0:size]
    train_Y = data_Y[0:size]
    test_X = data_X[size:len(data_X)]
    test_Y = data_Y[size:len(data_Y)]
    return (train_X, train_Y, test_X, test_Y)