import sys, os
import keyboard
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt, QPointF, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QPainter, QImage, QPolygonF, QTransform, QCursor


x_move = 1600
y_move = 850

keyboard_zones = {
    "1": "1", "q": "1", "a": "1", "z": "1",
    "2": "2", "3": "2", "w": "2", "e": "2", "s": "2", "d": "2", "x": "2", "c": "2",
    "4": "3", "5": "3", "r": "3", "t": "3", "f": "3", "g": "3", "v": "3", "b": "3",
    "6": "4", "7": "4", "y": "4", "u": "4", "h": "4", "j": "4", "n": "4", "m": "4",
    "8": "5", "9": "5", "i": "5", "o": "5", "k": "5", "l": "5",
    "0": "6", "p": "6",
}


def get_asset_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)

def change_image(self, image_path):
    new_pixmap = QtGui.QPixmap(image_path)
    if not new_pixmap.isNull():
        new_pixmap = new_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(new_pixmap)
        self.label.resize(new_pixmap.size())


class CharacterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.WindowTransparentForInput|
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        pixmap = QtGui.QPixmap(get_asset_path("assets/right_paw_up.png"))
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(300, 300)
            pixmap.fill(Qt.transparent)        
        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.size())
        self.resize(pixmap.size())

        screen = QtWidgets.QApplication.desktop().availableGeometry()
        self.move(x_move, y_move)
    
    def set_image(self, image_path):
        new_pixmap = QtGui.QPixmap(image_path)
        
        if not new_pixmap.isNull():
            self.pixmap = new_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            self.label.setPixmap(self.pixmap)

class PawWindow(QMainWindow):
    def __init__(self, character_pos):
        super().__init__()
        self.character_pos = character_pos

        self.mousepos_x = 200
        self.mousepos_y = 200

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.WindowTransparentForInput|
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.screen_geo = QtWidgets.QApplication.desktop().geometry()
        self.setGeometry(self.screen_geo)

        self.img = QImage(get_asset_path("assets/paw_left_rotated.png"))
        if self.img.isNull():
            self.img = QImage(100, 100, QImage.Format_ARGB32)
            self.img.fill(QtGui.QColor(200, 100, 50))

        self.anchor_left = QPointF(self.character_pos.x() + 79, self.character_pos.y() + 60)
        self.anchor_right = QPointF(self.character_pos.x() + 119, self.character_pos.y() + 80)

        self.p3 = QPointF(0, 0)
        self.p4 = QPointF(0, 0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_mouse_pos)
        self.timer.start(16)

    def update_mouse_pos(self):
        global_pos = QCursor.pos()
        
        local_pos = self.mapFromGlobal(global_pos)
        
        paw_width = 30

        starting_x = 82 + x_move
        starting_y = 110 + y_move

        self.mousepos_x = starting_x - (local_pos.x()/50)
        self.mousepos_y = starting_y - (local_pos.y()/41)
        
        self.p3 = QPointF(self.mousepos_x - paw_width, self.mousepos_y-10)
        self.p4 = QPointF(self.mousepos_x + paw_width, self.mousepos_y+10)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        w, h = float(self.img.width()), float(self.img.height())

        src_poly = QPolygonF([
            QPointF(0, 0), QPointF(w, 0), QPointF(w, h), QPointF(0, h)
        ])
        
        dest_poly = QPolygonF([
            self.anchor_left,
            self.anchor_right,
            self.p4,
            self.p3
        ])
        

        transform = QTransform()
        
        if QTransform.quadToQuad(src_poly, dest_poly, transform):
            painter.setTransform(transform)
            painter.drawImage(0, 0, self.img)
            painter.resetTransform()


class MouseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
                Qt.FramelessWindowHint |
                Qt.WindowStaysOnTopHint |
                Qt.WindowTransparentForInput|
                Qt.Tool
            )
        self.setAttribute(Qt.WA_TranslucentBackground)

        pixmap = QtGui.QPixmap(get_asset_path("assets/mouse.png"))
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(300, 300)
            pixmap.fill(Qt.transparent)
        
        pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.size())
        self.resize(pixmap.size())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_mouse_pos)
        self.timer.start(16)
    
    def update_mouse_pos(self):
        self.move(int(paw.mousepos_x)-20, int(paw.mousepos_y)-40)

