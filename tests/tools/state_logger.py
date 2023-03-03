import pandas as pd


class StateLogger:
    def __init__(self, file_name, columns):
        self.file_name = file_name
        self.columns = columns
        self.data_stock = []

        df = pd.DataFrame(columns=self.columns)
        df.to_csv(self.file_name)

    def add_data(self, data):
        self.data_stock.append(data)

        if len(self.data_stock) > 100000:
            self.save_to_file()

    def finish(self):
        self.save_to_file()

    def save_to_file(self):
        if not self.data_stock:
            return

        df = pd.DataFrame(self.data_stock, columns=self.columns)
        df.to_csv(self.file_name, mode="a", header=False)
        self.data_stock = []
