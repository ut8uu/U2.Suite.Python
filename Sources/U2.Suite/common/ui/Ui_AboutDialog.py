# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Projects\Git\_U2\U2.Suite.Python\Sources\U2.Suite\common\ui\AboutDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(612, 352)
        AboutDialog.setStyleSheet("background-color: rgb(46, 52, 54); color: rgb(211, 215, 207);")
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setGeometry(QtCore.QRect(470, 300, 121, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lblAppName = QtWidgets.QLabel(AboutDialog)
        self.lblAppName.setGeometry(QtCore.QRect(280, 20, 320, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lblAppName.setFont(font)
        self.lblAppName.setObjectName("lblAppName")
        self.lblVersion = QtWidgets.QLabel(AboutDialog)
        self.lblVersion.setGeometry(QtCore.QRect(280, 70, 320, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblVersion.setFont(font)
        self.lblVersion.setObjectName("lblVersion")
        self.lblCopyright = QtWidgets.QLabel(AboutDialog)
        self.lblCopyright.setGeometry(QtCore.QRect(280, 100, 320, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblCopyright.setFont(font)
        self.lblCopyright.setObjectName("lblCopyright")
        self.lblAppDescription = QtWidgets.QLabel(AboutDialog)
        self.lblAppDescription.setGeometry(QtCore.QRect(280, 140, 320, 120))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblAppDescription.setFont(font)
        self.lblAppDescription.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblAppDescription.setWordWrap(True)
        self.lblAppDescription.setObjectName("lblAppDescription")
        self.imageLabel = QtWidgets.QLabel(AboutDialog)
        self.imageLabel.setGeometry(QtCore.QRect(10, 20, 251, 250))
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")

        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(AboutDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About"))
        self.lblAppName.setText(_translate("AboutDialog", "App Name"))
        self.lblVersion.setText(_translate("AboutDialog", "version 1.0"))
        self.lblCopyright.setText(_translate("AboutDialog", "(c) 2022-2023 Sergey Usmanov, UT8UU"))
        self.lblAppDescription.setText(_translate("AboutDialog", "A description of the product."))
