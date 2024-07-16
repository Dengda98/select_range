'''
    Zhu Dengda 
    2024.03
'''

import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib as mpl

from matplotlib.widgets import Cursor, Button
from scipy.interpolate import interpn, griddata


from matplotlib.backend_bases import MouseButton

datasta = np.loadtxt('stations')
dataev = np.loadtxt('events')

fig, ax = plt.subplots(1, 1, figsize=(7, 10))
# ax.pcolorfast(slabsrf1_lon, slabsrf1_lat, deps_topo_interp)
ax.scatter(datasta[:,1], datasta[:,0], s=20, color='k', marker='^')
ax.scatter(dataev[:,1], dataev[:,0], s=10, color='green', marker='o', linewidths=0.2, edgecolors='k')


# 绘制海岸线 
with open('coast', 'r') as f:
    segslon = []
    segslat = []
    for line in f.readlines():
        if line[0]=='>':
            if len(segslon) > 0:
                ax.plot(segslon, segslat, c='r', lw=2)
            segslon = []
            segslat = []
            continue 
        else:
            lon, lat = map(lambda x:float(x), line.strip().split())
            segslon.append(lon)
            segslat.append(lat)

    ax.plot(segslon, segslat, c='r', lw=2)

# plot trench
with open('trench', 'r') as f:
    segslon = []
    segslat = []
    for line in f.readlines():
        if line[0]=='>':
            if len(segslon) > 0:
                ax.plot(segslon, segslat, c='k', lw=2)
            segslon = []
            segslat = []
            continue 
        else:
            lon, lat = map(lambda x:float(x), line.strip().split())
            segslon.append(lon)
            segslat.append(lat)

    ax.plot(segslon, segslat, c='r', lw=2)


ax.set_xlim((138, 146))
ax.set_ylim((36, 45))

lines_x = []
lines_y = []

def on_move(event):
    if event.inaxes:
        print(f'data coords {event.xdata} {event.ydata},',
              f'pixel coords {event.x} {event.y}')
        
cursor = Cursor(ax, useblit=True, color='red', linewidth=1)


OUTFILE = open('click_out', 'w')
def on_click(event):
    if event.button is MouseButton.LEFT:
        # print('disconnecting callback')
        # plt.disconnect(binding_id)

        print(f'{event.xdata:10.5f} {event.ydata:10.5f}')
        print(f'{event.xdata:10.5f} {event.ydata:10.5f}', file=OUTFILE)
        lines_x.append(event.xdata)
        lines_y.append(event.ydata)

        if len(lines_x)>=2:
            ax.plot(lines_x, lines_y, 'ro-')
            fig.canvas.draw()


# binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', on_click)
plt.show()
OUTFILE.close()