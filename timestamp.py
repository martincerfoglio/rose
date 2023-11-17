import pandas as pd
import time 

def timestamp():
    return str(pd.to_datetime(time.time_ns(), unit='ns'))
