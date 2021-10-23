import pandas as pd
import numpy as np 
from ex_imutracker_fuse6 import track_by_fuse6
from ex_datasrc import receive_imu, receive_gt
from ex_plot import plot3D_two


def _get_data(dirname="ds_Kiast/sensor_data_urban07_00"):
    print("using data under", dirname)
    data_imu = receive_imu(dirname + "/imu.csv")    # toggle data source between 'tcp' and 'file' here
    data_gt = receive_gt(dirname + "/gt.csv")
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


def do_exec_main():
    data_imu, data_gt = _get_data()

    for mode in range(6):
        data_et = track_by_fuse6(data_imu, mode=mode)
        if data_et is None:
            continue

        pd_p_et = pd.DataFrame(np.array(data_et), columns=["x", "y", "z"])
        print(pd_p_et)
        pd_p_gt = pd.DataFrame(np.array(data_gt), columns=["x", "y", "z"])
        print(pd_p_gt)

        plot_data_et = [[data_et, 'position']]
        plot_data_gt = [[data_gt, 'posotion']]
        #plot3D_one(plot_data)
        plt = plot3D_two(plot_data_et, plot_data_gt, return_plt=True, mode=mode)
        plt.show()


if __name__ == '__main__':
    do_exec_main()
