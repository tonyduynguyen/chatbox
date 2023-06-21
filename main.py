import GiaoDien as GiaoDien
from PyQt5 import QtCore
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QMovie, QIcon
import sys

import threading

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = GiaoDien.Ui_Dialog()
ui.setupUi(MainWindow)

# import tro_ly_ao
# obj = tro_ly_ao.trolyao()
# import virtual_assistant
# obj = virtual_assistant.virtual_assistant()
import virtual_assistant
obj = virtual_assistant.virtual_assistant(ui)

#python -m PyQt5.uic.pyuic -x untitled.ui -o GiaoDien.py

def giaodien():
    MainWindow.setStyleSheet("QMainWindow{background-color: white;}")

    MainWindow.setWindowIcon(QIcon("images/icons8-mute-unmute-50.png"));

    # set icon cho nút
    #ui.pushButton.setStyleSheet("QPushButton {qproperty-icon: url(C:/Users/Tin Ngo/Downloads/icons8-mute-unmute-50.png);}")

    ui.pushButton.setStyleSheet("QPushButton {border-image: url(images/icons8-mute-unmute-50.png); align-item: center;}")
    ui.pushButton.setHidden(False)  # ẩn button

    ui.label.setPixmap(QtGui.QPixmap("images/icons8-mute-unmute-50.png"))
    ui.label.setStyleSheet("QLabel {min-width : 150px; }")
    movie = QMovie("images/icons8-microphone.gif")
    #set size cho ảnh trong label
    movie.setScaledSize(QtCore.QSize(141, 131))
    ui.label.setMovie(movie)
    movie.start()
    ui.groupBox.setHidden(True)  # ẩn group box

def show_group():
    ui.groupBox.setHidden(False)
    ui.pushButton.setHidden(True)

def action():
    obj.main()

# để cho việc show giao diện và chạy code diễn ra đúng lúc
# chạy 2 luồng (show giao diện và trợ lý ảo) cùng 1 lúc
def multithread_start():
    t1 = threading.Thread(name='show_group', target=show_group)
    t2 = threading.Thread(name='action', target=action)
    t1.start()
    t2.start()

def hide_group():
    ui.groupBox.setHidden(True)
    ui.pushButton.setHidden(False)

def inaction():
    obj.exit()

def multithread_end():
    t = threading.Thread(name='inaction', target=inaction)
    d = threading.Thread(name='hide_group', target=hide_group)
    t.start()
    d.start()


def mainMenu():
    # show group
    ui.pushButton.clicked.connect(multithread_start)
    # hide group
    ui.pushButton_2.clicked.connect(multithread_end)
    MainWindow.show()


if __name__ == '__main__':
    giaodien()
    mainMenu()
    sys.exit(app.exec_())  # để cho cửa sổ không bị tắt liền khi mới chạy được











