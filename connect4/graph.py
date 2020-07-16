import matplotlib.pyplot as plt
import numpy as np

from util import get_full_file_path


def plot_win_rates(filename: str, display: bool):
    x, _, ma = np.loadtxt(filename, unpack=True, delimiter=',')

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(x, ma, lw=0.5)
    ax.set_xlabel("Number of games")
    ax.set_ylabel("Win rate (%)")
    fig.savefig(filename + ".png")

    if display:
        plt.show()


if __name__ == "__main__":
    plot_win_rates(get_full_file_path("win_rates.csv"), display=True)
