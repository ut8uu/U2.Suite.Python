import sys

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from RigSelectorDialog import RigSelectorDialog
from MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    rig_selector = RigSelectorDialog()
    dialog_code = rig_selector.exec()
    print(dialog_code)
    
    print('Rig selected')
    
    selected_rig = rig_selector.getSelectedRig()
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec_())
