import pandas as pd
import numpy as np 

from ex_datasrc import receive_imu, receive_gt
from ex_plot import plot3D_two
from ex_distance import cal_distance


def _get_data(dirname):
    print("using data under", dirname)
    data_imu = receive_imu(dirname + "/imu.csv")    # toggle data source between 'tcp' and 'file' here
    data_gt = receive_gt(dirname + "/gt.csv")
    return data_imu, data_gt

def _get_tracker_functions():
    track_funs = {}
    from ex_imutracker_IPT import track_by_IPT
    track_funs["IPT:IMU-Position-Tracking"] = track_by_IPT

    from ex_imutracker_gy89 import track_by_gy89
    track_funs["gy89:imu_gy89"] = track_by_gy89

    return track_funs

def show_pd_dis(data_pos, name=None):
    if name is not None:
        print("name", name)
    pd_p_et = pd.DataFrame(np.array(data_pos), columns=["x", "y", "z"])
    print(pd_p_et)
    dis_total_et, dis_3_et, distances_et = cal_distance(data_pos)
    print("100", dis_total_et)
    print("100", dis_3_et)
    dis_total_et, dis_3_et, distances_et = cal_distance(data_pos, cal_steps=50)
    print(" 50", dis_total_et)
    print(" 50", dis_3_et)
    print()

def show_result_by_mode(data_et, data_gt, mode):
    show_pd_dis(data_gt, "groundturth")
    show_pd_dis(data_et, "estimation_{}".format(mode))

    plot_data_et = [[data_et, 'position']]
    plot_data_gt = [[data_gt, 'position']]
    #plot3D_one(plot_data)
    plt = plot3D_two(plot_data_et, plot_data_gt, return_plt=True, mode=mode)
    plt.show()

def do_exec_main_same_tracker(dirname, tracker_func=None):
    data_imu, data_gt = _get_data(dirname)

    if tracker_func is None:
        from ex_imutracker_IPT import track_by_IPT
        tracker_func = track_by_IPT

    for mode in range(1):
        data_et = tracker_func(data_imu, mode=mode)
        if data_et is None:
            continue

        show_result_by_mode(data_et, data_gt, mode)

def do_exec_main_all_trackers(dirname):
    data_imu, data_gt = _get_data(dirname)

    tracker_funcs = _get_tracker_functions()

    data_ets = {}
    for key, tracker_func in tracker_funcs.items():
        print()
        print("------------")
        print("###Using tracker", key)
        data_et = tracker_func(data_imu)
        if data_et is None:
            continue
        data_ets[key] = data_et

    show_pd_dis(data_gt, "groundturth")
    for key, data_et in data_ets.items():
        show_pd_dis(data_et, "estimation_{}".format(key))


if __name__ == '__main__':
    #dirname ="ds_Kiast/sensor_data_urban07_00"
    #dirname ="ds_Oxiod_running/running_data1_syn_imu1"
    #dirname = "ds_Ridi/dan_body1"

    #dirname = "ds_Ridi/dan_body1"          # 1/2
    #dirname = "ds_Ridi/dan_body2"          # 1/2
    #dirname = "ds_Ridi/hang_bag_speed1"    # 1/2
    #dirname = "ds_Ridi/hang_bag_speed2"    # 1/2
    #dirname = "ds_Ridi/hang_body_fast1"    # 1/2
    #dirname = "ds_Ridi/hang_body_normal1"  # 2/3 97/153
    #dirname = "ds_Ridi/zhicheng_body1"     # 4/5 124/144
    #dirname = "ds_Ridi/zhicheng_body2"     # 4/5 53/66
    #dirname = "ds_Ridi/hao_body1"          # 39/65
    dirname = "ds_Ridi/hao_body2"           # 61/64

    do_exec_main_same_tracker(dirname)
    #do_exec_main_all_trackers(dirname)
