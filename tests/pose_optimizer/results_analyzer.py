import pandas as pd
import pathlib

from tests.tools.fig_maker import FigMaker

current_dir = pathlib.Path(__file__).resolve().parent

#TODO: modify to log selectable
log_dir = str(current_dir) + '/log/with_full_keyframe_position/'

fps = pd.read_csv(log_dir + 'fp_trajectory.csv')
fps_true = pd.read_csv(log_dir + 'fp_true_position.csv')

figMaker = FigMaker('featuer points trajectory', True)

plot_data = []
for fp_num in range(int(len(fps.columns) / 3)):
    n = 'fp_' + str(fp_num)
    l = [n + axis for axis in 'XYZ']
    plot_data += [[fps[l[0]], fps[l[1]], fps[l[2]], n]]

figMaker.add_plot(plot_data)

plot_data = []
for fp_num in range(int(len(fps_true.columns) / 3)):
    n = 'fp_' + str(fp_num)
    l = [n + axis for axis in 'XYZ']
    n = 'ture_' + n
    plot_data += [[fps_true[l[0]], fps_true[l[1]], fps_true[l[2]], n]]

figMaker.add_scatter(plot_data, 20)

figMaker.write()



kfs = pd.read_csv(log_dir + 'kf_trajectory.csv')
kfs_true = pd.read_csv(log_dir + 'kf_true_position.csv')

figMaker = FigMaker('keyframe trajectory', True)

plot_data = []
for kf_num in range(int(len(kfs.columns) / 3)):
    n = 'kf_' + str(kf_num)
    l = [n + axis for axis in 'XYZ']
    plot_data += [[kfs[l[0]], kfs[l[1]], kfs[l[2]], n]]

figMaker.add_plot(plot_data)

plot_data = []
for kf_num in range(int(len(kfs_true.columns) / 3)):
    n = 'kf_' + str(kf_num)
    l = [n + axis for axis in 'XYZ']
    n = 'ture_' + n
    plot_data += [[kfs_true[l[0]], kfs_true[l[1]], kfs_true[l[2]], n]]

print(plot_data)
figMaker.add_scatter(plot_data, 20)

figMaker.write()
