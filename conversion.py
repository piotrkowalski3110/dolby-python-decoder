import numpy as np

def convertToFloat(data):
    if data.dtype == np.int16:
        return data.astype(np.float64) / 32768.0
    elif data.dtype == np.int32:
        return data.astype(np.float64) / 2147483648.0
    elif data.dtype == np.uint8:
        return (data.astype(np.float64) - 128.0) / 128.0
    elif data.dtype == np.int8:
        return data.astype(np.float64) / 128.0
    elif data.dtype in [np.float32, np.float64]:
        converted = data.astype(np.float64)
        return np.clip(converted, -1.0, 1.0)
    else:
        return data.astype(np.float64)