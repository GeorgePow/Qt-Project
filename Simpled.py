import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt

WHITE = 0
RED = 1


class Board(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.current, self.new_coords = None, None # координаты хода
        self.color = WHITE

        # Создаем координаты красных шашек
        self.red_pawns = []
        first_y = 0
        for x in range(1, 9):
            for y in range(1 + first_y, 4, 2):
                self.red_pawns.append((x, y))
            first_y = (first_y + 1) % 2
        
        # Создаем координаты белых шашек
        self.white_pawns = []
        first_y = 1
        for x in range(1, 9):
            for y in range(6 + first_y, 9, 2):
                self.white_pawns.append((x, y))
            first_y = (first_y + 1) % 2

        # Шашки текущего игрока
        self.actual_pawns = self.white_pawns

    def initUI(self):
        self.setGeometry(300, 200, 500, 610)
        self.setWindowTitle('Шашки')

        self.label = QLabel(self)
        self.label.setText("Введите координаты, чтобы сделать ход")
        self.label.move(50, 470)

        # Читаем col_from
        self.col_from_label = QLabel(self)
        self.col_from_label.setText("Из какой колонки делаем ход?")
        self.col_from_label.move(50, 490)
        self.col_from = QLineEdit(self)
        self.col_from.move(250, 490)
        
        # Читаем row_from
        self.row_from_label = QLabel(self)
        self.row_from_label.setText("Из какого ряда делаем ход?")
        self.row_from_label.move(50, 510)
        self.row_from = QLineEdit(self)
        self.row_from.move(250, 510)
        
        # Читаем col_to
        self.col_to_label = QLabel(self)
        self.col_to_label.setText("В какую колонку делаем ход?")
        self.col_to_label.move(50, 530)
        self.col_to = QLineEdit(self)
        self.col_to.move(250, 530)
        
        # Читаем row_to
        self.row_to_label = QLabel(self)
        self.row_to_label.setText("В какой ряд делаем ход?")
        self.row_to_label.move(50, 550)
        self.row_to = QLineEdit(self)
        self.row_to.move(250, 550)
        
        # Создаём кнопку, чтобы сделать ход
        self.btn = QPushButton('Сходить', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 570)
        self.btn.clicked.connect(self.run)
        
        self.show()

    def run(self):
        try:
            x, y = int(self.col_from.text()), int(self.row_from.text())
            x1, y1 = int(self.col_to.text()), int(self.row_to.text())
            if can_move(x, y, x1, y1):
                self.current = (x, y)
                self.new_coords = (x1, y1)
        except:
            pass

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        
        self.drawField(event, qp)
        self.drawPawn(qp)
        self.movePawn(qp)

        qp.end()

    def drawField(self, event, qp):
        qp.setPen(Qt.white)
        qp.setBrush(Qt.white)

        qp.drawRect(0, 0, 600, 600)

        qp.setPen(Qt.black)
        qp.setFont(QFont('Decorative', 20))
        
        for x in range(8):
            qp.drawText(67 + 50 * x, 40, str(x + 1))
            qp.drawText(20, 87 + 50 * x, str(x + 1))
        qp.drawRect(50, 50, 400, 400)

        qp.setBrush(Qt.black)
        
        first_y = 0
        for x in range(1, 9):
            for y in range(1 + first_y, 9, 2):
                qp.drawRect(50 * x, 50 * y, 50, 50)
            first_y = (first_y + 1) % 2

    def drawPawn(self, qp):
        # draw red pawns
        qp.setPen(Qt.black)
        qp.setBrush(Qt.red)
        for x, y in self.red_pawns:
            qp.drawEllipse(50 * x + 2, 50 * y + 2, 46, 46)

        # draw white pawns
        qp.setPen(Qt.black)
        qp.setBrush(Qt.white)
        for x, y in self.white_pawns:
            qp.drawEllipse(50 * x + 2, 50 * y + 2, 46, 46)

    def movePawn(self, qp):
        if self.current and self.new_coords:
            qp.setPen(Qt.black)
            qp.setBrush(Qt.black)
            qp.drawRect(50 * self.current[0], 50 * self.current[1], 50, 50)

            qp.setPen(Qt.black)
            if self.color == WHITE:
                color = Qt.white
            else:
                color = Qt.red
            qp.setBrush(color)
            qp.drawEllipse(50 * self.new_coords[0] + 2, 50 * self.new_coords[1] + 2, 46, 46)

            self.current, self.new_coords = None, None
            self.color = opponent(self.color)
            

def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 1 <= row <= 8 and 1 <= col <= 8


def can_move(col_from, row_from, col_to, row_to):
    if not correct_coords(row_from, col_from) or \
       not correct_coords(row_to, col_to):
        return False
    if row_from == row_to and col_from == col_to:
        return False
    if not((col_from + row_from) % 2 and (col_to + row_to) % 2):
        return False
    if (col_from, row_from) not in self.actual_pawns or \
       (col_to, row_to) in (self.white_pawns + self.red_pawns):
        return False
    if abs(col_from - col_to) != abs(row_from - row_to) or abs(col_from - col_to) > 2:
        return False
    if abs(col_from - col_to) == 1:
        return True


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Board()
    sys.exit(app.exec_())
