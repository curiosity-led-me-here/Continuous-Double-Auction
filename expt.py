import numpy as np
alpha = 1
dt = 1
ticks = [1,2,3,4,5]

for i in range(100):
    k = np.random.geometric(0.5) - 1
    print(k)
