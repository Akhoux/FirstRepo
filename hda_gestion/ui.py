from PySide2 import QtWidgets, QtCore
import hou
import os
from typing import List

default_folder_path = "/Users/akhoux/LifeDisk/Pro/Dev/courcpp"

def get_folder_contents(folder_path: str) -> List[str]:
    if not os.path.isdir(folder_path):
        hou.ui.displayMessage("Folder path is not valid.")
        return []

    folder_contents = []
    for item in os.listdir(folder_path):
        full_path = os.path.join(folder_path, item)
        if os.path.isdir(full_path):
            folder_contents.append(full_path)

    return folder_contents

def get_files_in_folder(folder_path: str) -> List[str]:
    if not os.path.isdir(folder_path):
        return []

    files = []
    for item in os.listdir(folder_path):
        full_path = os.path.join(folder_path, item)
        if os.path.isfile(full_path):
            files.append(full_path)

    return files

class PresetSelector(QtWidgets.QDialog):
    def __init__(self, folder_path: str, parent=None) -> None:
        super(PresetSelector, self).__init__(parent)

        self.setWindowTitle("Select a Preset")
        self.setMinimumWidth(600)

        self.presets = get_folder_contents(folder_path)

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems([os.path.basename(p) for p in self.presets])

        self.path_map = {os.path.basename(p): p for p in self.presets}

        self.combo_box.currentIndexChanged.connect(self.update_files_list)

        self.files_list_widget = QtWidgets.QListWidget()
        self.files_list_widget.itemClicked.connect(self.file_clicked)

        layout = QtWidgets.QHBoxLayout()

        combo_layout = QtWidgets.QVBoxLayout()
        combo_layout.addWidget(self.combo_box)

        file_list_layout = QtWidgets.QVBoxLayout()
        file_list_layout.addWidget(self.files_list_widget)

        layout.addLayout(combo_layout)
        layout.addLayout(file_list_layout)
        self.setLayout(layout)

        self.update_files_list()

    def update_files_list(self) -> None:
        selected_name = self.combo_box.currentText()
        selected_folder = self.path_map.get(selected_name, "")

        if os.path.isdir(selected_folder):
            files = get_files_in_folder(selected_folder)

            self.files_list_widget.clear()
            for file in files:
                item = QtWidgets.QListWidgetItem(os.path.basename(file))
                item.setData(QtCore.Qt.UserRole, file)
                self.files_list_widget.addItem(item)

    def file_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        file_path = item.data(QtCore.Qt.UserRole)
        hou.ui.displayMessage(f"Clicked on file: {file_path}")

def show_preset_selector(folder_path: str) -> None:
    dialog = PresetSelector(folder_path, hou.ui.mainQtWindow())
    dialog.exec_()

show_preset_selector(default_folder_path)
