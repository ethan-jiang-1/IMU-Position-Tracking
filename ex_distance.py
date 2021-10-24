import numpy as np
import math

def cal_distance(data_pos, cal_steps=100, inc_ratio=1.0):
    len_pos = len(data_pos)
    i = 0
    dis_total = 0
    dis_x = 0
    dis_y = 0
    dis_z = 0
    distances = []
    while i < len_pos:
        pos_s = i 
        pos_e = i + cal_steps
        if pos_e >= len_pos:
            pos_e = len_pos - 1

        ps = data_pos[pos_s]
        pe = data_pos[pos_e]

        x = abs(pe[0] - ps[0])
        y = abs(pe[1] - ps[1])
        z = abs(pe[2] - ps[2])

        dis = math.sqrt(x ** 2 + y ** 2 + z ** 2) * inc_ratio
        distances.append(dis)

        dis_total += dis
        dis_x += x 
        dis_y += y
        dis_z += z

        if pos_e == len_pos - 1:
            break
        i += cal_steps
    return dis_total, (dis_x, dis_y, dis_z), np.array(distances)



