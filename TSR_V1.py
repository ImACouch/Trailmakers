#Made By AJ Studios

from time import sleep
import sys
import ast
from math import sqrt
from math import floor
import keyboard
import os
from pynput.keyboard import Controller
import csv
from PIL import Image

print("                ")
print("░█████╗░░░░░░██╗")
print("██╔══██╗░░░░░██║")
print("███████║░░░░░██║")
print("██╔══██║██╗░░██║")
print("██║░░██║╚█████╔╝")
print("╚═╝░░╚═╝░╚════╝░")
print("Made By. AJ studio's")
print("release version 1.0")
print("6/6/2026")
print("Contributors: AJ Studio's, CRITICALS")
print("")
print("--------------Trailmakers Sreen Writer---------------")
print("")
sleep(1)

#LOGER -------------------------------------------------------------------------------------------------------

class logger:
    def __init__(self, log_file):
        self.log_file = log_file

        if not os.path.exists(log_file):
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("log file created\n")
        else:
            os.remove(log_file)
            with open(log_file, 'w', encoding='utf-8') as f:                
                f.write("log file created\n")

    def log(self, message):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
            print(message)

#GAME WRITER -------------------------------------------------------------------------------------------------------

keyboardC = Controller()

class game_writer:
    def __init__(self):
        self.current_color_tenths = 0
        self.current_color_hundreths = 0
        self.color_negative = False
        self.full_color = False
        self.x = 1
        self.y = 1

        self.press_post_delay = 0.06
        
        controles = {
            #Posishon
            "x-right": ["1", 0.08],
            "x-left": ["2", 0.08],
            "y-up": ["3", 0.08],
            "y-down": ["4", 0.08],

            "x-reset": ["-", 0.08],
            "y-reset": ["=", 0.08],

            #color
            "color_invert": ["5", 0.08],

            "color_up_tenths": ["6", 0.08],
            "color_down_tenths": ["7", 0.08],

            "color_up_hundreds": ["8", 0.08],
            "color_down_hundreds": ["9", 0.08],

            "toggle_1": ["0", 0.08],

            #controle
            "write": [";", 0.14]
        }

        self.controles = controles

    def press_key(self, controle):
        key = self.controles[controle][0]
        keyboardC.press(key)
        sleep(self.controles[controle][1])
        keyboardC.release(key)
        sleep(self.press_post_delay)

    def real_color_to_compoents(self, color):
        hole_number = floor(color)
        tenths = floor((color - hole_number) * 10)
        hundreths = floor((color- hole_number - tenths/10) * 100)

        return hole_number, tenths, hundreths
    
    def get_real_preceived_color(self):
        color = 0
        if self.full_color and self.color_negative!= True:
            color = 1
            return color
        elif self.full_color and self.color_negative == True:
            color = -1
            return color

        color += self.current_color_tenths / 10
        color += self.current_color_hundreths / 100

        if self.color_negative:
            color *= -1

        return color
    
    def move(self, x, y):
        if x == 1:
            self.x = 1
            self.press_key("x-reset")
        if y == 1:
            self.y = 1
            self.press_key("y-reset")

        while self.x != x:
            if self.x < x:
                self.press_key("x-right")
                self.x += 1
            else:
                self.press_key("x-left")
                self.x -= 1

        while self.y != y:
            if self.y < y:
                self.press_key("y-up")
                self.y += 1
            else:
                self.press_key("y-down")
                self.y -= 1

    def change_color(self, color):
        hole_number, tenths, hundreths = self.real_color_to_compoents(abs(color))

        #change to negitve or positive flag
        if color < 0 and not self.color_negative:
            self.press_key("color_invert")
            self.color_negative = True
        elif color >= 0 and self.color_negative:
            self.press_key("color_invert")
            self.color_negative = False

        color = abs(color)

        #if hole number change it
        if hole_number == 1 and not self.full_color:
            self.press_key("toggle_1")
            self.full_color = True
        elif hole_number == 0 and self.full_color:
            self.press_key("toggle_1")
            self.full_color = False

        #change tenths
        while self.current_color_tenths != tenths:
            if self.current_color_tenths < tenths:
                self.press_key("color_up_tenths")
                self.current_color_tenths += 1
            else:
                self.press_key("color_down_tenths")
                self.current_color_tenths -= 1

        #change hundreths
        while self.current_color_hundreths != hundreths:
            if self.current_color_hundreths < hundreths:
                self.press_key("color_up_hundreds")
                self.current_color_hundreths += 1
            else:
                self.press_key("color_down_hundreds")
                self.current_color_hundreths -= 1

    def smart_reset(self):
        self.move(1, 1)
        self.change_color(0)

    def dumb_reset(self):
        for i in range(10):
            self.press_key("color_up_tenths")
            self.press_key("color_down_tenths")
            self.press_key("color_up_hundreds")
            self.press_key("color_down_hundreds")

        for i in range(32):
            self.press_key("x-right")
            self.press_key("y-down")

    def write_pixel(self, x, y, color):
        self.move(x, y)
        self.change_color(color)
        self.press_key("write")  

