import pandas as pd
import numpy as np 
from ex_imutracker_fuse6 import IMUTracker_Fuse6
from ex_datasrc import receive_imu, receive_gt
from ex_plot import plot3D_two


def _get_data():
    data_imu = receive_imu()    # toggle data source between 'tcp' and 'file' here
    data_gt = receive_gt()
    return data_imu, data_gt

def _plot_ani(p):
    # make 3D animation
    # xl = np.min(p[:, 0]) - 0.05
    # xh = np.max(p[:, 0]) + 0.05
    # yl = np.min(p[:, 1]) - 0.05
    # yh = np.max(p[:, 1]) + 0.05
    # zl = np.min(p[:, 2]) - 0.05
    # zh = np.max(p[:, 2]) + 0.05
    # plot3DAnimated(p, lim=[[xl, xh], [yl, yh], [zl, zh]], label='position', interval=5)
    pass

def _track_by_fuse6(data_imu):

    tracker = IMUTracker_Fuse6(sampling=100)

    print('initializing...')
    init_list = tracker.initialize(data_imu[5:30])

    print('--------')
    print('processing...')
    
    # EKF step
    a_nav, orix, oriy, oriz = tracker.attitudeTrack(data_imu[30:], init_list)

    # Acceleration correction step
    a_nav_filtered = tracker.removeAccErr(a_nav, filter=False)
    # plot3([a_nav, a_nav_filtered])

    # ZUPT step
    v = tracker.zupt(a_nav_filtered, threshold=0.2)
    # plot3([v])

    # Integration Step
    p = tracker.positionTrack(a_nav_filtered, v)
    return p


def do_exec_main():
    data_imu, data_gt = _get_data()

    data_et = _track_by_fuse6(data_imu)

    pd_p_et = pd.DataFrame(np.array(data_et), columns=["x", "y", "z"])
    print(pd_p_et)
    pd_p_gt = pd.DataFrame(np.array(data_gt), columns=["x", "y", "z"])
    print(pd_p_gt)

    plot_data_et = [[data_et, 'position']]
    plot_data_gt = [[data_gt, 'posotion']]
    #plot3D_one(plot_data)
    plot3D_two(plot_data_et, plot_data_gt)


if __name__ == '__main__':
    do_exec_main()
