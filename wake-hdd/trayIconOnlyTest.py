from PyQt5.QtWidgets import (QAction, QApplication, QMenu, QStyle,
                             QSystemTrayIcon, QWidget, qApp)


class IconWidget(QWidget):
    tray_icon = None

    def __init__(self):
        QWidget.__init__(self)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(quit_action)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(
            QStyle.SP_ComputerIcon))
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        import os
        self.tray_icon.showMessage("Tray Program",
                                   os.path.dirname(os.path.abspath(__file__)),
                                   QSystemTrayIcon.Information, 2000)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    icon = IconWidget()
    sys.exit(app.exec())
