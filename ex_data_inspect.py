import pandas as pd
#import numpy as np

names_raw = """Time 
attitude_roll(radians) attitude_pitch(radians) attitude_yaw(radians) 
rotation_rate_x(radians/s) rotation_rate_y(radians/s) rotation_rate_z(radians/s) 
gravity_x(G) gravity_y(G) gravity_z(G) 
user_acc_x(G) user_acc_y(G) user_acc_z(G)
magnetic_field_x(microteslas) magnetic_field_y(microteslas) magnetic_field_z(microteslas)
"""
#names_raw = names_raw.replace("\n", "")
#print(names_raw)

names_imu = "ts roll pitch yaw wx wy wz gv_x gv_y gv_z acc_x acc_y acc_z mag_x mag_y mag_z".split(" ")

pd_imu = pd.read_csv("Data/syn/imu1.csv", names=names_imu)
print(pd_imu)

names_vi = "ts hd px py pz rx ry rz".split(" ")
pd_vi = pd.read_csv("Data/syn/vi1.csv", names=names_vi)
print(pd_vi)


pd_imu1 = pd.read_csv("ds_Oxiod_running/running_data1_syn_imu1/imu.csv")
pd_gt1 = pd.read_csv("ds_Oxiod_running/running_data1_syn_imu1/gt.csv")

print(pd_imu1)
print(pd_gt1)


pd_imu2 = pd.read_csv("2012-01-08_00/imu.csv")
pd_gt2 = pd.read_csv("2012-01-08_00/gt.csv")

print(pd_imu2)
print(pd_gt2)