'''
GW.write_pixel(5, 5, 0.56)
sleep(1)
GW.write_pixel(3, 8, 1)
sleep(1)
GW.write_pixel(6, 2, -0.64)
sleep(1)
GW.write_pixel(6, 2, 0)
sleep(1)
GW.write_pixel(30, 1, -1)
sleep(1)
GW.write_pixel(15, 9, 1)
sleep(1)
GW.write_pixel(1, 32, 0.20)
sleep(1)
GW.write_pixel(1, 1, 0.05)
'''

#MAIN -------------------------------------------------------------------------------------------------------

GW = game_writer()
LG = logger("game_log.txt")

def write_image(GW, img, LG=False):
    for i in range(len(img)):
        for j in range(len(img[i])):
            if keyboard.is_pressed("Z") != True:
                if img[i][j] == -0.99: #account for negative values bug ):
                    GW.write_pixel(j+1, i+1, -0.98)
                else:
                    GW.write_pixel(j+1, i+1, img[i][j])
                if LG != False:
                    LG.log(f"wrote pixel at x: {j+1}, y: {i+1}, color: {img[i][j]}")
            else:
                print("pausing writeing process")
                print_help(GW)
                print("resuming writeing process")
                sleep(1)
                print("resuming in 3")
                sleep(1)
                print("resuming in 2")
                sleep(1)
                print("resuming in 1")
                sleep(1)

def print_help(GW):
    print("----------------------------------------------------\nInfo: ")
    print("In game writeing commands: ")
    print(f"    x-right: {GW.controles['x-right'][0]}")
    print(f"    x-left: {GW.controles['x-left'][0]}")
    print(f"    y-up: {GW.controles['y-up'][0]}")
    print(f"    y-down: {GW.controles['y-down'][0]}")
    print("")
    print(f"    x-reset: {GW.controles['x-reset'][0]}")
    print(f"    y-reset: {GW.controles['y-reset'][0]}")
    print("")
    print(f"    color_invert: {GW.controles['color_invert'][0]}")
    print(f"    color_up_tenths: {GW.controles['color_up_tenths'][0]}")
    print(f"    color_down_tenths: {GW.controles['color_down_tenths'][0]}")
    print(f"    color_up_hundreds: {GW.controles['color_up_hundreds'][0]}")
    print(f"    color_down_hundreds: {GW.controles['color_down_hundreds'][0]}")
    print(f"    color_toggle_1: {GW.controles['toggle_1'][0]}")
    print("")
    print(f"    write: {GW.controles['write'][0]}")

    print("\n")

    print("----------------------------------------------------\nHelp Menu:")
    print("1: resume writeing")
    print("2: Cancel/close proggram")
    print("3: Print current perceived data")
    print("")
    print("4: Reset position")
    print("5: change perceived values")

    Q = input("what do you want to do? (1-5): ")
    if Q == "1":
        return
    elif Q == "2":
        exit()
    elif Q == "3":
        print_current_perceived_data(GW)
    elif Q == "4":
        for i in range(3):
            print(f"resetting position in {3-i}")
            sleep(1)
        GW.smart_reset()
        print("position reset")
    elif Q == "5":
        change_perceived_values(GW)
        
    print_help(GW)

