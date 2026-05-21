# features.py
import pandas
from .config import ALL_FEATURES

def engineer_features(inputs):
    df = pandas.DataFrame([dict(inputs)])
    return df[ALL_FEATURES]