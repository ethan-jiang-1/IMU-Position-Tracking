import pandas as pd
import numpy as np
from tqdm import tqdm

def receive_imu(filename="ds_NCLT/2012-01-08_00/imu.csv"):

    data = []

    #data_order={'w': 1, 'a': 2, 'm': 3}
    pd_imu = pd.read_csv(filename)
    print(pd_imu)
    len_pd = len(pd_imu)
    for i in tqdm(range(len_pd)):
        row = pd_imu.iloc[i]
        dl = [row.wx, row.wy, row.wz, row.ax*9.8, row.ay*9.8, row.az*9.8]
        #dl = [row.wx, row.wy, row.wz, row.ax, row.ay, row.az]
        data.append(dl)
    return np.array(data)

def receive_gt(filename="ds_NCLT/2012-01-08_00/gt.csv"):
    data = []

    #data_order={'w': 1, 'a': 2, 'm': 3}
    pd_gt = pd.read_csv(filename)
    print(pd_gt)
    len_pd = len(pd_gt)
    for i in tqdm(range(len_pd)):
        row = pd_gt.iloc[i]
        dl = [row.px, row.py, row.pz]
        data.append(dl)
    return np.array(data)

