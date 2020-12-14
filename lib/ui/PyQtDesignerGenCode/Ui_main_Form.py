# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Movie_Aleter_UI.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_Form(object):
    def setupUi(self, main_Form):
        main_Form.setObjectName("main_Form")
        main_Form.resize(546, 302)
        main_Form.setToolTip("")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(main_Form)
        self.doubleSpinBox.setGeometry(QtCore.QRect(140, 40, 41, 22))
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setMinimum(1.0)
        self.doubleSpinBox.setMaximum(10.0)
        self.doubleSpinBox.setSingleStep(0.1)
        self.doubleSpinBox.setProperty("value", 6.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.rating_label = QtWidgets.QLabel(main_Form)
        self.rating_label.setGeometry(QtCore.QRect(50, 40, 81, 21))
        self.rating_label.setScaledContents(False)
        self.rating_label.setObjectName("rating_label")
        self.spinBox = QtWidgets.QSpinBox(main_Form)
        self.spinBox.setGeometry(QtCore.QRect(141, 70, 61, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(999000)
        self.spinBox.setSingleStep(10)
        self.spinBox.setObjectName("spinBox")
        self.min_votes_label = QtWidgets.QLabel(main_Form)
        self.min_votes_label.setGeometry(QtCore.QRect(50, 70, 71, 20))
        self.min_votes_label.setObjectName("min_votes_label")
        self.exit_pushButton = QtWidgets.QPushButton(main_Form)
        self.exit_pushButton.setGeometry(QtCore.QRect(30, 260, 75, 23))
        self.exit_pushButton.setObjectName("exit_pushButton")
        self.blacklist_listWidget = QtWidgets.QListWidget(main_Form)
        self.blacklist_listWidget.setGeometry(QtCore.QRect(290, 90, 211, 161))
        self.blacklist_listWidget.setObjectName("blacklist_listWidget")
        self.blacklist_lineEdit = QtWidgets.QLineEdit(main_Form)
        self.blacklist_lineEdit.setGeometry(QtCore.QRect(290, 60, 161, 20))
        self.blacklist_lineEdit.setClearButtonEnabled(True)
        self.blacklist_lineEdit.setObjectName("blacklist_lineEdit")
        self.blacklist_label = QtWidgets.QLabel(main_Form)
        self.blacklist_label.setGeometry(QtCore.QRect(290, 30, 141, 21))
        self.blacklist_label.setObjectName("blacklist_label")
        self.blacklist_add_pushButton = QtWidgets.QPushButton(main_Form)
        self.blacklist_add_pushButton.setGeometry(QtCore.QRect(460, 60, 31, 23))
        self.blacklist_add_pushButton.setObjectName("blacklist_add_pushButton")
        self.blacklist_del_pushButton = QtWidgets.QPushButton(main_Form)
        self.blacklist_del_pushButton.setGeometry(QtCore.QRect(500, 60, 31, 23))
        self.blacklist_del_pushButton.setObjectName("blacklist_del_pushButton")
        self.pb_lineEdit = QtWidgets.QLineEdit(main_Form)
        self.pb_lineEdit.setGeometry(QtCore.QRect(110, 160, 171, 20))
        self.pb_lineEdit.setObjectName("pb_lineEdit")
        self.pb_label = QtWidgets.QLabel(main_Form)
        self.pb_label.setGeometry(QtCore.QRect(10, 160, 101, 20))
        self.pb_label.setObjectName("pb_label")
        self.sc_spinBox = QtWidgets.QSpinBox(main_Form)
        self.sc_spinBox.setGeometry(QtCore.QRect(140, 100, 42, 22))
        self.sc_spinBox.setMaximum(168)
        self.sc_spinBox.setProperty("value", 12)
        self.sc_spinBox.setObjectName("sc_spinBox")
        self.sc_label = QtWidgets.QLabel(main_Form)
        self.sc_label.setGeometry(QtCore.QRect(50, 100, 71, 16))
        self.sc_label.setObjectName("sc_label")
        self.sc_hours_label = QtWidgets.QLabel(main_Form)
        self.sc_hours_label.setGeometry(QtCore.QRect(190, 110, 47, 13))
        self.sc_hours_label.setObjectName("sc_hours_label")
        self.bo_url_lineEdit = QtWidgets.QLineEdit(main_Form)
        self.bo_url_lineEdit.setGeometry(QtCore.QRect(90, 200, 191, 20))
        self.bo_url_lineEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.bo_url_lineEdit.setObjectName("bo_url_lineEdit")
        self.bo_url_label = QtWidgets.QLabel(main_Form)
        self.bo_url_label.setGeometry(QtCore.QRect(10, 200, 71, 16))
        self.bo_url_label.setObjectName("bo_url_label")
        self.start_pushButton = QtWidgets.QPushButton(main_Form)
        self.start_pushButton.setGeometry(QtCore.QRect(120, 260, 75, 23))
        self.start_pushButton.setObjectName("start_pushButton")

        self.retranslateUi(main_Form)
        QtCore.QMetaObject.connectSlotsByName(main_Form)

    def retranslateUi(self, main_Form):
        _translate = QtCore.QCoreApplication.translate
        main_Form.setWindowTitle(_translate("main_Form", "Movie Alerter"))
        self.rating_label.setText(_translate("main_Form", "Minimum Rating"))
        self.min_votes_label.setText(_translate("main_Form", "Minimum Votes"))
        self.exit_pushButton.setText(_translate("main_Form", "Exit"))
        self.blacklist_label.setText(_translate("main_Form", "Add Blacklisted Categories"))
        self.blacklist_add_pushButton.setText(_translate("main_Form", "Add"))
        self.blacklist_del_pushButton.setText(_translate("main_Form", "Del"))
        self.pb_label.setText(_translate("main_Form", "Push Bullet API Key"))
        self.sc_label.setText(_translate("main_Form", "Check Every"))
        self.sc_hours_label.setText(_translate("main_Form", "hours"))
        self.bo_url_lineEdit.setToolTip(_translate("main_Form", "Box Office URL in case it changes. You probably don\'t need to change this."))
        self.bo_url_lineEdit.setText(_translate("main_Form", "https://www.imdb.com/chart/boxoffice?ref_=nv_ch_cht_2"))
        self.bo_url_label.setText(_translate("main_Form", "Box Office Url"))
        self.start_pushButton.setText(_translate("main_Form", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_Form = QtWidgets.QWidget()
    ui = Ui_main_Form()
    ui.setupUi(main_Form)
    main_Form.show()
    sys.exit(app.exec_())
