# This file is part of the U2.Suite.Python distribution
# (https://github.com/ut8uu/U2.Suite.Python).
# 
# Copyright (c) 2022 Sergey Usmanov, UT8UU.
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
import logging
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import brandmeister.bm_groups as bm_groups
import brandmeister.bm_monitor_constants as const
from brandmeister.bm_monitor_core import BrandmeisterMonitorCore, MonitorReportData
from brandmeister.bm_monitor_database import BmMonitorDatabase
from brandmeister.ui.Ui_BmMonitorMainWindow import Ui_BmMonitorMainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyledItemDelegate
from PyQt5 import QtGui, QtCore

from helpers.FileSystemHelper import FileSystemHelper

class StyledItemDelegate(QStyledItemDelegate):
    checked = QtCore.pyqtSignal(QtCore.QModelIndex, int)
    def editorEvent(self, event, model, option, index):
        if model.flags(index) & QtCore.Qt.ItemIsUserCheckable:
            # before the change
            last_value = index.data(QtCore.Qt.CheckStateRole)
        value = QStyledItemDelegate.editorEvent(self, event, model, option, index)
        if model.flags(index) & QtCore.Qt.ItemIsUserCheckable:
            # after the change
            new_value = index.data(QtCore.Qt.CheckStateRole)
            if last_value != new_value:
                self.checked.emit(index, new_value)
        return value

logging.basicConfig(filename='bm_monitor.log',
                    level='DEBUG',
                    filemode='a',
                    format='%(name)s: %(levelname)s - %(message)s')
logging.info('======================================================')
logging.info('Application started')

class BrandmeisterMonitor(QMainWindow, Ui_BmMonitorMainWindow):
    '''Represents a brandmeister monitor application.'''
    
    _db : BmMonitorDatabase
    _monitor_core : BrandmeisterMonitorCore
    _logger : logging.Logger
    
    '''==============================================================='''    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        self._monitor_core = BrandmeisterMonitorCore()
        self._monitor_core.MonitorReport.report.connect(self.monitor_reported)

        log_level = logging.getLevelName(self._monitor_core.Preferences.LogLevel)
        self._logger = logging.getLogger("bm")
        console_handler = logging.StreamHandler()
        self._logger.addHandler(console_handler)
        self._logger.setLevel(log_level)

        path = Path(self._monitor_core.Preferences.PathToDatabase)
        self._logger.debug(f'Path to db: {path}')
        self._db = BmMonitorDatabase(path)
        
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QtGui.QIcon(FileSystemHelper.relpath('icon/radio-48.png')))
        
        self.actionExit.triggered.connect(self.close_window)
        self.actionStart.triggered.connect(self.start_monitor)
        self.actionStop.triggered.connect(self.stop_monitor)

        pref = self._monitor_core.Preferences
        self.cbCallsigns.setChecked(pref.UseCallsigns)
        self.tbCallsigns.setPlainText(','.join(pref.Callsigns))
        self.tbCallsigns.setEnabled(pref.UseCallsigns)

        self.cbTalkGroups.setChecked(pref.UseTalkGroups)
        self.cbDisplayAllGroups.setChecked(pref.DisplayAllTalkGroups)
        
        model = QtGui.QStandardItemModel()
        for group_id in bm_groups.bm_groups:
            group_title = bm_groups.bm_groups[group_id]
            item = QtGui.QStandardItem(f'[{group_id}] {group_title}')
            is_checked = int(group_id) in pref.TalkGroups
            check = QtCore.Qt.CheckState.Checked if is_checked else QtCore.Qt.CheckState.Unchecked
            item.setCheckState(check)
            item.setCheckable(True)
            model.appendRow(item)
        self.lbGroups.setModel(model)
        
        self.lbGroups.setEnabled(pref.UseTalkGroups)
        
        self.cbTalkGroups.stateChanged.connect(self.update_preferences)
        self.cbDisplayAllGroups.stateChanged.connect(self.update_preferences)
        self.cbCallsigns.stateChanged.connect(self.update_preferences)
        self.tbCallsigns.textChanged.connect(self.update_preferences)        
        
        delegate = StyledItemDelegate()
        delegate.checked.connect(self.lbgroups_on_checked)
        self.lbGroups.setItemDelegate(delegate)

        self.start_monitor()
            
    '''================================================================'''
    def lbgroups_on_checked(self, index, state):
        '''Handles checking/unchecking of the item in the groups list view.'''
        text = f'Group {index.data()} is '
        
        if state == QtCore.Qt.CheckState.Unchecked:
            text += 'un'
        text += 'checked.'
        self._logger.debug(text)
        self.update_preferences()
        
    '''==============================================================='''    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self._monitor_core.Stop()
        return super().closeEvent(a0)

    '''==============================================================='''
    def monitor_reported(self, data : MonitorReportData) -> None:
        '''Handles reporting of data from the monitor.'''
        timestamp = data.Timestamp.strftime('%d.%m.%Y %H:%M:%S')
        line = (
            f'{timestamp.rjust(16)} '
            f'{str(data.TG).rjust(6)} '
            f'{data.Callsign.ljust(12)} '
            f'{data.Duration}s'
            )
        self._logger.debug(f'Received report: {line}')
        self.monitoringList.addItem(line)
        self._db.insert_report(data)
        
    '''==========================================================================='''
    def GetPathToDatabase(self) -> Path:
        '''Calculates the full path to the database'''
        return FileSystemHelper.get_appdata_path(Path('U2.Suite') / 'BmMonitor' / 'Database', create_if_not_exists=True)

    '''==============================================================='''
    def update_preferences(self) -> None:
        '''Updates preferences according to the current window state.'''
        self._monitor_core.Preferences.UseCallsigns = self.cbCallsigns.isChecked()
        self.tbCallsigns.setEnabled(self.cbCallsigns.isChecked())
        callsigns = self.tbCallsigns.toPlainText().split(',')
        self._monitor_core.Preferences.Callsigns = callsigns

        self._monitor_core.Preferences.UseTalkGroups = self.cbTalkGroups.isChecked()
        self._monitor_core.Preferences.DisplayAllTalkGroups = self.cbDisplayAllGroups.isChecked()
        self.cbTalkGroups.setEnabled(self.cbTalkGroups.isChecked())
        groups = []
        model = self.lbGroups.model()
        item : QtGui.QStandardItem
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == QtCore.Qt.Checked:
                text = item.text().split(' ')[0].lstrip('[').rstrip(']')
                group_id = int(text)
                groups.append(group_id)
        self._monitor_core.Preferences.TalkGroups = groups
        
        self._monitor_core.Preferences.write_preferences()
        
    '''==============================================================='''    
    def start_monitor(self):
        if not self.actionStart.isEnabled():
            return

        self.actionStart.setEnabled(False)
        self.actionStop.setEnabled(True)
        self._monitor_core.Start()
    
    '''==============================================================='''    
    def stop_monitor(self):
        if not self.actionStop.isEnabled():
            return

        self.actionStart.setEnabled(True)
        self.actionStop.setEnabled(False)
        self._monitor_core.Stop()
    
    '''==============================================================='''    
    def close_window(self):
        self.close()
    
'''==============================================================='''    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font_dir = FileSystemHelper.relpath("font")
    families = FileSystemHelper.load_fonts_from_dir(os.fspath(font_dir))

    window = BrandmeisterMonitor()

    window.show()

    app.exec()
    window.destroy()
    del window
