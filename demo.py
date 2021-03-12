#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QSizePolicy

import cv2
import numpy as np
import sys
import time
import os
import random

import checkAlign
from connectPLC import PLC
from detectYesNo import Detect


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Thread(QThread):
    progress = pyqtSignal()

    def run(self):
        while True:
            self.progress.emit()
            time.sleep(0.1)

class Query(QThread):
    progress = pyqtSignal()

    def run(self):
        while True:
            self.progress.emit()
            time.sleep(0.5)

class Camera(QThread):
    setup = pyqtSignal()

    def run(self):
        self.setup.emit()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        # QT Config
        self.title = "UET-CAM"
        self.icon = QIcon(resource_path('data/icon/uet.png'))

        # Declare Check Variable
        self.total = 0
        self.number_tested = 0
        self.number_success = 0
        self.number_error1 = 0
        self.number_error2 = 0
        self.number_error3 = 0
        self.count = 0

        self.cap_detect = any
        self.cap_check = any
        self.get_cap_detect = False
        self.get_cap_check = False

        self.Controller = PLC()
        self.command = "Idle"
        self.demo_count = 0
        self.report_one_time = True

        # Run QT
        self.initUI()
    
    def initUI(self):

        # Config Main Window
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet("background-color: rgb(171, 171, 171);")
        
        # Show UET LOGO
        self.uet_logo = QLabel(self)
        self.uet_pixmap = QPixmap(resource_path('data/icon/uet.png')).scaled(111,111,Qt.KeepAspectRatio)
        self.uet_logo.setPixmap(self.uet_pixmap)
        self.uet_logo.setGeometry(100, 10, 111, 111)

        # Show Title
        self.title_label = QLabel("HỆ THỐNG KIỂM TRA LINH KIỆN (UET-CAM)", self)
        self.title_label.setGeometry(341, 17, 1300, 95)
        font_title = QFont('', 36, QFont.Bold)
        self.title_label.setFont(font_title)
        self.title_label.setStyleSheet("color: rgb(255, 255, 255);")

        # Show Current Time
        self.time_label = QLabel(self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setGeometry(1500, 20, 430, 95)
        font_timer = QFont('', 40, QFont.Bold)
        self.time_label.setFont(font_timer)
        timer = QTimer(self)
        timer.timeout.connect(self.updateTimer)
        timer.start(1000)
        self.time_label.setStyleSheet("color: rgb(255, 255, 255);")

        # Show Detect Camera
        self.cam1_name = QLabel("DETECT CAMERA", self)
        self.cam1_name.setGeometry(55, 127, 728, 60)
        self.cam1_name.setAlignment(Qt.AlignCenter)
        self.cam1_name.setStyleSheet("background-color: rgb(50, 130, 184);"
                                    "color: rgb(255, 255, 255);"
                                    "font: bold 14pt;")
        self.cam1 = QLabel(self)
        self.cam1.setGeometry(55, 185, 728, 410)
        self.cam1.setStyleSheet("border-color: rgb(50, 130, 184);"
                                "border-width: 5px;"
                                "border-style: inset;")

        # Show Check Camera
        self.cam2_name = QLabel("CHECK CAMERA", self)
        self.cam2_name.setGeometry(55, 606, 728, 60)
        self.cam2_name.setAlignment(Qt.AlignCenter)
        self.cam2_name.setStyleSheet("background-color: rgb(50, 130, 184);"
                                    "color: rgb(255, 255, 255);"
                                    "font: bold 14pt;")
        self.cam2 = QLabel(self)
        self.cam2.setGeometry(55, 666, 728, 410)
        self.cam2.setStyleSheet("border-color: rgb(50, 130, 184);"
                                "border-width: 5px;"
                                "border-style: inset;")

        # Set Font
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        
        # Trays Information
        self.tray = []
        for i in range(2):
            tray_name = QLabel("TRAY {}".format(i+1), self)
            tray_name.setGeometry(980+400*i-5, 127, 372, 60)
            tray_name.setAlignment(Qt.AlignCenter)
            tray_name.setStyleSheet("background-color:rgb(50, 130, 184);"
                                    "color: rgb(255, 255, 255);"
                                    "font: bold 14pt;")
            table_margin = QLabel(self)
            table_margin.setGeometry(980+400*i-5, 181, 372, 417)
            table_margin.setStyleSheet("border-color: rgb(50, 130, 184);"
                                        "border-width: 5px;"
                                        "border-style: inset;")
            table = QTableWidget(7,3,self)
            table.setGeometry(980+400*i,186,362,408)
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            for j in range(3):
                table.setColumnWidth(j,120)
            for j in range(7):
                table.setRowHeight(j,58)
            table.setFont(self.font)
            table.setStyleSheet("color: rgb(255, 255, 255);")
            self.tray.append(table)

        # Table Info Area        
        self.s_name = QLabel("INFORMATION", self)
        self.s_name.setGeometry(830, 606, 734, 60)
        self.s_name.setAlignment(Qt.AlignCenter)
        self.s_name.setStyleSheet("background-color:rgb(50, 130, 184);"
                                    "color: rgb(255, 255, 255);"
                                    "font: bold 14pt;")

        self.statistic_table = QTableWidget(5,3,self)
        self.statistic_table.setGeometry(830, 666, 734, 410)
        self.statistic_table.horizontalHeader().hide()
        self.statistic_table.verticalHeader().hide()
        self.statistic_table.setFont(self.font)
        self.statistic_table.setStyleSheet("color: rgb(255, 255, 255);"
                                            "text-align: center;"
                                            "border-width: 5px;"
                                            "border-style: inset;"
                                            "border-color: rgb(50, 130, 184);")
        for j in range(3):
            self.statistic_table.setColumnWidth(j,241)
        for j in range(5):
            self.statistic_table.setRowHeight(j,80)
        tested_item = QTableWidgetItem("TESTED")
        tested_item.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(0,0,tested_item)

        success_item = QTableWidgetItem("SUCCESS")
        success_item.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(1,0,success_item)

        error1_item = QTableWidgetItem("NEED RETEST")
        error1_item.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(2,0,error1_item)

        error2_item = QTableWidgetItem("CONNECTION ERROR")
        error2_item.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(3,0,error2_item)

        error3_item = QTableWidgetItem("FAILURE")
        error3_item.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(4,0,error3_item)

        # Note Table
        self.s_name = QLabel("REPORT", self)
        self.s_name.setGeometry(1590, 606, 300, 60)
        self.s_name.setAlignment(Qt.AlignCenter)
        self.s_name.setStyleSheet("background-color:rgb(50, 130, 184);"
                                    "color: rgb(255, 255, 255);"
                                    "font: bold 14pt;")
        self.textBox = QPlainTextEdit(self)
        # self.textBox.setGeometry(1590,666,300,410)
        self.textBox.move(1590, 666)
        self.textBox.resize(300, 410)
        self.textBox.setFont(self.font)
        
        # Exit Button
        self.exit_button = QPushButton(self)
        self.exit_icon = QIcon(resource_path('data/icon/close.jpg'))
        self.exit_button.setIcon(self.exit_icon)
        self.exit_button.setIconSize(QSize(50, 50))
        self.exit_button.setGeometry(1878, -8, 50, 50)
        self.exit_button.setHidden(0)
        self.exit_button.setStyleSheet("border: none")
        self.exit_button.clicked.connect(self.close)

        # Create Thread
        self.camera_thread = Camera()
        self.camera_thread.setup.connect(self.setup_camera)
        self.main_thread = Thread()
        self.main_thread.progress.connect(self.main_process)
        # self.plc_thread = Query()
        # self.main_thread.progress.connect(self.get_command)
        self.demo_thread = Query()
        self.demo_thread.progress.connect(self.demo)
        
        self.camera_thread.start()
        self.main_thread.start()
        # self.plc_thread.start()
        self.demo_thread.start()
    
    def update_detect_image(self, img):
        rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        # p = convertToQtFormat.scaled(570, 760, Qt.KeepAspectRatio)
        self.cam1.setPixmap(QPixmap.fromImage(convertToQtFormat))
    
    def update_check_image(self, img):
        rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        # p = convertToQtFormat.scaled(570, 760, Qt.KeepAspectRatio)
        self.cam2.setPixmap(QPixmap.fromImage(convertToQtFormat))
    
    def update_statistic(self, data):
        self.number_tested += 1
        if self.count == 42:
            self.count = 0
        
        while self.Controller.data[self.count] != 1:
            self.count += 1
            
        tested = QTableWidgetItem("{}".format(self.number_tested) + " / {}".format(self.total))
        tested.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(0,1,tested)
        ratio_tested = QTableWidgetItem("{} %".format(int(self.number_tested / self.total * 100)))
        ratio_tested.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(0,2,ratio_tested)
        
        tray_idx = self.count // 21
        row = 6 - self.count % 21 % 7
        col = self.count % 21 // 7
        if data == "1":
            self.number_success += 1
            self.tray[tray_idx].item(row,col).setBackground(QColor(67, 138, 94))
            self.textBox.appendPlainText("Linh Kiện Tray {}".format(tray_idx+1) + " Hàng {}".format(row+1) + " Cột {}".format(col+1) + " Hoạt Động Tốt!\n")
        elif data == "0":
            self.number_error3 += 1
            self.tray[tray_idx].item(row,col).setBackground(QColor(232, 80, 91))
            self.textBox.appendPlainText("Linh Kiện Tray {}".format(tray_idx+1) + " Hàng {}".format(row+1) + " Cột {}".format(col+1) + " Bị Hỏng!\n")
        elif data == "-1":
            self.number_error1 += 1
            self.tray[tray_idx].item(row,col).setBackground(QColor(255, 255, 51))
            self.textBox.appendPlainText("Linh Kiện Tray {}".format(tray_idx+1) + " Hàng {}".format(row+1) + " Cột {}".format(col+1) + " Gặp Lỗi Vị Trí Trên Jig. Đề Nghị Kiểm Tra!\n")
        elif data == "404":
            self.number_error2 += 1
            self.tray[tray_idx].item(row,col).setBackground(QColor(255, 128, 0))
            self.textBox.appendPlainText("Linh Kiện Tray {}".format(tray_idx+1) + " Hàng {}".format(row+1) + " Cột {}".format(col+1) + " Gặp Lỗi Kết Nối Với Bộ Test. Đề Nghị Kiểm Tra!\n")

        success = QTableWidgetItem("{}".format(self.number_success) + " / {}".format(self.number_tested))
        success.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(1,1,success)
        ratio_success = QTableWidgetItem("{} %".format(int(self.number_success / self.number_tested * 100)))
        ratio_success.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(1,2,ratio_success)

        error1 = QTableWidgetItem("{}".format(self.number_error1) + " / {}".format(self.number_tested))
        error1.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(2,1,error1)
        ratio_error1 = QTableWidgetItem("{} %".format(int(self.number_error1 / self.number_tested * 100)))
        ratio_error1.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(2,2,ratio_error1)

        error2 = QTableWidgetItem("{}".format(self.number_error2) + " / {}".format(self.number_tested))
        error2.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(3,1,error2)
        ratio_error2 = QTableWidgetItem("{} %".format(int(self.number_error2 / self.number_tested * 100)))
        ratio_error2.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(3,2,ratio_error2)

        error3 = QTableWidgetItem("{}".format(self.number_error3) + " / {}".format(self.number_tested))
        error3.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(4,1,error3)
        ratio_error3 = QTableWidgetItem("{} %".format(int(self.number_error3 / self.number_tested * 100)))
        ratio_error3.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(4,2,ratio_error3)
        
        self.Controller.data[self.count] = 0
        self.count += 1
    
    def init_statistic(self):
        tested = QTableWidgetItem("{}".format(0) + " / {}".format(self.total))
        tested.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(0,1,tested)
        ratio_tested = QTableWidgetItem("{} %".format(0))
        ratio_tested.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(0,2,ratio_tested)

        success = QTableWidgetItem("{}".format(0) + " / {}".format(0))
        success.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(1,1,success)
        ratio_success = QTableWidgetItem("{} %".format(0))
        ratio_success.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(1,2,ratio_success)

        error1 = QTableWidgetItem("{}".format(0) + " / {}".format(0))
        error1.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(2,1,error1)
        ratio_error1 = QTableWidgetItem("{} %".format(0))
        ratio_error1.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(2,2,ratio_error1)

        error2 = QTableWidgetItem("{}".format(0) + " / {}".format(0))
        error2.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(3,1,error2)
        ratio_error2 = QTableWidgetItem("{} %".format(0))
        ratio_error2.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(3,2,ratio_error2)

        error3 = QTableWidgetItem("{}".format(0) + " / {}".format(0))
        error3.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(4,1,error3)
        ratio_error3 = QTableWidgetItem("{} %".format(0))
        ratio_error3.setTextAlignment(Qt.AlignCenter)
        self.statistic_table.setItem(4,2,ratio_error3)

    def update_data(self, data):
        
        # Update Data to Table
        c = 0
        for k in range(2):
            for j in range(3):
                for i in range(6,-1,-1):
                    self.tray[k].setItem(i,j,QTableWidgetItem())
                    if(int(data[c])):
                        self.tray[k].item(i,j).setBackground(QColor(102, 102, 255))
                        self.total += 1
                    c += 1

        # Send Data to PLC
        self.Controller.data = data
        # self.Controller.sendData()
        self.Controller.command = "Grip"
        # self.Controller.sendCommand()
        
    def updateTimer(self):
        cr_time = QTime.currentTime()
        time = cr_time.toString('hh:mm AP')
        self.time_label.setText(time)

    def main_process(self):
        if self.command == "Idle":
            if self.get_cap_detect == True:
                self.total = 0
                self.number_tested = 0
                self.number_success = 0
                self.number_error1 = 0
                self.number_error2 = 0
                self.number_error3 = 0
                self.count = 0
                self.demo_count = 0
                self.report_one_time = True

                # Hiện Video khi chờ
                # ret, image = self.cap_detect.read()
                image = cv2.imread(resource_path('data/demo/Detect/origin.jpg'))
                image = cv2.resize(image, (717,450)) # Resize cho Giao diện
                self.update_detect_image(image)
                time.sleep(0.1)
        elif self.command == "Detect":
            if self.get_cap_detect == True:
                
                # Lấy dữ liệu từ camera
                # ret, image = self.cap_detect.read()
                image = cv2.imread(resource_path('data/demo/Detect/origin.jpg'))
                resize_img = cv2.resize(image, (717,450)) # Resize cho Giao diện
                detect = Detect()

                # Xử lý Ảnh
                detect.image = cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_AREA)
                detect.grabCut()

                # Detect YES/NO
                result = detect.check(detect.crop_tray_1)
                result = np.append(result, detect.check(detect.crop_tray_2))
                self.update_detect_image(resize_img) # Đưa ảnh lên giao diện

                # Gửi kết quả Detect YES/NO cho PLC và Table  
                self.update_data(result)
                self.init_statistic()
                self.command = "Wait"
            
        elif self.command == "Check":
            if self.get_cap_check == True:
                # ret, image = self.cap_check.read() # Lấy dữ liệu từ camera
                rand_list = os.listdir(resource_path('data/demo/Check'))
                file = random.choice(rand_list)
                image = cv2.imread(resource_path('data/demo/Check/' + file))
                resize_img = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                resize_img = cv2.resize(resize_img, (717,450)) # Resize cho Giao diện
                image = cv2.resize(image, (800, 800))
                checkAlign.crop_image(image)
                mean = checkAlign.calc_mean_all()
                check = checkAlign.check(mean)

                self.update_check_image(resize_img) # Đưa video lên giao diện
                if check:
                    self.Controller.command = "Grip-1"
                    # self.Controller.sendCommand()
                else:
                    self.Controller.command = "Grip-0"
                    # self.Controller.sendCommand()
                self.command = "Wait"

        elif self.command == "1":
            self.update_statistic(self.command)
            self.Controller.command = "Grip"
            # self.Controller.sendCommand()
            self.command = "Wait"
        elif self.command == "0":
            self.update_statistic(self.command)
            self.Controller.command = "Grip"
            # self.Controller.sendCommand()
            self.command = "Wait"
        elif self.command == "-1":
            self.update_statistic(self.command)
            self.Controller.command = "Grip"
            # self.Controller.sendCommand()
            self.command = "Wait"
        elif self.command == "404":
            self.update_statistic(self.command)
            self.Controller.command = "Grip"
            # self.Controller.sendCommand()
            self.command = "Wait"
        elif self.command == "Report":
            if self.report_one_time:
                self.report_one_time = False
                QMessageBox.about(self, "Kiểm Tra Hoàn Tất", "Đã Kiểm Tra " + str(self.total) + " linh kiện!\n" + "Còn " + str(self.number_error1) + " linh kiện cần kiểm tra lại!")
                self.command = "Idle"

    def setup_camera(self):
        # self.cap_detect = cv2.VideoCapture(0) # Khai báo USB Camera Detect Config
        self.get_cap_detect = True
        # self.cap_check = cv2.VideoCapture(0) # Khai báo USB Camera Check Config
        self.get_cap_check = True

    # def get_command(self):
    #     self.command = self.Controller.queryCommand()

    def demo(self):
        if self.command == "Wait":
            if self.demo_count < self.total:
                if self.Controller.command == "Grip-0":
                    self.command = "-1"
                elif self.Controller.command == "Grip-1":
                    rand_list = ['1', '0', '404', '1', '1']
                    self.command = random.choice(rand_list)
                elif self.Controller.command == "Grip":       
                    self.command = "Check"
                    self.demo_count += 1
            elif self.demo_count == self.total:
                if self.Controller.command == "Grip-0":
                    self.command = "-1"
                elif self.Controller.command == "Grip-1":
                    rand_list = ['1', '0', '404', '1', '1']
                    self.command = random.choice(rand_list)
                self.demo_count += 1
            else:
                self.command = "Report"
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.command = "Detect"
        if event.key() == Qt.Key_Escape:
            self.command = "Idle"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())