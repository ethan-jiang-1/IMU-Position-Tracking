import numpy as np
import math

# import numpy as np
import matplotlib.pyplot as plt

class TrajOdometer(object):

    @classmethod
    def get_rmse(cls, traj_gt, traj_pr):
        #shape of traj is (n, 3): n points x, y, z        
        com_len = min(traj_gt.shape[0], traj_pr.shape[0])
        traj_gt = traj_gt[0:com_len:,:]
        traj_pr = traj_pr[0:com_len:,:]

        return np.sqrt(np.mean(np.square(np.linalg.norm(traj_gt - traj_pr, axis=-1))))

    @classmethod
    def get_distance_3D(cls, traj_x):
        distance_all = 0
        for i in range(1, len(traj_x)):
            p0 = traj_x[i-1]
            p1 = traj_x[i]
            d = math.sqrt((p1[0] - p0[0]) ** 2 + \
                          (p1[1] - p0[1]) ** 2 + \
                          (p1[2] - p0[2]) ** 2 )
            distance_all += d
        return distance_all

    @classmethod
    def get_distance_2D(cls, traj_x):
        distance_all = 0
        for i in range(1, len(traj_x)):
            p0 = traj_x[i-1]
            p1 = traj_x[i]
            d = math.sqrt((p1[0] - p0[0]) ** 2 + \
                          (p1[1] - p0[1]) ** 2 )
            distance_all += d
        return distance_all


class TrajPlotter(object):
    @classmethod
    def plot3D(cls, traj_gt, traj_pr, figsize=(10, 10)):
         #shape of traj is (n, 3): n points x, y, z

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')

        if traj_gt is not None:
            gt_3d = TrajOdometer.get_distance_3D(traj_gt)
            ax.plot(traj_gt[:, 0], traj_gt[:, 1], traj_gt[:, 2], '.', label="gt 3d {:.4f}".format(gt_3d))

        if traj_pr is not None:
            pr_3d = TrajOdometer.get_distance_3D(traj_pr)
            ax.plot(traj_pr[:, 0], traj_pr[:, 1], traj_pr[:, 2], ':', label="pr 3d {:.4f}".format(pr_3d))

        ax.legend()
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        #ax.plot([0], [0], [0], 'ro')
        plt.show()

    @classmethod
    def plot2D(cls, traj_gt, traj_pr, figsize=(10, 10)):
         #shape of traj is (n, 3): n points x, y, z

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')

        if traj_gt is not None:
            gt_2d = TrajOdometer.get_distance_2D(traj_gt)
            ax.plot(traj_gt[:, 0], traj_gt[:, 1], [0 for i in range(len(traj_gt))], '.', label="gt 2d {:.4f}".format(gt_2d))

        if traj_pr is not None:
            pr_2d = TrajOdometer.get_distance_2D(traj_pr)
            ax.plot(traj_pr[:, 0], traj_pr[:, 1], [1 for i in range(len(traj_pr))], ':', label="pr 2d {:.4f}".format(pr_2d))

        ax.legend()
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        #ax.plot([0], [0], [0], 'ro')
        plt.show()