def print_current_perceived_data(GW):
    print("----------------------------------------------------\nvalues: ")
    print(f"    x: {GW.x}")
    print(f"    y: {GW.y}")
    print(f"    color tenths: {GW.current_color_tenths}")
    print(f"    color hundreths: {GW.current_color_hundreths}")
    print(f"    color negative: {GW.color_negative}")
    print(f"    color full: {GW.full_color}")
    print(f"    real color: {GW.get_real_preceived_color()}")

    input("Press Enter to go back to help menu...")

def change_perceived_values(GW):
    print("----------------------------------------------------\nvalues: ")
    print(f"1: x: {GW.x}")
    print(f"2: y: {GW.y}")
    print(f"3: color tenths: {GW.current_color_tenths}")
    print(f"4: color hundreths: {GW.current_color_hundreths}")
    print(f"5: color negative: {GW.color_negative}")
    print(f"6: color full: {GW.full_color}")
    print(f"7: real color: {GW.get_real_preceived_color()}")

    print("0: back to help menu")

    Q = input("which value do you want to change? (1-7): ")
    if Q == "1":
        GW.x = int(input("new x: "))
    elif Q == "2":
        GW.y = int(input("new y: "))
    elif Q == "3":
        GW.current_color_tenths = int(input("new color tenths: "))
    elif Q == "4":
        GW.current_color_hundreths = int(input("new color hundreths: "))
    elif Q == "5":
        GW.color_negative = bool(input("new color negative (True/False): "))
    elif Q == "6":
        GW.full_color = bool(input("new color full (True/False): "))
    elif Q == "7":
        color = float(input("new real color (-1.00 to 1.00): "))
        parts = GW.real_color_to_compoents(color)

        GW.current_color_tenths = parts[1]
        GW.current_color_hundreths = parts[2]
        GW.full_color = parts[0]
        
        if color < 0:
            GW.color_negative = True
        else:            
            GW.color_negative = False
    elif Q == "0":
        return
    else:
        print("invalid input")

    change_perceived_values(GW)

def main():
    print("loading image data")
    
    stand_alone = True

    #import list from converter
    if stand_alone!= True:
        path = ""
        for i in range(1, len(sys.argv)):
            path += sys.argv[i]
            path += " "
        path = path[:-1]

        with open(path, "r") as f:
            img = f.read()
            f.close()
    else:
        with open("signals.txt", "r") as f:
            img = f.read()
            f.close()

    img = ast.literal_eval(img)

    print("Loaded image with " + str(len(img)) + " pixels")

    size = floor(sqrt(len(img)))
    print("assumed width and height: " + str(size))

    def invert_neg(x):
        assert -1.0 <= x <= 0.0
        return -1.0 - x

    img2 = []
    for i in range(size):
        img2.append([])
        for j in range(size):
            if img[i*size+j][2] < 0:
                img2[i].append(round(invert_neg(img[i*size+j][2]),2))
            else:
                img2[i].append(round(img[i*size+j][2],2))

    print("accounted for negative values bug")

    Q = input("Reset Posishon? (Y/N): ")
    if Q == "Y":
        GW.smart_reset()

    print("Press Z at any time to pause the writeing process and open help menue")
    input("Press Enter to start writeing...")
    sleep(1)
    print("starting in 3")
    sleep(1)
    print("starting in 2")
    sleep(1)
    print("starting in 1")
    sleep(1)

    write_image(GW, img2, LG) 
    #print(img2)

#CONVERTER -------------------------------------------------------------------------------------------------------

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QSlider, QFileDialog, QHBoxLayout, QVBoxLayout, QTextEdit,
    QGroupBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QFont

