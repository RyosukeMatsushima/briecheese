import pandas as pd
import pathlib
import argparse
import sys
from mpl_toolkits.mplot3d import Axes3D

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../../")

from tests.tools.fig_maker import FigMaker

ap = argparse.ArgumentParser()
ap.add_argument("log_file_name")
args = ap.parse_args()
log_file_name = args.log_file_name

current_dir = pathlib.Path(__file__).resolve().parent

# TODO: modify to log selectable
log_dir = str(current_dir) + "/log/" + log_file_name + "/"

fps = pd.read_csv(log_dir + "fp_trajectory.csv")
fps_true = pd.read_csv(log_dir + "fp_true_position.csv")

figMaker = FigMaker("featuer points trajectory", True)

plot_data = []
for fp_num in range(int(len(fps.columns) / 3)):
    n = "fp_" + str(fp_num)
    list = [n + axis for axis in "XYZ"]
    plot_data += [[fps[list[0]], fps[list[1]], fps[list[2]], n]]

figMaker.add_plot(plot_data)

plot_data = []
for fp_num in range(int(len(fps_true.columns) / 3)):
    n = "fp_" + str(fp_num)
    list = [n + axis for axis in "XYZ"]
    n = "ture_" + n
    plot_data += [[fps_true[list[0]], fps_true[list[1]], fps_true[list[2]], n]]

figMaker.add_scatter(plot_data, 20)

figMaker.write()


kfs = pd.read_csv(log_dir + "kf_trajectory.csv")
kfs_true = pd.read_csv(log_dir + "kf_true_position.csv")

figMaker = FigMaker("keyframe trajectory", True)

plot_data = []
for kf_num in range(int(len(kfs.columns) / 3)):
    n = "kf_" + str(kf_num)
    list = [n + axis for axis in "XYZ"]
    plot_data += [[kfs[list[0]], kfs[list[1]], kfs[list[2]], n]]

figMaker.add_plot(plot_data)

plot_data = []
for kf_num in range(int(len(kfs_true.columns) / 3)):
    n = "kf_" + str(kf_num)
    list = [n + axis for axis in "XYZ"]
    n = "ture_" + n
    plot_data += [[kfs_true[list[0]], kfs_true[list[1]], kfs_true[list[2]], n]]

figMaker.add_scatter(plot_data, 20)

plot_data = []
for kf_num in range(int(len(kfs.columns) / 3)):
    n = "kf_" + str(kf_num)
    list = [n + axis for axis in "XYZ"]
    plot_data += [[kfs[list[0]][0], kfs[list[1]][0], kfs[list[2]][0], n]]

figMaker.add_scatter(plot_data, 10)

figMaker.write()
