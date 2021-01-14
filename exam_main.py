
import numpy as np

#from numpy.linalg import inv, norm

#from mathlib import *
from plotlib import plot3D, plot3, plot3DAnimated


from imu_tracker import IMUTracker
from ex_data import DataLoader


def ex_cvs_cmp_traj(mode, pathname, p):
    import pandas as pd
    from ex_traj import TrajPlotter
    traj_pr = p
    traj_gt = DataLoader.receive_gt(mode, pathname)

    df_pr = pd.DataFrame(traj_pr, columns=["x", "y", "z"])
    df_gt = pd.DataFrame(traj_gt, columns=["x", "y", "z"])
    print("\n pred")
    print(df_pr)
    print(df_pr.describe())
    print("\n gt")
    print(df_gt)
    print(df_gt.describe())

    TrajPlotter.plot3D(traj_gt, None)
    TrajPlotter.plot3D(None, traj_pr)

    TrajPlotter.plot3D(traj_gt, traj_pr)   


def plot_trajectory(mode="file", pathname="data.txt", sampling_rate=100):
    data = DataLoader.receive_data(mode=mode, pathname=pathname)    # toggle data source between 'tcp' and 'file' here

    tracker = IMUTracker(sampling=sampling_rate)

    print('initializing...')
    init_list = tracker.initialize(data[5:30])

    print('--------')
    print('processing...')
    
    # EKF step
    a_nav, orix, oriy, oriz = tracker.attitudeTrack(data[30:], init_list)

    # Acceleration correction step
    a_nav_filtered = tracker.removeAccErr(a_nav, filter=False)
    #plot3([a_nav, a_nav_filtered])

    # ZUPT step
    v = tracker.zupt(a_nav_filtered, threshold=0.2)
    #plot3([v])

    # Integration Step
    p = tracker.positionTrack(a_nav_filtered, v)
    if mode not in["csv_file", "oxiod"]:
        plot3D([[p, 'position']])
    else:
        ex_cvs_cmp_traj(mode, pathname, p)



if __name__ == '__main__':
    #mode = "csv_file"
    #pathname = "ds_csv/synced_data_03.csv"
    
    mode = "oxiod"
    pathname = "handheld/data1:2"
    
    plot_trajectory(mode=mode, pathname=pathname)