class KeyboardWindow(QMainWindow):
    image_change_requested = pyqtSignal(str)
    def __init__(self, plane):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.WindowTransparentForInput|
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.pixmap = QtGui.QPixmap(get_asset_path("assets/keyboard.png"))
        if self.pixmap.isNull():
            self.pixmap = QtGui.QPixmap(200, 98)
            self.pixmap.fill(Qt.transparent)
        
        self.pixmap = self.pixmap.scaled(130, 63, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.size())
        self.resize(self.pixmap.size())

        screen = QtWidgets.QApplication.desktop().availableGeometry()
        self.move(plane.x()+110, plane.y()+90)

        self.image_change_requested.connect(self.set_image)

        self.idle_timer = QTimer(self)
        self.idle_timer.setInterval(700)
        self.idle_timer.setSingleShot(True)
        self.idle_timer.timeout.connect(self.report_idle)
    
    def handle_key_signal(self, key):
        self.idle_timer.start()
        
        if key in keyboard_zones:
            zone = keyboard_zones[key]
            self.set_image(second_paw.positions[zone][2])
            character.set_image(get_asset_path("assets/no_paws.png"))
            second_paw.show()
            second_paw.set_position(zone)
    
    def report_idle(self):
        self.set_image(get_asset_path("assets/keyboard.png"))
        character.set_image(get_asset_path("assets/right_paw_up.png"))
        second_paw.hide()
    
    def set_image(self, image_path):
        new_pixmap = QtGui.QPixmap(image_path)
        
        if not new_pixmap.isNull():
            self.pixmap = new_pixmap.scaled(130, 63, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            self.label.setPixmap(self.pixmap)

class SecondPawWindow(QMainWindow):
    def __init__(self, character_pos):
        super().__init__()
        self.character_pos = character_pos

        self.positions = {
            "1": [150 + x_move, 110 + y_move, get_asset_path("assets/keyboard_red.png")],
            "2": [164 + x_move, 110 + y_move, get_asset_path("assets/keyboard_yellow.png")],
            "3": [186 + x_move, 110 + y_move, get_asset_path("assets/keyboard_green.png")],
            "4": [204 + x_move, 115 + y_move, get_asset_path("assets/keyboard_cyan.png")],
            "5": [220 + x_move, 120 + y_move, get_asset_path("assets/keyboard_blue.png")],
            "6": [240 + x_move, 125 + y_move, get_asset_path("assets/keyboard_pink.png")]
        }

        self.picked_position = "1"

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.WindowTransparentForInput|
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.screen_geo = QtWidgets.QApplication.desktop().geometry()
        self.setGeometry(self.screen_geo)

        self.img = QImage(get_asset_path("assets/paw_right_rotated.png"))

        self.anchor_left = QPointF(self.character_pos.x() + 149, self.character_pos.y() + 80)
        self.anchor_right = QPointF(self.character_pos.x() + 209, self.character_pos.y() + 90)

        self.p3 = QPointF(0, 0)
        self.p4 = QPointF(0, 0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_mouse_pos)
        self.timer.start(16)
    
    def set_position(self, position):
        self.picked_position = position

    def update_mouse_pos(self):
        self.p3 = QPointF(self.positions[self.picked_position][0] - 30, self.positions[self.picked_position][1])
        self.p4 = QPointF(self.positions[self.picked_position][0] + 30, self.positions[self.picked_position][1]+10)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        w, h = float(self.img.width()), float(self.img.height())

        src_poly = QPolygonF([
            QPointF(0, 0), QPointF(w, 0), QPointF(w, h), QPointF(0, h)
        ])
        
        dest_poly = QPolygonF([
            self.anchor_left,
            self.anchor_right,
            self.p4,
            self.p3
        ])
        

        transform = QTransform()
        
        if QTransform.quadToQuad(src_poly, dest_poly, transform):
            painter.setTransform(transform)
            painter.drawImage(0, 0, self.img)
            painter.resetTransform()


class KeyboardListener(QThread):
    key_pressed = pyqtSignal(str)

    def run(self):
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name.lower()
                if len(key) == 1 and key.isalnum():
                    self.key_pressed.emit(key)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mouse = MouseWindow()
    mouse.show()

    character = CharacterWindow()
    character.show()

    cat_keyboard = KeyboardWindow(character.pos())

    listener = KeyboardListener()
    listener.key_pressed.connect(cat_keyboard.handle_key_signal)
    listener.start()

    cat_keyboard.show()

    paw = PawWindow(character.pos())
    paw.show()

    second_paw = SecondPawWindow(character.pos())
    

    keyboard.add_hotkey('end', lambda: app.quit())
    sys.exit(app.exec_())