import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt

WHITE = 0
RED = 1


class Shashki(QWidget):

    def __init__(self):
        super().__init__()
        self.header = 'Приветствуем!'
        # self.current, self.new_coords = None, None # координаты хода
        while True:
            self.board = Board()
            if self.board.current_player_color() == WHITE:
                self.header = self.header + ' Ход белых:'
            else:
                self.header = self.header + ' Ход красных:'

            self.initUI()

    def initUI(self):
        self.setGeometry(300, 100, 500, 610)
        self.setWindowTitle('Шашки')

        self.label = QLabel(self)
        self.label.setText("Введите координаты, чтобы сделать ход")
        self.label.move(50, 470)
        
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
            qp.drawEllipse(50 * self.new_coords[0] + 2,
                           50 * self.new_coords[1] + 2, 46, 46)

            self.current, self.new_coords = None, None
            self.color = opponent(self.color)


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [[Pawn(WHITE), None] * 4]
        self.field[1] = [[None, Pawn(WHITE)] * 4]
        self.field[2] = [[Pawn(WHITE), None] * 4]
        self.field[5] = [[[None, Pawn(RED)] * 4]]
        self.field[6] = [[Pawn(RED), None] * 4]
        self.field[7] = [[[None, Pawn(RED)] * 4]]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return Qt.transparent
        color = piece.get_color()
        c = Qt.white if color == WHITE else Qt.red
        return c


class Pawn:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def can_move(self, board, col_from, row_from, col_to, row_to):
        if abs(col_from - col_to) == 1:
            return True
        
        if abs(col_from - col_to) != abs(row_from - row_to) \
           or abs(col_from - col_to) > 2:
            return False

        return False

    
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
    if abs(col_from - col_to) != abs(row_from - row_to) \
       or abs(col_from - col_to) > 2:
        return False
    if abs(col_from - col_to) == 1:
        return True


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Shashki()
    sys.exit(app.exec_())
