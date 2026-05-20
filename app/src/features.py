import pandas
from .config import ALL_FEATURES

def engineer_features(inputs):
    return pandas.DataFrame([dict(inputs)])[ALL_FEATURES]