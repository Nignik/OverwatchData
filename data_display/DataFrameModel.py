import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt


class DataFrameModel(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self._df = df

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            value = self._df.iloc[index.row(), index.column()]
            return str(value)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[section]
            if orientation == Qt.Vertical:
                return str(self._df.index[section])
        return None


class DataFrameViewer(QMainWindow):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.setWindowTitle("Pandas DataFrame Viewer")

        # Create a QTableView widget
        self.table_view = QTableView()
        self.setCentralWidget(self.table_view)

        # Set the model
        self.model = DataFrameModel(df)
        self.table_view.setModel(self.model)