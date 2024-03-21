from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QButtonGroup, QHeaderView


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.showFullScreen()
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setMinimumSize(QtCore.QSize(800, 800))
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setTabletTracking(True)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 0, 0, 1, 1)
        #
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        # draw roi :下拉框
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setObjectName("comboBox")
        # 下拉框个数
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 3)
        # draw minimum roi :下拉框
        self.detect_size = QtWidgets.QComboBox(Form)
        self.detect_size.setObjectName("detects size")
        # 下拉框个数
        self.detect_size.addItem("")
        self.detect_size.addItem("")
        self.gridLayout.addWidget(self.detect_size, 1, 0, 1, 3)

        # import image button
        self.loadButton = QtWidgets.QPushButton(Form)
        self.loadButton.setObjectName("load image")
        self.gridLayout.addWidget(self.loadButton, 2, 0, 1, 3)

        # form function check box - draw Person roi
        self.Person_ROI = QtWidgets.QCheckBox(Form)
        self.Person_ROI.setObjectName("Person")
        self.gridLayout.addWidget(self.Person_ROI, 3, 0, 1, 1)
        # form function check box - draw PPE roi
        self.PPE_ROI = QtWidgets.QCheckBox(Form)
        self.PPE_ROI.setObjectName("PPE")
        self.gridLayout.addWidget(self.PPE_ROI, 3, 1, 1, 1)
        # form function check box - draw Falldown roi
        self.Falldown_ROI = QtWidgets.QCheckBox(Form)
        self.Falldown_ROI.setObjectName("Falldown")
        self.gridLayout.addWidget(self.Falldown_ROI, 3, 2, 1, 1)
        # form
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 設置tablewidget不可編輯
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)  # 設置tablewidget不可被選取
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        # form title style
        self.tableWidget.horizontalHeader().setFixedHeight(100)
        self.tableWidget.verticalHeader().setFixedWidth(100)
        self.tableWidget.verticalHeader().setVisible(False)
        # form content row1
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        # form content row2 - delete specific roi
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.tableWidget, 4, 0, 1, 3)
        # form layout
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 2, 1)
        # function button overview
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        # form function button - clear all roi
        self.ClearROIButton = QtWidgets.QPushButton(Form)
        self.ClearROIButton.setObjectName("ClearROIButton")
        self.gridLayout_3.addWidget(self.ClearROIButton, 0, 0, 1, 1)
        # form function button - confirm roi and save
        self.confirmROIButton = QtWidgets.QPushButton(Form)
        self.confirmROIButton.setObjectName("confirmROIButton")
        self.gridLayout_3.addWidget(self.confirmROIButton, 0, 1, 1, 1)

        # form function button - exit
        self.exitButton = QtWidgets.QPushButton(Form)
        self.exitButton.setObjectName("ExitButton")
        self.gridLayout_3.addWidget(self.exitButton, 0, 3, 1, 1)
        # function layout
        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        #
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "ROI"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "delete"))
        # 下拉式表單選項 : roi 形狀
        self.comboBox.setItemText(0, _translate("MainWindowv", "draw Rect ROI"))
        self.comboBox.setItemText(1, _translate("MainWindowv", "draw MultiRect ROI"))
        # 下拉式表單選項 : 偵測大小限制 roi
        self.detect_size.setItemText(0, _translate("MainWindowv", "draw minimum ROI"))
        self.detect_size.setItemText(1, _translate("MainWindowv", "draw maximum ROI"))

        self.loadButton.setText(_translate("MainWindowv", "Load Image"))

        #
        self.Person_ROI.setText(_translate("Form", "Person ROI"))
        self.PPE_ROI.setText(_translate("Form", "PPE ROI"))
        self.Falldown_ROI.setText(_translate("Form", "Falldown ROI"))

        self.ClearROIButton.setText(_translate("Form", "ClearROI"))
        # draw ROI confirm
        self.confirmROIButton.setText(_translate("Form", "draw ROI finish"))
        self.exitButton.setText(_translate("Form", "Exit"))

