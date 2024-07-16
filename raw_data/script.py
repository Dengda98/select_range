import numpy as np

# with open('sta879_ajp', 'r') as f1, open('stations', 'w') as f2:
#     for line in f1.readlines():
#         f2.write(line[21:])

dataev = np.loadtxt('events_all', usecols=[7,9])
np.savetxt("events", dataev, fmt='%12.4f')