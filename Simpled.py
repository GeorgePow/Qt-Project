import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt


WHITE = 0
RED = 1


def opponent(color):
    if color == WHITE:
        return RED
    else:
        return WHITE
    

class Shashki(QWidget):

    def __init__(self):
        super().__init__()
        self.header = 'Приветствуем!'
        self.coords_from, self.coords_to = None, None # координаты хода
        # while True:
        self.board = Board()
        if self.board.currentPlayerColor() == WHITE:
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

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        
        self.drawField(event, qp)

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

        # draw red pawns
        for row in range(8):
            for col in range(8):
                color = self.board.cell(row, col)
                qp.setPen(color)
                qp.setBrush(color)
                qp.drawEllipse(50 * (col + 1) + 3, 50 * (row + 1) + 3, 44, 44)

    def mouseMoveEvent(self, event):
        if self.coords_from is None:
            self.coords_from = (event.y() // 50 - 1, event.x() // 50 - 1)
        else:
            self.coords_to = (event.y() // 50 - 1, event.x() // 50 - 1)
            if self.board.movePiece(*self.coords_from, *self.coords_to):
                self.header = 'Ход успешен!'
            else:
                self.header = 'Координаты некорректы! Попробуйте другой ход!'
            self.coords_from, self.coords_to = None, None
            
            self.initUI()

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
        self.field[0] = [Pawn(WHITE), None] * 4
        self.field[1] = [None, Pawn(WHITE)] * 4
        self.field[2] = [Pawn(WHITE), None] * 4
        self.field[5] = [None, Pawn(RED)] * 4
        self.field[6] = [Pawn(RED), None] * 4
        self.field[7] = [None, Pawn(RED)] * 4

    def currentPlayerColor(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return Qt.transparent
        color = piece.getColor()
        c = Qt.white if color == WHITE else Qt.red
        return c

    def getPiece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def movePiece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.getColor() != self.color:
            return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)
        return True


class Pawn:
    def __init__(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def canMove(self, board, col_from, row_from, col_to, row_to):
        if abs(col_from - col_to) != abs(row_from - row_to) \
           or abs(col_from - col_to) >= 2:
            return False

        if abs(col_from - col_to) == 1:
            return True
      
        return False

    
def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


def canMove(col_from, row_from, col_to, row_to):
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
