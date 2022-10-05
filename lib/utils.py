import re
import os
from datetime import datetime
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def path_to_datetime(path):
    """Returns the datetime object associated with an event path.

        Args:
            path (str): The path on the filesystem matching a fault event directory.  Ending in .../<date>/<time> where
                        <date> is of the format YYYY_MM_DD and <time> is formatted hhmmss.S

        Returns:
            datetime: A datetime object corresponding to the event timestamp embedded in the supplied path

        Raises:
            ValueError: if the path is not of the expected format
    """

    time_pattern = re.compile(r'\d\d\d\d\d\d\.\d')
    date_pattern = re.compile(r'\d\d\d\d_\d\d_\d\d')
    path = os.path.abspath(path).split(os.path.sep)

    time = str(path[-1])
    date = str(path[-2])
    if not time_pattern.match(time):
        raise ValueError("Path includes invalid time format - " + time)

    if not date_pattern.match(date):
        raise ValueError("Path includes invalid date format - " + date)

    return datetime(year=int(date[0:4]), month=int(date[5:7]), day=int(date[8:10]), hour=int(time[0:2]),
                    minute=int(time[2:4]), second=int(time[4:6]), microsecond=int(time[7:8]) * 100000)


def path_to_zone_and_timestamp(path, fmt="%Y-%m-%d %H:%M:%S.%f"):
    """Returns a tuple containing the event zone and timestamp.

        Args:
            path (str): The path on the filesystem matching a fault event directory.  Ending in .../<date>/<time> where
                        <date> is of the format YYYY_MM_DD and <time> is formatted hhmmss.S
            fmt (str): The format string used by datetime.strftime.
        Returns:
            tuple: A tuple object containing strings for the event zone and timestamp

        Raises:
            ValueError: if the path is not of the expected format
    """

    time_pattern = re.compile(r'\d\d\d\d\d\d\.\d')
    date_pattern = re.compile(r'\d\d\d\d_\d\d_\d\d')
    path = os.path.abspath(path).split(os.path.sep)

    time = str(path[-1])
    date = str(path[-2])
    zone = str(path[-3])
    if not time_pattern.match(time):
        raise ValueError("Path includes invalid time format - " + time)

    if not date_pattern.match(date):
        raise ValueError("Path includes invalid date format - " + date)

    dt = datetime(year=int(date[0:4]), month=int(date[5:7]), day=int(date[8:10]), hour=int(time[0:2]),
                  minute=int(time[2:4]), second=int(time[4:6]), microsecond=int(time[7:8]) * 100000)

    return zone, dt.strftime(fmt)[:-5]


def softmax(x: np.array) -> Tuple[int, List[float]]:
    dist = np.exp(x) / np.sum(np.exp(x))
    y = np.argmax(dist)
    return int(y), dist


def standard_scaling(df: pd.DataFrame, fill: float = 0.0) -> pd.DataFrame:
    """This is like sklearn's StandardScaler, except that constant signals are replaced with an arbitrary constant.

    This transforms the DataFrame in place.
    """
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
    df = df.copy()
    for i in range(len(df.columns)):
        signal = df.iloc[:, i].values.reshape(-1, 1)
        if np.min(signal) == np.max(signal):
            df.iloc[:, i] = [fill] * len(signal)
        else:
            df.iloc[:, i] = scaler.fit_transform(signal)
    return df