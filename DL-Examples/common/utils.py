from sklearn.datasets import fetch_mldata
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import numpy as np

def mnist_for_library(channel_first=True, one_hot=False): 
    # Raw data
    mnist = fetch_mldata('MNIST original')
    y = mnist.target
    # Reshape to N, W, H and scale by pixel intensity
    X = mnist.data.reshape(-1, 28, 28)
    X = X / 256.0
    # Channels first or last
    if channel_first:
        X = np.expand_dims(X, axis=1)
    else:
        X = np.expand_dims(X, axis=-1)
        
    # One-hot encode y
    if one_hot:
        enc = OneHotEncoder(categorical_features='all')
        y = enc.fit_transform(np.expand_dims(y, axis=-1)).toarray()
        
    return train_test_split(X.astype(np.float32), y.astype(np.int8), train_size=6/7, random_state=123)