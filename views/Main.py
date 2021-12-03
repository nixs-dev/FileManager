# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import controllers.FileNavigator as FileManager
import views.SampleDialog as S_Dialog
from functools import partial
import controllers.Styler as Stylers


class Ui_MainWindow(object):
    this_window = None
    navigator = None
    itens = []
    selected_item = None

    def clear_content(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                layout.removeWidget(child.widget())
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_content(child.layout(), None)

        self.itens = []
        self.selected_item = None

    def change_path(self):
        new_path = self.pathBar.text()

        if self.navigator.go_to(new_path):
            self.load_content()
        else:
            self.pathBar.setText(self.navigator.current_directory)
            QtWidgets.QMessageBox.critical(self.this_window, 'Erro', 'Caminho inexistente')

    def make_item_selected(self, item, filename, event):
        if event.button() == QtCore.Qt.LeftButton:
            if item not in self.itens:
                return self.load_content()

            if self.selected_item is not None:
                self.selected_item.styler.content_gets_idle()

            self.selected_item = item
            self.selected_item.styler.content_select()
        else:
            self.open_content_menu(item, filename, event.pos())

    def go(self, name, content_type, event):
        full_path = self.navigator.get_full_path(name)

        if content_type == 'folder':
            if self.navigator.go(name):
                self.pathBar.setText(self.navigator.current_directory)
                self.load_content()
        else:
            self.navigator.open_file(full_path)

    def back(self, event):
        if self.navigator.back():
            self.pathBar.setText(self.navigator.current_directory)
            self.load_content()
        else:
            print('Algo deu errado')

    def open_content_menu(self, content, filename, mouse_pos):
        options = QtWidgets.QMenu(content)
        delete = options.addAction('Deletar')
        rename = options.addAction('Renomear')

        parent_position = content.mapToGlobal(QtCore.QPoint(0, 0))
        menu_position = parent_position + mouse_pos

        options.setStyleSheet('color: #000000; border: 1px solid #000000;')
        options.move(menu_position.x(), menu_position.y())

        delete.triggered.connect(partial(self.make_content_change, options, self.navigator.delete_content, filename))
        rename.triggered.connect(partial(self.make_content_change, options, self.navigator.rename_content, filename))

        options.show()

    def make_content_change(self, options_menu, method, filename):
        if method == self.navigator.delete_content:
            self.navigator.delete_content(filename)
        if method == self.navigator.rename_content:
            S_Dialog.SampleDialog(self.this_window, filename, method)

        options_menu.close()
        self.load_content()

    def load_content(self):
        max_per_row = 3
        x = 0
        y = 0

        self.clear_content(self.directoriesLayout)

        for c in self.navigator.show_content():
            self.content_frame = QtWidgets.QFrame()
            self.content_frame.styler = Stylers.ItemStyler(self.content_frame)
            self.content_frame.setFixedSize(QtCore.QSize(200, 100))
            self.content_frame.setStyleSheet(self.content_frame.styler.content_idle)
            self.content_frame.setObjectName("content_frame_{}_{}".format(x, y))
            self.content_frame.mouseDoubleClickEvent = partial(self.go, c['name'], c['type'])
            self.content_frame.mousePressEvent = partial(self.make_item_selected, self.content_frame, c['name'])
            self.content_frame.enterEvent = partial(self.content_frame.styler.content_mouse_enter)
            self.content_frame.leaveEvent = partial(self.content_frame.styler.content_mouse_leave)
            self.content_symbol = QtWidgets.QLabel(self.content_frame)
            self.content_symbol.setGeometry(QtCore.QRect(16, 12, 61, 71))
            self.content_symbol.setStyleSheet('border: None')
            self.content_symbol.setPixmap(c['icon'])
            self.content_symbol.setScaledContents(True)
            self.content_symbol.setObjectName("content_symbol")
            self.content_name = QtWidgets.QLabel(self.content_frame)
            self.content_name.setGeometry(QtCore.QRect(100, 10, 91, 20))
            self.content_name.setStyleSheet("color: rgb(0, 0, 0); border: None")
            self.content_name.setText(c['name'])
            self.content_name.setObjectName("content_name")
            self.directoriesLayout.addWidget(self.content_frame, x, y)
            self.itens.append(self.content_frame)

            x += 1

            if x > max_per_row:
                x = 0
                y += 1

    def setup_ui(self, MainWindow):
        self.this_window = MainWindow
        self.navigator = FileManager.FileNavigator()

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 601)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.backNavigator = QtWidgets.QLabel(self.centralwidget)
        self.backNavigator.setGeometry(QtCore.QRect(10, 30, 47, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.backNavigator = QtWidgets.QLabel(self.centralwidget)
        self.backNavigator.setGeometry(QtCore.QRect(10, 30, 47, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.backNavigator.setFont(font)
        self.backNavigator.setAlignment(QtCore.Qt.AlignCenter)
        self.backNavigator.setObjectName("backNavigator")

        self.pathBar = QtWidgets.QLineEdit(self.centralwidget)
        self.pathBar.setGeometry(QtCore.QRect(70, 30, 701, 31))
        self.pathBar.setObjectName("pathBar")
        self.pathBar.setStyleSheet("color: rgb(150, 150, 150); border: 1px solid rgb(0, 0, 0)")

        self.scrollableArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollableArea.setGeometry(QtCore.QRect(10, 89, 761, 481))
        self.scrollableArea.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.scrollableArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollableArea.setWidgetResizable(True)
        self.scrollableArea.setObjectName("scrollableArea")

        self.directoriesContentArea = QtWidgets.QWidget()
        self.directoriesContentArea.setGeometry(QtCore.QRect(0, 0, 759, 479))
        self.directoriesContentArea.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.directoriesContentArea.setObjectName("directoriesContentArea")

        self.directoriesLayout = QtWidgets.QGridLayout(self.directoriesContentArea)
        self.directoriesLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.directoriesLayout.setContentsMargins(10, 0, 50, 0)
        self.directoriesLayout.setObjectName("directoriesLayout")

        self.scrollableArea.setWidget(self.directoriesContentArea)
        MainWindow.setCentralWidget(self.centralwidget)

        self.pathBar.editingFinished.connect(partial(self.change_path))
        self.backNavigator.mousePressEvent = partial(self.back)
        self.load_content()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.backNavigator.setText(_translate("MainWindow", "<"))
        self.pathBar.setText(_translate("MainWindow", self.navigator.current_directory))