import json
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QSize, Qt, QPoint, QRect, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QPushButton,
    QMainWindow,
    QDialogButtonBox,
    QLineEdit,
    QWidget,
    QLabel,
    QHBoxLayout,
)
from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush
import sys


class TitleWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.is_valid = False
        layout = QVBoxLayout(self)
        
        title = QLabel('Name', objectName='name')
        layout.addWidget(title)
        
        self.nameEdit = QLineEdit()
        layout.addWidget(self.nameEdit)
        buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttonBox)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.show()
        self.loop = QtCore.QEventLoop()
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.loop.exec()
        
    def accept(self):
        self.is_valid = True
        self.title =  self.nameEdit.text()
        self.close()
        self.loop.quit()

    def reject(self):
        self.is_valid = False
        self.close()
        self.loop.quit()
        

class AnnotationBox(QWidget):
    def __init__(self, box: QRect) -> None:
        super().__init__()

        self.box = box
        self.setGeometry(self.box)

        self.title_window = TitleWindow()

        if self.title_window.is_valid:
            self.title = self.title_window.title
            self.is_valid = True
        else:
            self.title = "Invalid"
            self.is_valid = False

    def mousePressEvent(self, event) -> None:
        if self.box.contains(event.pos()):
            print(self.box)

    def __str__(self) -> str:
        return f"Name: {self.title} Coords: {self.box}"
    


class DrawableQLabel(QLabel):
    def __init__(self, *args, is_drawable=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.is_drawable = is_drawable
        self.begin = QPoint()
        self.end = QPoint()

        self.annotations = []

        self.show()

    def paintEvent(self, event):
        QLabel.paintEvent(self, event)

        qp = QPainter(self)
        br_drawing = QBrush(QColor(100, 10, 10, 40))
        br_drawn = QBrush(QColor(0, 255, 0, 90))
        qp.setBrush(br_drawing)
        qp.drawRect(QRect(self.begin, self.end))

        for box in self.annotations:
            qp.setBrush(br_drawn)
            qp.drawRect(box.box)

    def mousePressEvent(self, event):
        if self.is_drawable:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawable:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.is_drawable:
            self.end = event.pos()
            annot = AnnotationBox(QRect(self.begin, self.end))
            if annot.is_valid:
                self.annotations.append(annot)
            else:
                del annot
            self.begin = event.pos()
            self.update()

    def changeDrawable(self, checked):
        self.is_drawable = checked

    def showAnnotations(self):

        print(f"{len(self.annotations)} boxes")
        for ann in self.annotations:
            print(ann)

    def export(self):
        
        formatted_annotations = []
        for ann in self.annotations:
            formatted_annotations.append({
                "name": ann.title,
                "coords": [ann.box.x(), ann.box.y(), ann.box.width(), ann.box.height()]
            })

        out = {"annotations": formatted_annotations}
        return out
        
class MainWindow(QMainWindow):
    def __init__(self, filepath):
        super().__init__()

        self.setWindowTitle("Editor")

        widget = QWidget()

        layout = QHBoxLayout()

        btn_layout = QVBoxLayout()

        # self.btn_open = QPushButton("Open")
        # self.btn_open.clicked.connect(self.getfile)
        # btn_layout.addWidget(self.btn_open)

        self.btn_draw = QPushButton("Draw")
        self.btn_draw.setCheckable(True)
        self.btn_draw.clicked.connect(self.draw_rectangle)

        btn_layout.addWidget(self.btn_draw)

        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save)
        btn_layout.addWidget(self.btn_save)

        self.btn_show = QPushButton("Show")
        self.btn_show.clicked.connect(self.show_annots)
        btn_layout.addWidget(self.btn_show)

        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear)
        btn_layout.addWidget(self.btn_clear)

        layout.addLayout(btn_layout)

        self.le = DrawableQLabel()
        self.le.setPixmap(QPixmap(filepath))
        layout.addWidget(self.le)

        widget.setLayout(layout)

        self.setCentralWidget(widget)

    # def getfile(self):
    #     # fname = QFileDialog.getOpenFileName(self, 'Open file', "/prosight/data/imgs_lol/", "Image files (*.jpg *.jpeg)")
    #     fname = ["data/imgs_lol/sample_3480.jpeg"]
    #     self.le.setPixmap(QPixmap(fname[0]))

    def keyPressEvent(self, event):
        # q
        if event.key() == 81:
            self.close()

    def draw_rectangle(self, checked):
        
        self.le.changeDrawable(checked)
        
    def clear(self):
        
        print("Reset annotations")
        self.le.annotations = []
        self.le.update()
    
    def save(self):
        
        with open("test.json", "w") as f:
            json.dump(self.le.export(), f)
    
    def show_annots(self):
        self.le.showAnnotations()


app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow(sys.argv[1])
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()
