import lime.lime_tabular as lt
import tensorflow as tf
import numpy as np

class CNN:
    """
    CNN based Traffic Matrix Completion model for single coordinate estimation.

    Attributes
    ----------
    input_shape : tuple
        The shape of the input matrices extended by a 1-valued position (e.g (10, 10, 1) for 10 x 10 matrices).
    target_coordinate : tuple
        The coordinate of the missing value to predict (e.g. coordinate (7,9)) .

    Methods
    -------
    train(matrix_data, model_path)
        Train the model using matrix data and save it in the specified path.

    predict(sample)
        Make a prediction on a batch of traffic matrices.
    """
    
    def __init__(self, input_shape, target_coordinate) -> None:
        """
        Initialize the Traffic Matrix Completion model.
        
        Parameters
        ----------
        input_shape : tuple
            The shape of the input matrices extended by a 1-valued position (e.g (N, M, 1) for N x M matrices).
        target_coordinate : tuple
            The coordinate of the missing value to predict (e.g. coordinate (i,j)) .
        """
        self.input_shape = input_shape
        self.target_coordinate = target_coordinate
        inter_act = 'relu'
        dense = 100
        self.model = tf.keras.models.Sequential([
            tf.keras.Input(shape=(input_shape[0]*input_shape[1],)),
            tf.keras.layers.Reshape(input_shape),
            tf.keras.layers.Conv2D(32, (2,2), kernel_initializer='random_uniform', bias_initializer='zeros', bias_regularizer=tf.keras.regularizers.l2(), kernel_regularizer=tf.keras.regularizers.l2(), padding='same', input_shape=(12,12,1)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Activation(inter_act),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Conv2D(64, (2,2), kernel_initializer='random_uniform', bias_initializer='zeros', bias_regularizer=tf.keras.regularizers.l2(), kernel_regularizer=tf.keras.regularizers.l2(), padding='same'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Activation(inter_act),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(dense, activation=inter_act, kernel_initializer='random_uniform', bias_initializer='zeros', bias_regularizer=tf.keras.regularizers.l2(), kernel_regularizer=tf.keras.regularizers.l2()), 
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(1, activation='linear')
        ])
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=5e-5), loss='mse', metrics=['mae', 'mape'])
        self.model.summary()

    def train(self, train_X, train_Y, test_X, test_Y, model_path):
        """
        Train the model using matrix data and save it in the specified path.
        
        Parameters
        ----------
        train_X : NDArray
            A numpy array of training traffic matrices.
        train_Y : NDArray
            A numpy array of training floating point truth values.
        test_ : NDArray
            A numpy array of test traffic matrices.
        test_Y : NDArray
            A numpy array of test floating point truth values.
        model_path : str
            Path to save trained model in after training .
        """
        if train_X.shape[1] != self.input_shape[0]*self.input_shape[1] or test_X.shape[1] != self.input_shape[0]*self.input_shape[1]:
            raise ValueError(f'Provided data does not match model input shape')
        cb = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience = 10, mode = 'min', restore_best_weights = True, verbose = 1)
        self.model.fit(train_X, train_Y, epochs=300, batch_size=64, validation_data=(test_X, test_Y), callbacks=[cb])
        self.model.save(model_path)

    def predict(self, data_X):
        """
        Make a prediction on a batch of traffic matrices.
        
        Parameters
        ----------
        data : NDArray
            A numpy array of incomplete traffic matrices.

        Returns
        -------
        list
            list of predictions.
        """
        if len(data_X) == 1:
            data_X = np.expand_dims(data_X, -1)
        return self.model.predict(data_X)
    
    def lime(self, train_X, test_X, dest_dir = None):
        """
        Computes average feature (traffic flow) importance over 500 random samples of the test set with LIME XAI tool.

        Parameters
        ----------
        train : NDArray
            training dataset needed to instantiate LIME tool.
        test : NDArray
            test dataset to sample for feature relevance computation.
        dest_dir: str
            directory to save average relevance matrix in, after computation. If None data will NOT be saved to disk.

        Returns
        -------
        NDArray
            sorted array of most important coordinates, from least to most important. 
        """
        n = self.input_shape[0]
        m = self.input_shape[1]
        feature_names = [str((i, j)) for i in range(n) for j in range(m)]
        num_features = n * m
        explainer = lt.LimeTabularExplainer(training_data=np.array(train_X), verbose=True,  mode='regression', class_names=['flow'], feature_names=feature_names)
        test_X = np.array(test_X)
        indices = np.random.choice(len(test_X), 500, replace=False)
        sample = test_X[indices]
        importance_sums = np.zeros((num_features))
        for i, test_instance in enumerate(sample):
            exp = explainer.explain_instance(test_instance, self.model.predict, num_features=num_features)
            imp = exp.local_exp[1]
            for record in imp:
                importance_sums[record[0]] += abs(record[1])
        importance_averages = importance_sums/i
        matrix_avg_imp = np.reshape(importance_averages, (n,m))
        np.save(dest_dir, matrix_avg_imp)
        i = np.absolute(importance_averages).argsort(axis=None, kind='mergesort')
        j = np.unravel_index(i, matrix_avg_imp.shape) 
        sorted = np.vstack(j).T
        return sorted