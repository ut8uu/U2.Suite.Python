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

import os
import sys
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QDialog

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import brandmeister.BmGroups as BmGroups
from brandmeister.BmMonitorPreferences import BrandmeisterMonitorApplicationPreferences
from brandmeister.ui.Ui_BmMonitorPreferences import Ui_BmPreferencesDialog
import brandmeister.BmMonitorConstants as const
import common.data.dxcc as dxcc
from helpers.FileSystemHelper import FileSystemHelper

class PreferencesDialogEvent(QObject):
    """
    Custom qt event signal used when something in station info was updated.
    """
    changed = pyqtSignal()
    dialogClosed = pyqtSignal()


class BmMonitor_PreferencesDialog(QDialog, Ui_BmPreferencesDialog):
    """Represents Preferences dialog."""
    
    _preferences : BrandmeisterMonitorApplicationPreferences
    change_event : PreferencesDialogEvent
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        
        self.setupUi(self)

        self.change_event = PreferencesDialogEvent()

        self.buttonBox.accepted.connect(self.save_changes)
        self.buttonBox.rejected.connect(self.close_dialog)

        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(FileSystemHelper.relpath('icon/radio-48.png')))
    
    """---------------------------------------------------------------------------"""
    def setup(self, preferences : BrandmeisterMonitorApplicationPreferences) -> None:
        """Initiates the dialog with data."""

        self._preferences = preferences
        
        # filter (general)
        self.udSilenceDuration.setValue(preferences.MinSilenceSec)
        self.udTransmissionDuration.setValue(preferences.MinDurationSec)
        
        # filter (TG)
        self.cbFilterByTG.setChecked(preferences.UseTalkGroups)
        model = QStandardItemModel()
        all_groups = preferences.TalkGroups
        for group_id in BmGroups.bm_groups:
            group_title = BmGroups.bm_groups[group_id]
            item = QStandardItem(f'[{group_id}] {group_title}')
            is_checked = int(group_id) in all_groups
            check = Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked
            item.setCheckState(check)
            item.setCheckable(True)
            item.data = group_id
            model.appendRow(item)
        self.lbGroups.setModel(model)
        
        # DXCC-related stuff
        self.cbFilterByDxcc.setChecked(preferences.UseCountries)

        all_countries = preferences.Countries
        dxcc_model = QStandardItemModel()
        
        entries = dict(sorted(dxcc.Countries.items(), key=lambda item: item[1]))
        for country_id in entries:
            country_title = dxcc.Countries[country_id]
            item = QStandardItem(country_title)
            is_checked = int(country_id) in all_countries
            check = Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked
            item.setCheckState(check)
            item.setCheckable(True)
            item.data = country_id
            dxcc_model.appendRow(item)
        self.lbCountries.setModel(dxcc_model)

        # storage
        self.tbPathToDb.setText(preferences.PathToDatabase)
        self.cbSaveToDb.setChecked(preferences.SaveToDatabase)
        self.cbDbStorageLimit.setCurrentText(preferences.SaveToDatabaseLimit)
        
        # setup the filter combobox
        self.cbDbStorageLimit.clear()
        self.cbDbStorageLimit.addItems([
            const.DB_LIMIT_NO_LIMIT,
            const.FILTER_LAST_1000,
            const.FILTER_LAST_5MINUTES,
            const.FILTER_LAST_HOUR,
            const.FILTER_LAST_6HOURS,
            const.FILTER_LAST_12HOURS,
            const.FILTER_LAST_DAY,
            const.FILTER_LAST_WEEK,
        ])
        self.cbDbStorageLimit.setCurrentText(preferences.SaveToDatabaseLimit)        
        
    """==============================================================="""
    def close_dialog(self) -> None:
        self.close()

    """==============================================================="""
    def save_changes(self) -> None:
        """Saves changes to preferences file."""
        
        pp = self._preferences
        
        # filter - options
        pp.MinDurationSec = self.udTransmissionDuration.value()
        pp.MinSilenceSec = self.udSilenceDuration.value()
        
        # storage
        pp.SaveToDatabase = self.cbSaveToDb.isChecked()
        pp.SaveToDatabaseLimit = self.cbDbStorageLimit.currentText()
        pp.PathToDatabase = self.tbPathToDb.text()
        
        # filter - callsigns        
        callsigns = self.tbCallsigns.toPlainText().split(',')
        pp.Callsigns = callsigns
        pp.UseCallsigns = self.cbFilterByCallsigns.isChecked()

        # filter - TG
        pp.UseTalkGroups = self.cbFilterByTG.isChecked()
        self.cbFilterByTG.setEnabled(self.cbFilterByTG.isChecked())
        groups = []
        model = self.lbGroups.model()
        item : QStandardItem
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == Qt.Checked:
                text = item.text().split(' ')[0].lstrip('[').rstrip(']')
                group_id = int(text)
                groups.append(group_id)
        pp.TalkGroups = groups
        
        # filter - DXCC
        countries = []
        model = self.lbCountries.model()
        item : QStandardItem
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == Qt.Checked:
                country_id = int(item.data)
                countries.append(country_id)
        pp.Countries = countries
        pp.UseCountries = self.cbFilterByDxcc.isChecked()
                
        self._preferences.write_preferences()
        self.change_event.changed.emit()
        self.close()
        
"""==============================================================="""
if __name__ == '__main__':
    """Launched directly. Consider a test run."""
    import os
    app = QApplication(sys.argv)
    preferences = BrandmeisterMonitorApplicationPreferences()
    preferences.SaveToDatabase = True
    preferences.PathToDatabase = 'd:\\tmp\\db.sqlite'
    preferences.SaveToDatabaseLimit = const.FILTER_LAST_12HOURS
    preferences.Callsigns = ['UT8UU', 'UT3UBR']
    preferences.UseCallsigns = True
    preferences.Countries = [1, 2, 3]
    preferences.UseCountries = True
    preferences.TalkGroups = [91, 310]
    preferences.UseTalkGroups = True

    # an instance of the window using the default path and name of the database
    dialog = BmMonitor_PreferencesDialog()
    dialog.setup(preferences)
    dialog.open()
    app.exec()
