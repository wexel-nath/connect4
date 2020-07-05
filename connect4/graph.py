import matplotlib.pyplot as plt

from util import get_full_file_path

graph_data = open(get_full_file_path("win_rates.csv"), "r").read()
lines = graph_data.split('\n')
xs = []
ys = []
for line in lines:
    if len(line) > 1:
        x, y = line.split(",")
        xs.append(int(x))
        ys.append(float(y))

plt.cla()
plt.plot(xs, ys, lw=0.4)
plt.xlabel("Number of games")
plt.ylabel("Win rate (%)")

plt.tight_layout()
plt.show()
