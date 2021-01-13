import numpy as np

#from numpy.linalg import inv, norm

#from mathlib import *
from plotlib import plot3D, plot3, plot3DAnimated


from imu_tracker import IMUTracker

'''
data sample rate need to be spectied seprated, default is 100 (Hz)
line in raw data (w: gyro) (a: acce) (m: magn)

idx = {1: [0, 3], 2: [3, 6], 3: [6, 9]}
self._widx = idx[data_order['w']]
self._aidx = idx[data_order['a']]
self._midx = idx[data_order['m']]
'''

def _recv_data_tcp(mode, pathname):
    import data_receiver
    data = []
    r = data_receiver.Receiver()
    file = open(pathname, 'w')
    print('listening...')
    for line in r.receive():
        file.write(line)
        data.append(line.split(','))
    data = np.array(data, dtype=np.float)
    return data

def _recv_data_txt(mode, pathname):
    data = []
    file = open(pathname, 'r')
    for line in file.readlines():
        data.append(line.split(','))
    data = np.array(data, dtype=np.float)
    return data

def _recv_data_csv(mode, pathname):
    import pandas as pd
    data = []
    df_data = pd.read_csv(pathname)
    print("\n" + pathname)
    print(df_data)
    print(df_data.describe())
    data = df_data[["w_x","w_y","w_z","a_x","a_y","a_z","m_x","m_y","m_z"]].to_numpy()
    return data

def receive_data(mode='txt_file', pathname='data.txt'):
    if mode == 'tcp':
        return _recv_data_tcp(mode, pathname)
    elif mode == 'txt_file':
        return _recv_data_txt(mode, pathname)
    elif mode == "csv_file":
        return _recv_data_csv(mode, pathname)
    else:
        raise Exception('Invalid mode argument: ', mode)

def ex_cvs_cmp_traj(pathname, p):
    import pandas as pd
    from ex_traj import TrajPlotter
    traj_pr = p
    df_data = pd.read_csv(pathname)
    traj_gt = df_data[["pos_x", "pos_y", "pos_z"]].to_numpy()

    df_pr = pd.DataFrame(traj_pr, columns=["x", "y", "z"])
    df_gt = pd.DataFrame(traj_gt, columns=["x", "y", "z"])
    print("\n pred")
    print(df_pr)
    print(df_pr.describe())
    print("\n gt")
    print(df_gt)
    print(df_gt.describe())

    TrajPlotter.plot3D(traj_gt, traj_pr)    

def plot_trajectory(mode="file", pathname="data.txt", sampling_rate=100):
    tracker = IMUTracker(sampling=sampling_rate)
    data = receive_data(mode=mode, pathname=pathname)    # toggle data source between 'tcp' and 'file' here

    print('initializing...')
    init_list = tracker.initialize(data[5:30])

    print('--------')
    print('processing...')
    
    # EKF step
    a_nav, orix, oriy, oriz = tracker.attitudeTrack(data[30:], init_list)

    # Acceleration correction step
    a_nav_filtered = tracker.removeAccErr(a_nav, filter=False)
    plot3([a_nav, a_nav_filtered])

    # ZUPT step
    v = tracker.zupt(a_nav_filtered, threshold=0.2)
    plot3([v])

    # Integration Step
    p = tracker.positionTrack(a_nav_filtered, v)
    if mode != "csv_file":
        plot3D([[p, 'position']])
    else:
        ex_cvs_cmp_traj(pathname, p)


    
    # # make 3D animation
    # xl = np.min(p[:, 0]) - 0.05
    # xh = np.max(p[:, 0]) + 0.05
    # yl = np.min(p[:, 1]) - 0.05
    # yh = np.max(p[:, 1]) + 0.05
    # zl = np.min(p[:, 2]) - 0.05
    # zh = np.max(p[:, 2]) + 0.05
    # plot3DAnimated(p, lim=[[xl, xh], [yl, yh], [zl, zh]], label='position', interval=50)


if __name__ == '__main__':
    mode = "csv_file"
    pathname = "ds_csv/synced_data_02.csv"
    plot_trajectory(mode=mode, pathname=pathname)
