import pandas as pd
import numpy as np
from tqdm import tqdm

def receive_imu(filename, g_based=False):
    data = []

    pd_imu = pd.read_csv(filename)
    print("imu data", filename)
    print(pd_imu)
    print(pd_imu.describe())
    print()
    len_pd = len(pd_imu)
    for i in tqdm(range(len_pd), desc="imu"):
        row = pd_imu.iloc[i]
        if g_based:
            dl = [row.wx, row.wy, row.wz, row.ax*9.8, row.ay*9.8, row.az*9.8]
        else:
            dl = [row.wx, row.wy, row.wz, row.ax, row.ay, row.az]
        data.append(dl)
    return np.array(data)

def receive_gt(filename):
    data = []

    print("gt data", filename)
    pd_gt = pd.read_csv(filename)
    print(pd_gt)
    print(pd_gt.describe())
    print()
    len_pd = len(pd_gt)
    for i in tqdm(range(len_pd), desc="gt"):
        row = pd_gt.iloc[i]
        dl = [row.px, row.py, row.pz]
        data.append(dl)
    return np.array(data)

