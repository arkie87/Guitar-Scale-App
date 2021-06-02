from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLabel, QComboBox, QGridLayout


class MainWindow(QWidget):
    def __init__(self):
        # Initialize
        super().__init__()
        self.setWindowTitle("Arkie's Guitar App")
        self.setFixedWidth(1000)
        self.setFixedHeight(500)
        # Data
        self.scale = Scale()
        self.guitar = Guitar()
        # Widgets
        self.root_label = MyLabel(self, "Root Note: ")
        self.scale_label = MyLabel(self, "Scale Type: ")
        self.tuning_label =  MyLabel(self, "Guitar Tuning: ")
        self.mode_label = MyLabel(self, "Note/Tab View: ")
        self.labels = [self.root_label, self.scale_label,
                       self.tuning_label, self.mode_label]
        self.root_combo = MyComboBox(self, Note.letters)
        self.scale_combo = MyComboBox(self, Scale.scales)
        self.tuning_combo = MyComboBox(self, Guitar.tunings)
        self.mode_combo = MyComboBox(self, {"Notes":[], "Tabs":[]})
        self.buttons = [self.root_combo, self.scale_combo, 
                        self.tuning_combo, self.mode_combo]
        self.fretboard = FretBoardTable(self)
        self.label = MyLabel(self, "")
        # Layout
        self.layout = QGridLayout()
        for k, (label, button) in enumerate(zip(self.labels, self.buttons)):
            self.layout.addWidget(label, 2*k, 0)
            self.layout.addWidget(button, 2*k+1, 0)
        self.layout.addWidget(self.fretboard, 2*k+2, 0)
        self.layout.addWidget(self.label, 2*k+3, 0)
        self.setLayout(self.layout)
        # Initialize
        self.update_all()
        # Show
        self.show()
        
    def update_all(self):
        root = self.root_combo.currentText()
        scale_type = self.scale_combo.currentText()
        self.scale.root = Note(root)
        self.scale.scale_type = scale_type
        self.scale.update()
        tuning = self.tuning_combo.currentText()
        self.guitar.tuning = tuning
        self.guitar.update()
        self.fretboard.update_fretboard()


class MyLabel(QLabel):
    def __init__(self, window, text):
        super().__init__(window)
        self.setText(text)
        

class MyComboBox(QComboBox):
    def __init__(self, window, dictionary):
        super().__init__(window)
        self.addItems(dictionary.keys())
        self.currentIndexChanged.connect(window.update_all)


class FretBoardTable(QTableWidget):
    COLORS = ["blue", "green", "orange", 
              "red", "purple", "magenta", "cyan"]
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
    def update_fretboard(self):
        scale = self.parent.scale
        guitar = self.parent.guitar
        self.setRowCount(len(guitar.strings))
        self.setColumnCount(guitar.frets)
        strings = [string.note for string in guitar.strings]
        self.setVerticalHeaderLabels(strings)
        labels = [str(i) for i in range(1, guitar.frets + 1)]
        self.setHorizontalHeaderLabels(labels)
        self.resizeColumnsToContents()
        self.fretboard = guitar.fretboard
        self.fill_fretboard(scale)
                
    def fill_fretboard(self, scale):
        mode = self.parent.buttons[-1].currentText()

        for col in range(self.columnCount()):
            for row in range(self.rowCount()):
                fret = self.fretboard[row][col+1]
                if fret in scale:
                    index = scale.index(fret)
                    color = FretBoardTable.COLORS[index]
                    if mode == "Notes":
                        note = scale.notes[index]
                    else:
                        note = col + 1
                else:
                    note = "-"
                    color = "black"
                item = QTableWidgetItem(str(note))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                item.setForeground(QColor(color))
                self.setItem(row, col, item)
            
        
class Guitar:
    tunings = {"E Standard": ["E", "A", "D", "G", "B", "E"],
               "Drop D": ["D", "A", "D", "G", "B", "E"]}  
    
    def __repr__(self):
        return str(self.strings)
    
    def __init__(self, tuning="E Standard", frets=24):
        self.tuning = tuning
        self.frets = frets
        self.update()
        
    def update(self):
        self.get_strings()
        self.get_fretboard_notes()
        
    def get_strings(self):
        strings = []
        notes = Guitar.tunings[self.tuning]
        for note in reversed(notes):
            strings.append(Note(note))
        self.strings =  strings

    def get_fretboard_notes(self):
        fretboard = []
        for i, root in enumerate(self.strings):
            values = []
            for fret in range(self.frets + 1):
                value = root + fret
                values.append(value)
            fretboard.append(values)
        self.fretboard = fretboard


class Scale:
    scales = {"Major" : [2, 4, 5, 7, 9, 11],
              "Minor" : [2, 3, 5, 7, 8, 10],
              "Harmonic Minor" : [2, 3, 5, 7, 8, 11],
              "Melodic Minor" : [2, 3, 5, 7, 9, 11]}
    
    def __repr__(self):
        return str(self.notes)
    
    def __contains__(self, value):
        return value in self.values
    
    def __init__(self, root="C", scale_type="Major"):
        self.root = Note(root)
        self.scale_type = scale_type
    
    def index(self, value):
        return self.values.index(value)
        
    def update(self):
        letters = list(Note.letters.keys())
        offset = letters.index(self.root.note[0]) + 1
        notes = [self.root]
        values = [self.root.value]
        for i, interval in enumerate(Scale.scales[self.scale_type]):
            letter = letters[(i + offset) % 7]
            letter_value = Note.letters[letter]
            value = notes[0] + interval
            diff = value - letter_value
            if abs(diff) > 6:
                diff -= 12 
            if diff > 0:
                symbol = "#"
            elif diff < 0:
                symbol = "b"
            else:
                symbol = ""
            note = Note(letter + symbol)
            notes.append(note)
            values.append(value)
        self.notes = notes
        self.values = values


class Note:
    letters = {"A": 0, "B": 2, "C": 3, "D": 5, "E": 7, "F": 8, "G": 10}
    
    def __repr__(self):
        return self.note
    
    def __add__(self, other):
        return (self.value + other) % 12
    
    def __init__(self, note):
        self.note = note
        self.value = self.get_value()
        
    def get_value(self):
        value = Note.letters[self.note[0]]
        if len(self.note) == 2:
            symbol = self.note[1]
            if symbol == "#":
                value += len(self.note) - 1
            elif symbol == "b":
                value -= len(self.note) - 1
        return (value % 12)
            

if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(True)
    result = MainWindow()
    app.exec_()
