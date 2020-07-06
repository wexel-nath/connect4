import matplotlib.pyplot as plt

from util import get_full_file_path


def plot_win_rates(filename: str, display: bool):
    graph_data = open(filename, "r").read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(",")
            xs.append(int(x))
            ys.append(float(y))

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(xs, ys, lw=0.5)
    ax.set_xlabel("Number of games")
    ax.set_ylabel("Win rate (%)")
    fig.savefig(get_full_file_path("win_rates.png"))

    if display:
        plt.show()


if __name__ == "__main__":
    plot_win_rates(get_full_file_path("win_rates.csv"), display=True)
