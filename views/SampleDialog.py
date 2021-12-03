from PyQt5 import QtWidgets, QtCore


class SampleDialog(QtWidgets.QDialog):
    parent = None
    old_content_name = ''
    on_ok_execute = None

    def __init__(self, parent, old_content_name, execute_on_ok):
        super().__init__(parent=parent)

        self.parent = parent
        self.old_content_name = old_content_name
        self.on_ok_execute = execute_on_ok
        self.setup_ui()
        self.exec()

    def ok_clicked(self):
        result = self.on_ok_execute(self.old_content_name, self.main_field.text())

        if result:
            self.close()

    def setup_ui(self):
        self.setFixedSize(300, 70)
        self.move((self.parent.width() - self.width())//2, (self.parent.height() - self.height())//2)

        self.layout = QtWidgets.QHBoxLayout(self)

        self.main_field = QtWidgets.QLineEdit()
        self.ok_button = QtWidgets.QPushButton('OK')

        self.ok_button.clicked.connect(self.ok_clicked)

        self.layout.addWidget(self.main_field)
        self.layout.addWidget(self.ok_button)

