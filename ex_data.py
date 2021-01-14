import pandas as pd
import numpy as np

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
    data = []
    df_data = pd.read_csv(pathname)
    print("\n" + pathname)
    print(df_data)
    print(df_data.describe())
    data = df_data[["w_x","w_y","w_z","a_x","a_y","a_z","m_x","m_y","m_z"]].to_numpy()
    return data

def _recv_gt_csv(mode, pathname):
    import pandas as pd
    df_data = pd.read_csv(pathname)
    data_gt = df_data[["pos_x", "pos_y", "pos_z"]].to_numpy()
    return data_gt

'''
def load_oxiod_dataset(imu_data_filename, gt_data_filename):
    imu_data = pd.read_csv(imu_data_filename).values
    gt_data = pd.read_csv(gt_data_filename).values

    imu_data = imu_data[1200:-300]
    gt_data = gt_data[1200:-300]

    gyro_data = imu_data[:, 4:7]
    acc_data = imu_data[:, 10:13]
    
    pos_data = gt_data[:, 2:5]
    ori_data = np.concatenate([gt_data[:, 8:9], gt_data[:, 5:8]], axis=1)

    return gyro_data, acc_data, pos_data, ori_data

imu data
 0 Time 
 1 attitude_roll(radians) attitude_pitch(radians) attitude_yaw(radians) 
 4 rotation_rate_x(radians/s) rotation_rate_y(radians/s) rotation_rate_z(radians/s) 
 7 gravity_x(G) gravity_y(G) gravity_z(G) 
10 user_acc_x(G) user_acc_y(G) user_acc_z(G) 
13 magnetic_field_x(microteslas) magnetic_field_y(microteslas) magnetic_field_z(microteslas)

'''

def _recv_data_oxiod(mode, pathname):
    # "handheld/data1:2"
    names = pathname.split(":")
    imu_path = "ds_oxiod/{}/syn/imu{}.csv".format(names[0], names[1])
    df_imu = pd.read_csv(imu_path)
    imu_data = df_imu.values

    gyro_data = imu_data[:, 4:7]
    acc_data = imu_data[:, 10:13]
    mag_data = imu_data[:, 13:16]

    data = np.concatenate([gyro_data, acc_data, mag_data], axis=1)
    return data

'''
 0 Time  
 1 Header  
 2 translation.x translation.y translation.z 
 5 rotation.x rotation.y rotation.z rotation.w

'''
def _recv_gt_oxiod(mode, pathname):
    # "handheld/data1:2"
    names = pathname.split(":")
    vi_path = "ds_oxiod/{}/syn/vi{}.csv".format(names[0], names[1])
    df_vi = pd.read_csv(vi_path)
    vi_data = df_vi.values
    data = vi_data[:, 2:5]
    return data


class DataLoader(object):
    @classmethod
    def receive_data(cls, mode='txt_file', pathname='data.txt'):
        if mode == 'tcp':
            return _recv_data_tcp(mode, pathname)
        elif mode == 'txt_file':
            return _recv_data_txt(mode, pathname)
        elif mode == "csv_file":
            return _recv_data_csv(mode, pathname)
        elif mode == "oxiod":
            return _recv_data_oxiod(mode, pathname)
        raise ValueError('no data')

    @classmethod
    def receive_gt(cls, mode='txt_file', pathname='data.txt'):
        if mode == "csv_file":
            return _recv_gt_csv(mode, pathname)
        elif mode == "oxiod":
            return _recv_gt_oxiod(mode, pathname)
        raise ValueError("no_gt")


if __name__ == '__main__':
    data = DataLoader.receive_data(mode="oxiod", pathname="handheld/data1:2")
    gt = DataLoader.receive_gt(mode="oxiod", pathname="handheld/data1:2")
