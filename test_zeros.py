
import numpy as np

lst = [3, 3, 3]

zeros = list(zip(*np.where(np.array(lst) == 0)))
y, x = rd.choice(zeros)
new_value = rd.choices((0, 2, 2 * 2), [.1, .8, .1])[0]
