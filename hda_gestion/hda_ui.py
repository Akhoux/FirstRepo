import hou
from PySide2 import QtWidgets


# Function to create the custom pane
def create_custom_pane():
    # Set up the pane and its window properties
    pane_tab = hou.ui.createFloatingPanel(hou.paneTabType.PythonPanel)
    pane_tab.setName("Custom Editor")
    # Load a custom interface in PySide2 here (add buttons, dropdowns, etc.)

    # Example layout
    window = pane_tab
    layout = QtWidgets.QVBoxLayout()
    label = QtWidgets.QLabel("This is a custom editor window.")
    layout.addWidget(label)

    # Assuming a main widget to add the layout
    main_widget = QtWidgets.QWidget()
    main_widget.setLayout(layout)

    return pane_tab

# Call the function to open the custom pane
create_custom_pane()