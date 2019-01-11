from PyQt5.QtWidgets import (QAction, QApplication, QMenu, QStyle,
                             QSystemTrayIcon, QWidget, qApp)
from _thread import start_new_thread
import sys, os, time

APP_NAME = 'WakeHDDApp'
APP_PATH = ''
TXT_NAME = 'wakeHDD.log'
TXT_PATH = ''


class IconWidget(QWidget):
    tray_icon = None
    secs_passed = 0

    def __init__(self):
        QWidget.__init__(self)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(qApp.quit)
        stat_action = QAction("Stat", self)
        stat_action.triggered.connect(self.show_stat)

        tray_menu = QMenu()
        tray_menu.addAction(stat_action)
        tray_menu.addAction(quit_action)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(
            QStyle.SP_DriveHDIcon))
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.tray_icon.showMessage(APP_NAME, '%s running!' % APP_NAME,
                                   QSystemTrayIcon.Information, 1000)
        start_new_thread(self.write_txt, ())

    def show_stat(self):
        self.tray_icon.showMessage(
            APP_NAME, 'Written %s for %d secs.' % (TXT_PATH, self.secs_passed),
            QSystemTrayIcon.Information, 2000)

    def write_txt(self):
        while True:
            file = open(TXT_PATH, 'w')
            file.write('[%s] Written %s for %d secs.' %
                       (time.asctime(), TXT_PATH, self.secs_passed))
            file.close()
            time.sleep(1)
            self.secs_passed += 1


if __name__ == "__main__":

    APP_PATH = os.path.dirname(os.path.abspath(__file__))
    TXT_PATH = '%s\\%s' % (APP_PATH, TXT_NAME)

    app = QApplication(sys.argv)
    icon = IconWidget()
    sys.exit(app.exec())
