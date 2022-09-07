import pandas as pd
import pathlib

from tests.tools.fig_maker import FigMaker

current_dir = pathlib.Path(__file__).resolve().parent
log_dir = str(current_dir) + '/log/'

fps = pd.read_csv(log_dir + 'fp_position_trajectory.csv')
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