def rgb_to_hsv(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    d = mx - mn
    v = mx
    s = 0 if mx == 0 else d / mx
    h = 0
    if d:
        if mx == r:   h = ((g-b)/d + (6 if g<b else 0)) / 6
        elif mx == g: h = ((b-r)/d + 2) / 6
        else:         h = ((r-g)/d + 4) / 6
    return h*360, s, v


def hsv_to_rgb(h, s, v):
    h = h % 360
    i = int(h/60)
    f = h/60 - i
    p = v*(1-s); q = v*(1-f*s); t = v*(1-(1-f)*s)
    vals = [(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)]
    r,g,b = vals[i%6]
    return int(r*255), int(g*255), int(b*255)


def pixel_to_signal(r, g, b, panel_sat, panel_bri, sat_thresh, bri_thresh):
    if r == 0 and g == 0 and b == 0:
        return 0.0, (0, 0, 0)

    h, s, v = rgb_to_hsv(r, g, b)


    channel_diff = max(r, g, b) - min(r, g, b)
    diff_thresh = sat_thresh * 255
    v = max(r, g, b) / 255
    is_grey = channel_diff < diff_thresh or (v > bri_thresh and channel_diff < diff_thresh * 2)

    if is_grey:
        abs_x = min(1.0, 1 - v/panel_bri) if panel_bri > 0 else 1.0
        sig = -max(0.0002, abs_x)
        grey = int((1 - abs(sig)) * panel_bri * 255)
        return sig, (grey, grey, grey)
    else:
        sig = max(0.001, h / 360)
        return sig, hsv_to_rgb(h, panel_sat, panel_bri)


def signal_to_map_color(sig):
    if sig == 0:   return (20, 20, 20)
    if sig < 0:
        gv = int((1 - abs(sig)) * 160 + 40)
        return (int(gv*0.4), int(gv*0.5), gv)
    return hsv_to_rgb(sig * 360, 1.0, 1.0)




class ConvertWorker(QThread):
    done = pyqtSignal(object, object, object, object, int, int)

    def __init__(self, img, max_w, panel_sat, panel_bri, sat_thresh, bri_thresh):
        super().__init__()
        self.img = img
        self.max_w = max_w
        self.panel_sat = panel_sat
        self.panel_bri = panel_bri
        self.sat_thresh = sat_thresh
        self.bri_thresh = bri_thresh

    def run(self):
        img = self.img.convert("RGB")
        ow, oh = img.size
        scale = min(self.max_w / ow, self.max_w / oh, 1.0)
        W, H = max(1, int(ow * scale)), max(1, int(oh * scale))

        small = img.resize((W, H), Image.NEAREST)
        px = small.load()

        orig_data   = bytearray(W * H * 3)
        render_data = bytearray(W * H * 3)
        sigmap_data = bytearray(W * H * 3)
        signals = []

        for y in range(H):
            row = []
            for x in range(W):
                r, g, b = px[x, y]
                sig, rgb = pixel_to_signal(r, g, b,
                    self.panel_sat, self.panel_bri,
                    self.sat_thresh, self.bri_thresh)
                row.append(sig)
                i = (y * W + x) * 3
                orig_data[i:i+3]   = [r, g, b]
                render_data[i:i+3] = list(rgb)
                sigmap_data[i:i+3] = list(signal_to_map_color(sig))
            signals.append(row)

        self.done.emit(orig_data, render_data, sigmap_data, signals, W, H)




class CanvasLabel(QLabel):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(200, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("background:#111; border:1px solid #333;")
        self.setText(f"<span style='color:#444;font-size:11px;'>{title}</span>")
        self._pixmap = None

    def set_rgb_data(self, data, W, H):
        img = QImage(bytes(data), W, H, W*3, QImage.Format_RGB888)
        self._pixmap = QPixmap.fromImage(img)
        self._update_scaled()

    def resizeEvent(self, e):
        self._update_scaled()

    def _update_scaled(self):
        if self._pixmap:
            scaled = self._pixmap.scaled(
                self.width(), self.height(),
                Qt.KeepAspectRatio, Qt.FastTransformation)
            self.setPixmap(scaled)




class SliderRow(QWidget):
    def __init__(self, label, mn, mx, default, decimals=2, scale=100):
        super().__init__()
        self._scale = scale
        self._dec = decimals
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)

        lbl = QLabel(label)
        lbl.setFixedWidth(160)
        lbl.setStyleSheet("color:#aaa; font-size:11px;")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(int(mn*scale), int(mx*scale))
        self.slider.setValue(int(default*scale))
        self.slider.setFixedWidth(180)

        self.val_lbl = QLabel(f"{default:.{decimals}f}")
        self.val_lbl.setFixedWidth(40)
        self.val_lbl.setStyleSheet("color:#9cf; font-size:11px;")

        self.slider.valueChanged.connect(
            lambda v: self.val_lbl.setText(f"{v/scale:.{decimals}f}"))

        lay.addWidget(lbl)
        lay.addWidget(self.slider)
        lay.addWidget(self.val_lbl)

    def value(self):
        return self.slider.value() / self._scale




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trailmakers RGB → Signal Converter")
        self.setMinimumSize(900, 640)
        self.setStyleSheet("""
            QMainWindow, QWidget { background:#1a1a1a; color:#ccc; }
            QPushButton {
                background:#2a2a2a; color:#ccc; border:1px solid #444;
                padding:4px 12px; font-size:11px;
            }
            QPushButton:hover { background:#3a3a3a; }
            QPushButton:disabled { color:#555; border-color:#333; }
            QGroupBox { border:1px solid #333; margin-top:8px; font-size:11px; color:#888; }
            QGroupBox::title { subcontrol-origin:margin; left:8px; }
            QTextEdit { background:#111; color:#9f9; border:1px solid #333; font-size:10px; }
            QScrollBar:vertical { background:#222; width:8px; }
            QScrollBar::handle:vertical { background:#444; }
        """)

        self.image = None
        self.signals = None
        self.W = self.H = 0
        self.worker = None
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(6)
        root.setContentsMargins(10,10,10,10)


        ctrl_box = QGroupBox("Settings")
        ctrl_lay = QVBoxLayout(ctrl_box)
        ctrl_lay.setSpacing(3)

        self.sat_s   = SliderRow("Panel Saturation",  0, 1,    1.0)
        self.bri_s   = SliderRow("Panel Brightness",  0, 1,    1.0)
        self.sthr_s  = SliderRow("Sat threshold",     0, 0.8,  0.25)
        self.vthr_s  = SliderRow("Brightness thresh", 0, 1,    0.85)
        self.scale_s = SliderRow("Max width (px)",   16, 256,  64, decimals=0, scale=1)
        self.scale_s.slider.setSingleStep(8)

        for w in [self.sat_s, self.bri_s, self.sthr_s, self.vthr_s, self.scale_s]:
            ctrl_lay.addWidget(w)


        btn_row = QHBoxLayout()
        self.btn_open    = QPushButton("Open Image")
        self.btn_convert = QPushButton("Convert")
        self.btn_csv     = QPushButton("Export CSV")
        self.btn_list    = QPushButton("Export List")
        self.btn_copy    = QPushButton("Copy List")
        self.btn_preview = QPushButton("Save Preview")

        self.btn_write = QPushButton("write to game")

        for b in [self.btn_convert, self.btn_csv, self.btn_list, self.btn_copy, self.btn_preview,self.btn_write]:
            b.setDisabled(True)

        for b in [self.btn_open, self.btn_convert, self.btn_csv,
                  self.btn_list, self.btn_copy, self.btn_preview,self.btn_write]:
            btn_row.addWidget(b)
        btn_row.addStretch()

        self.btn_open.clicked.connect(self.open_image)
        self.btn_convert.clicked.connect(self.convert)
        self.btn_csv.clicked.connect(self.export_csv)
        self.btn_list.clicked.connect(self.export_list)
        self.btn_copy.clicked.connect(self.copy_list)
        self.btn_preview.clicked.connect(self.save_preview)
        self.btn_write.clicked.connect(self.write_to_game)

        ctrl_lay.addLayout(btn_row)
        root.addWidget(ctrl_box)

   
        canvas_row = QHBoxLayout()
        self.c_orig   = CanvasLabel("Original")
        self.c_render = CanvasLabel("In-game preview")
        self.c_signal = CanvasLabel("Signal map")
        for c in [self.c_orig, self.c_render, self.c_signal]:
            canvas_row.addWidget(c)
        root.addLayout(canvas_row, stretch=3)

   
        out_box = QGroupBox("Signal list  [[x, y, value], ...]")
        out_lay = QVBoxLayout(out_box)
        self.list_out = QTextEdit()
        self.list_out.setReadOnly(True)
        self.list_out.setMaximumHeight(100)
        self.list_out.setPlaceholderText("Convert an image to see the signal list here...")
        out_lay.addWidget(self.list_out)
        root.addWidget(out_box, stretch=1)

 
        self.status = QLabel("Ready — open an image to begin")
        self.status.setStyleSheet("color:#666; font-size:10px;")
        root.addWidget(self.status)



    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.webp)")
        if not path:
            return
        self.image = Image.open(path)
        self.status.setText(f"Loaded: {self.image.width}x{self.image.height} — {os.path.basename(path)}")
        self.btn_convert.setEnabled(True)

        thumb = self.image.convert("RGB")
        thumb.thumbnail((400, 400))
        self.c_orig.set_rgb_data(bytearray(thumb.tobytes()), thumb.width, thumb.height)
        for c in [self.c_render, self.c_signal]:
            c._pixmap = None
            c.setText(f"<span style='color:#444;font-size:11px;'>{c.title}</span>")

    def convert(self):
        if not self.image:
            return
        self.btn_convert.setEnabled(False)
        self.status.setText("Converting...")
        self.worker = ConvertWorker(
            self.image, int(self.scale_s.value()),
            self.sat_s.value(), self.bri_s.value(),
            self.sthr_s.value(), self.vthr_s.value()
        )
        self.worker.done.connect(self._on_done)
        self.worker.start()

    def _on_done(self, orig, render, sigmap, signals, W, H):
        self.signals = signals
        self.W, self.H = W, H

        self.c_orig.set_rgb_data(orig, W, H)
        self.c_render.set_rgb_data(render, W, H)
        self.c_signal.set_rgb_data(sigmap, W, H)

        entries = [f"[{x},{y},{v:.5f}]"
                   for y, row in enumerate(signals)
                   for x, v in enumerate(row)]
        self.list_out.setPlainText("[" + ",\n".join(entries) + "]")

        for b in [self.btn_convert, self.btn_csv, self.btn_list, self.btn_copy, self.btn_preview,self.btn_write]:
            b.setEnabled(True)
        self.status.setText(f"Done: {W}x{H} — {W*H} signals")

    def copy_list(self):
        text = self.list_out.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.status.setText("Copied to clipboard")

    def export_csv(self):
        if not self.signals:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "signals.csv", "CSV (*.csv)")
        if not path:
            return
        with open(path, "w", newline="") as f:
            csv.writer(f).writerows(
                [[f"{v:.5f}" for v in row] for row in self.signals])
        self.status.setText(f"Saved: {path}")

    def export_list(self):
        if not self.signals:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save List", "signals.txt", "Text (*.txt)")
        if not path:
            return
        entries = [f"[{x},{y},{v:.5f}]"
                   for y, row in enumerate(self.signals)
                   for x, v in enumerate(row)]
        with open(path, "w") as f:
            f.write("[" + ",\n".join(entries) + "]")
        self.status.setText(f"Saved: {path}")

    def save_preview(self):
        if not self.signals:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Preview", "preview.png", "PNG (*.png)")
        if not path:
            return
        W, H = self.W, self.H
        img = Image.new("RGB", (W, H))
        pix = img.load()
        ps, pb = self.sat_s.value(), self.bri_s.value()
        for y, row in enumerate(self.signals):
            for x, sig in enumerate(row):
                if sig == 0:       pix[x,y] = (0,0,0)
                elif sig < 0:
                    g = int((1-abs(sig))*pb*255)
                    pix[x,y] = (g,g,g)
                else:              pix[x,y] = hsv_to_rgb(sig*360, ps, pb)
        img.save(path)
        self.status.setText(f"Saved: {path}")

    
    def write_to_game(self):
        print("write to game")

        path = os.getcwd() + "\\signals.txt"

        entries = [f"[{x},{y},{v:.5f}]"
                   for y, row in enumerate(self.signals)
                   for x, v in enumerate(row)]
        
        if os.path.exists(path):
            os.remove(path)

        with open(path, "w") as f:
            f.write("[" + ",\n".join(entries) + "]")
        self.status.setText(f"Saved: {path}")
        
        # close the window and quit the Qt event loop so control returns to
        # the code after `app.exec_()` in `__main__` (which will then run `main()`)
        self.close()
        QApplication.instance().quit()

        print("exited")

    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Consolas", 9))
    win = MainWindow()
    win.show()
    # Start the Qt event loop. When the GUI calls `QApplication.instance().quit()`
    # (for example from `write_to_game`), `app.exec_()` will return and
    # execution continues here. We then run `main()` which uses terminal I/O.
    app.exec_()

    # Qt window closed and loop stopped — run the terminal-based main()
    main()
    sys.exit(0)

