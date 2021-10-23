from plotlib import *

def plot3D_one(data, lim=None, ax=None):
    '''
    @param data: [[data, label_string], ...]
    @param lim: [[xl, xh], [yl, yh], [zl, zh]]
    '''

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    for item in data:
        label = item[1]
        d = item[0]
        ax.plot(d[:, 0], d[:, 1], d[:, 2], 'o', label=label)

    if lim is not None:
        if lim[0] is not None:
            ax.set_xlim(lim[0][0], lim[0][1])
        if lim[1] is not None:
            ax.set_ylim(lim[1][0], lim[1][1])
        if lim[2] is not None:
            ax.set_zlim(lim[2][0], lim[2][1])

    ax.legend()
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.plot([0], [0], [0], 'ro')
    plt.show()

def plot3D_two(data1, data2):
    '''
    @param data: [[data, label_string], ...]
    @param lim: [[xl, xh], [yl, yh], [zl, zh]]
    '''
    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')
    
    for item in data1:
        label = item[1]
        d = item[0]
        ax1.plot(d[:, 0], d[:, 1], d[:, 2], 'o', label=label)

    ax1.legend()
    ax1.set_xlabel('X axis')
    ax1.set_ylabel('Y axis')
    ax1.set_zlabel('Z axis')
    ax1.plot([0], [0], [0], 'ro')

    for item in data2:
        label = item[1]
        d = item[0]
        ax2.plot(d[:, 0], d[:, 1], d[:, 2], 'o', label=label)

    ax2.legend()
    ax2.set_xlabel('X axis')
    ax2.set_ylabel('Y axis')
    ax2.set_zlabel('Z axis')
    ax2.plot([0], [0], [0], 'ro')

    plt.show()
