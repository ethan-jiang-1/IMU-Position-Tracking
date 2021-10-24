import numpy as np
from tqdm import tqdm

class IMUTracker_Double(object):
    def __init__(self, sampling=100):
        self.sampling = sampling
        self.dt = 1 / sampling    # second

    def initialize(self, data):

        sample_number = np.shape(data)[0]

        t = 0
        print("\nfuse8")
        pbar = tqdm(total=int(sample_number/100), desc="double")
        while t < sample_number:
            if t > 0:
                pbar.update(int(t/100))

            t += 1


s_ncs = {0: {'w': 100, 'a': 100}}

def track_by_double(data_imu, mode=None):
    noise_coefficient = None
    if mode is not None:
        if mode in s_ncs:
            noise_coefficient = s_ncs[mode]
        else:
            print("not valid mode", mode)
            return None
    tracker = IMUTracker_Double(sampling=100)

    print('initializing...')
    init_list = tracker.initialize(data_imu[5:30],  noise_coefficient=noise_coefficient)

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
