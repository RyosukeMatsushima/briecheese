import matplotlib.pyplot as plt


class FigMaker:
    def __init__(self, title, is_3d):
        self.fig = plt.figure(figsize=(10, 10))
        self.is_3d = is_3d

        if self.is_3d:
            self.ax = self.fig.add_subplot(111, projection="3d")
        else:
            self.ax = self.fig.add_subplot(111)

        self.ax.set_title(title)

    def add_plot(self, data_list):
        for data in data_list:
            if self.is_3d:
                self.ax.plot(data[0], data[1], data[2], label=data[3])
            else:
                self.ax.plot(data[0], data[1], label=data[2])

    def add_scatter(self, data_list, s):
        for data in data_list:
            if self.is_3d:
                self.ax.scatter(data[0], data[1], data[2], s=s)
            else:
                self.ax.scatter(data[0], data[1], s=s)

    def write(self):
        plt.legend()
        plt.show()
