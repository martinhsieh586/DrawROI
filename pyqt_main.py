import sys
from PyQt5.QtWidgets import *  # 引入PyQt相關類別
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# from pyqtgraph.graphicsItems import *
import pyqtgraph as pg
import math
from pyqt_ui import *  # 導入窗口介面
import numpy as np
from PIL import Image  # pillow
import os
import json
import qdarkstyle

global dir_str
global item
global pic
global grayimg  # Gray picture
global imgarray

class roiwidge(QWidget, Ui_Form):  # 介面布局自動縮放
    def __init__(self, parent=None):
        super(roiwidge, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("ROI")

        self.graphicsView.mouseReleaseEvent = self.gpmouseReleaseEvent
        self.graphicsView.mousePressEvent = self.gpmousePressEvent

        ## 如果要用載入圖片功能
        self.loadButton.clicked.connect(self.load_click)
        self.loadButton.setText("Select File")

        # 清除界面所有ROI
        self.ClearROIButton.clicked.connect(self.ClearAllROI)
        # draw ROI finish
        self.confirmROIButton.clicked.connect(self.confirmROI)
        # 退出界面設置
        self.exitButton.clicked.connect(self.set_quit)

        # img dir
        self.fname = 'output/down-arrow.png'
        # for save draw roi pos
        self.ROI_logging = {'person':dict(),'PPE':dict(),'fall down':dict(),'maximum':dict(),'minimum':dict()}
        self.ROI_view = dict()
        self.lastPoint = QPoint()
        self.endPoint = QPoint()
        self.points = list()  # 僅多邊形使用
        self.name = list()
        self.rect_draw_count = 0
        self.tmp_multi = list()

        self.qssStyle = '''
                    QHeaderView
                    {
                        background:transparent;
                    }
                    QHeaderView::section
                    {
                        font-size:20px;
                        font-family:"Microsoft JhengHei";
                        color:#FFFFFF;
                        background:#60669B;
                        border:none;
                        text-align:left;
                        min-height:49px;
                        max-height:49px;
                        margin-left:0px;
                        padding-left:0px;
                    }
                    QTableWidget
                    {
                        background:#FFFFFF;
                        border:none;
                        font-size:20px;
                        font-family:"Microsoft JhengHei";
                        color:#666666;
                    }
                    QTableWidget::item
                    {
                        font-size:20px;
                        font-family:"Microsoft JhengHei";
                        border-bottom:1px solid #EEF1F7 ;
                    }
                    
                    QTableWidget::item::selected
                    {
                        color:red;
                        background:#EFF4FF;
                    }
                    QScrollBar::handle:vertical
                    {
                        background: rgba(255,255,255,20%);
                        border: 0px solid grey;
                        border-radius:3px;
                        width: 8px;
                    }
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
                    {
                        background:rgba(255,255,255,10%);
                    }
                    QScollBar::add-line:vertical, QScrollBar::sub-line:vertical
                    {
                        background:transparent;
                    }
                    
                   QPushButton:hover{text-align : center;
                               background-color : rgb(150,150,255);
                               font : 20px \"Microsoft JhengHei\";
                               color:rgb(255, 255, 255);}
                   QPushButton{text-align : center;
                               background-color : rgb(0,0,255);
                               font : 20px \"Microsoft JhengHei\";
                               padding: none;
                               color:rgb(255, 255, 255);}
                   QCheckBox {font : 20px \"Microsoft JhengHei\";
                        color: #00f;
                    }
                    QCheckBox:hover {color:#f00;}
                    
                    QComboBox {
                        font : 18px \"Microsoft JhengHei\";
                        color:#666666;
                        padding: 1px 15px 1px 3px;
                        border:2px solid rgb(0,0,228);
                        border-radius:5px 5px 0px 0px;
                    }
                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 15px;
                        border:none;
                    }
                    QComboBox::down-arrow,QDateEdit::down-arrow {
                        top: 0px;
                        left: -10px;
                        image: url(icon/down-arrow.png);
                        width:20px;
                        height:20px;
                    }
                    QComboBox:on { 
                          padding-top: 3px;
                          padding-left: 4px;
                      }
                      QComboBox::down-arrow:on { 
                          top: 1px;
                          left: -7px;
                      }
                   '''
        self.setStyleSheet(self.qssStyle)
        # 計算圖片大小
        grayimg = Image.open(self.fname).convert('L')
        imgarray = np.asarray(grayimg)
        self.size_x = len(imgarray[0])
        self.size_y = len(imgarray)

        # 顯示
        self.display_image()

    # 載入圖檔
    def load_click(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open Image', 'Image', '*.png *.jpg *.bmp')
        if self.fname == '':
            return
        # 計算圖片大小
        grayimg = Image.open(self.fname).convert('L')
        imgarray = np.asarray(grayimg)
        self.size_x = len(imgarray[0])
        self.size_y = len(imgarray)
        if self.size_y == 1 or self.size_x == 1:
            return
        qimg = QImage(self.fname)
        pic = QPixmap.fromImage(qimg)
        item = QGraphicsPixmapItem(pic)
        self.scene = QGraphicsScene(0, 0, self.size_x, self.size_y)
        self.scene.addItem(item)
        self.graphicsView.setScene(self.scene)
        # 顯示
        self.display_image()

    # diplay image
    def display_image(self):
        qimg = QImage(self.fname)
        pic = QPixmap.fromImage(qimg)
        item = QGraphicsPixmapItem(pic)
        self.scene = QGraphicsScene(0, 0, self.size_x, self.size_y)
        self.scene.addItem(item)
        self.graphicsView.setScene(self.scene)

    # 滑鼠控制事件 : 滑鼠滾輪
    def wheelEvent(self, event):
        # 圖片縮放
        self.scaleView(math.pow(2.0, event.angleDelta().y() / 240.0))
        pass

    # 圖片縮放
    def scaleView(self, scaleFactor):
        factor = self.graphicsView.transform().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.graphicsView.scale(scaleFactor, scaleFactor)

    #  滑鼠控制事件 : 滑鼠點擊
    def gpmousePressEvent(self, event):
        # 按下鼠標左鍵
        if event.buttons() == QtCore.Qt.LeftButton:
            # 獲取座標位址 (QpointF.x,QpointF.y)
            point = self.graphicsView.mapToScene(event.pos())
            # pyqt的ui介面如果選擇畫多邊形 ROI
            if self.comboBox.currentText() == 'draw MultiRect ROI':
                self.points.append(point)
                self.test(points=self.points)
            # 若不是，記錄每次點擊的座標位址
            elif self.comboBox.currentText() == 'draw Rect ROI':
                self.lastPoint = point
        event.accept()
    # 當滑鼠點擊放開時
    def gpmouseReleaseEvent(self, event):
        if event.button() == 1:
            point = self.graphicsView.mapToScene(event.pos())
            self.endPoint = point
            (x, y, w, h) = self.caculat_Rec(self.lastPoint, self.endPoint)
            self.test((x, y), (w, h))

    # 計算矩形ROI的原點和長寬
    def caculat_Rec(self, pos1, pos2):
        x1 = pos1.x()
        x2 = pos2.x()
        y1 = pos1.y()
        y2 = pos2.y()

        if x1 >= x2:
            x = x2
        else:
            x = x1
        if y1 >= y2:
            y = y2
        else:
            y = y1
        h = abs(y1 - y2)
        w = abs(x1 - x2)
        return x, y, w, h

    # ROI : pos(x,y) , size(w,h), points : for MultiRectROI
    def test(self, pos=(0, 0), size=(0, 0), points=list()):
        global frame
        # 當上次畫完矩陣未儲存，自動刪除紀錄
        if len(self.name)!=self.rect_draw_count and len(points) <= 1:
            self.scene.removeItem(self.scene.items()[1])
            self.rect_draw_count -= 1
        # 如果使用者想畫矩形 ROI
        if self.comboBox.currentText() == 'draw Rect ROI':
            frame = pg.RectROI(pos, size, pen=pg.mkPen('g', width=4))
            self.scene.addItem(frame)
            self.points.clear()
            self.rect_draw_count += 1
        # 如果使用者想畫多邊形 ROI
        elif self.comboBox.currentText() == 'draw MultiRect ROI' and pos == (0, 0) and size == (0, 0):
            frame = pg.PolyLineROI(points, pen=pg.mkPen('g', width=4))
            self.scene.addItem(frame)
            self.tmp_multi.append(frame)

    def ClearAllROI(self):
        self.tableWidget.clearContents()    # 清空頁面暫存
        self.tableWidget.setRowCount(0)
        self.points.clear()
        self.name.clear()
        self.ROI_logging = {'person':dict(),'PPE':dict(),'fall down':dict(),'maximum':dict(),'minimum':dict()}
        self.ROI_view.clear()
        self.rect_draw_count=0
        for i in range(len(self.scene.items()) - 1):
            self.scene.removeItem(self.scene.items()[0])

    # ROI位址紀錄 pos : 矩形: [top_x, top_y , bottom_x, bottom_y]
    def ROI_pos_logging(self, pos):
        self.save_file = 'output/'
        # classify name
        if self.detect_size.currentText() == 'draw minimum ROI':
            self.ROI_logging['minimum'][self.name[-1]] = pos
        elif self.detect_size.currentText() == 'draw maximum ROI':
            self.ROI_logging['maximum'][self.name[-1]] = pos
        if self.Person_ROI.isChecked():
            self.ROI_logging['person'][self.name[-1]] = pos
        if self.PPE_ROI.isChecked():
            self.ROI_logging['PPE'][self.name[-1]] = pos
        if self.Falldown_ROI.isChecked():
            self.ROI_logging['fall down'][self.name[-1]] = pos
        # json file save
        if not os.path.exists(self.save_file):
            os.makedirs(self.save_file)
        with open(self.save_file+'logging.json', 'w') as fp:
            json.dump(self.ROI_logging, fp)
        self.points.clear()

    # ROI name record
    def Roiname_record(self):
        if self.comboBox.currentText() == 'draw Rect ROI':
            self.name.append(f'Rect_{len(self.name) + 1}')
        elif self.comboBox.currentText() == 'draw MultiRect ROI':
            self.name.append(f'MultiRect_{len(self.name) + 1}')

    def confirmROI(self):
        # font format
        myFont = QtGui.QFont("Microsoft JhengHei", 15, 1000 , italic=False)
        self.Roiname_record()
        # 矩形確認儲存
        if self.comboBox.currentText() == 'draw Rect ROI':
            x1 = self.lastPoint.x()
            x2 = self.endPoint.x()
            y1 = self.lastPoint.y()
            y2 = self.endPoint.y()
            self.ROI_view[self.name[-1]]=[self.scene.items()[1]]
            self.ROI_pos_logging([int(x1), int(y1), int(x2), int(y2)])
            # display text of roi name
            self.text = self.scene.addText(self.name[-1], myFont)
            self.text.setPos(x1, y1 - 30)
            self.ROI_view[self.name[-1]].append(self.scene.items()[-(len(self.name)+1)])
        # 多邊形確認儲存
        elif self.comboBox.currentText() == 'draw MultiRect ROI':
            # 多邊形ROI位址紀錄
            point = list()
            for i in self.points:
                point.append([int(i.x()), int(i.y())])
            # 將結尾與開頭座標連結
            draw = point.copy()
            draw.append(point[0])
            self.rect_draw_count += 1
            self.test(points=draw)
            # display set
            self.ROI_view[self.name[-1]]=self.tmp_multi
            # display text of roi name
            self.text = self.scene.addText(self.name[-1], myFont)
            self.text.setPos(int(point[0][0]), int(point[0][1]) - 45)
            self.ROI_view[self.name[-1]].append(self.scene.items()[-(len(self.name)+1)])
            # init logging for roi pos
            self.tmp_multi = list()
            del draw
            # json file logging
            self.ROI_pos_logging(point)
        # form
        self.ROI_form()

    # 右側欄位紀錄
    ## 可刪除指定ROI
    def ROI_form(self):
        a = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(a + 1)
        self.tableWidget.setItem(a, 0, QTableWidgetItem(self.name[-1]))
        # delete specific roi
        widget = QtWidgets.QWidget()
        hLayout = QtWidgets.QHBoxLayout()

        self.delete_specific = QPushButton('delete')
        self.delete_specific.setStyleSheet(self.qssStyle)

        self.delete_specific.clicked.connect(self.del_specific_roi)
        hLayout.addWidget(self.delete_specific)
        widget.setLayout(hLayout)
        self.tableWidget.setCellWidget(a, 1, widget)

    def del_specific_roi(self):
        button = self.sender()
        if button:
            # 確認當前位址 - 列
            row = self.tableWidget.indexAt(button.parent().pos()).row()
            # 取得該列roi名稱
            title = self.tableWidget.item(row, 0).text()
            # 刪除表單列資料
            self.tableWidget.removeRow(row)
            # 刪除該roi相關紀錄
            for i in self.ROI_logging:
                if title in list(i):
                    del i[title]
            # del display roi
            if 'Rect_' in title:
                for i in self.ROI_view[title]:
                    self.scene.removeItem(i)
                self.rect_draw_count -= 1
            else:
                for i in self.ROI_view[title]:
                    self.scene.removeItem(i)
            del self.ROI_view[title]
            self.name.remove(title)
            self.tmp_multi = list()
            with open(self.save_file + 'logging.json', 'w') as fp:
                json.dump(self.ROI_logging, fp)

    # 退出介面
    def set_quit(self):
        QCoreApplication.instance().quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    myWin = roiwidge()
    myWin.show()
    sys.exit(app.exec_())