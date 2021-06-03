from Music import Note, Scale
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class Guitar:
    tunings = {"E Standard": ["E2", "A2", "D3", "G3", "B3", "E4"],
               "Drop D": ["D2", "A2", "D3", "G3", "B3", "E4"],
               "Drop C": ["C2", "G2", "C3", "F3", "A3", "D4"]}  
    
    def __repr__(self):
        return str(self.strings)
    
    def __init__(self, tuning="E Standard", frets=22, scale=None):
        self.tuning = tuning
        self.frets = frets
        self.get_strings()
        self.get_fretboard_notes()
        if scale is None:
            scale = Scale(scale="Chromatic")
        self.scale = scale
        self.widget = FretboardTable(self)
        self.update()
        
    def update(self):
        self.get_strings()
        self.get_fretboard_notes()
        self.scale.update()
        self.widget.update_fretboard()
        
    def get_strings(self):
        strings = []
        notes = Guitar.tunings[self.tuning]
        for note in notes:
            strings.append(Note(Note.get_pitch(note)))
        self.strings =  strings

    def get_fretboard_notes(self):
        fretboard = []
        for root in self.strings:
            values = []
            for fret in range(self.frets + 1):
                value = root + fret
                values.append(value)
            fretboard.append(values)
        self.fretboard = fretboard
        
    def strum(self):
        for string in self.strings:
            string.play()
            
    def play(self, string, fret):
        self.fretboard[string-1][fret].play()


class FretboardTable(QTableWidget):
    colors = ("blue", "green", "orange", 
              "red", "purple", "magenta", 
              "cyan", "black", "black", "black", "black", "black")
    
    def __init__(self, instrument, mode="Notes"):
        super().__init__()
        self.instrument = instrument
        self.mode = mode
        self.scale = self.instrument.scale
        self.cellPressed.connect(self.play)
        
    def play(self, row, col):
        text = self.item(row, col).text()
        if text != "-":
            strings = len(self.instrument.strings)
            string = strings - row
            fret = col
            self.instrument.play(string, fret)
        
    def update_fretboard(self):
        self.setRowCount(len(self.instrument.strings))
        self.setColumnCount(self.instrument.frets + 1)
        strings = [string.scale_name for string in self.instrument.strings]
        self.setVerticalHeaderLabels(reversed(strings))
        labels = [str(i) for i in range(self.instrument.frets + 2)]
        self.setHorizontalHeaderLabels(labels)
        self.resizeColumnsToContents()
        self.fill_fretboard(self.scale)
                
    def fill_fretboard(self, scale):
        strings = len(self.instrument.strings)
        for col in range(self.columnCount()):
            for row in range(self.rowCount()):
                string = strings - row - 1
                note = self.instrument.fretboard[row][col]
                if note in scale:
                    index = scale.index(note)
                    color = FretboardTable.colors[index]
                    if self.mode == "Notes":
                        fret = scale.names[index].scale_name
                    else:
                        fret = str(col)
                else:
                    fret = "-"
                    color = "black"
                item = MyTableWidgetItem(fret, color)
                self.setItem(string, col, item)    


class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, text, color):
        super().__init__(text)
        self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.setForeground(QColor(color)) 


def play_toxicity():
    guitar = Guitar(tuning="Drop C")
    # First Part
    for _ in range(4):
        guitar.play(2, 5)
        guitar.play(3, 7)
    for _ in range(4):
        guitar.play(2, 8)
        guitar.play(3, 10)
    for _ in range(3):
        guitar.play(2, 5)
        guitar.play(3, 7)
    guitar.play(3, 8)
    guitar.play(2, 5)
    guitar.play(3, 8)
    guitar.play(3, 7)
    guitar.play(2, 5)
    guitar.play(3, 7)
    # Second Part
    guitar.play(2, 8)
    guitar.play(3, 10)
    guitar.play(2, 8)
    guitar.play(3, 10)
    guitar.play(3, 12)
    guitar.play(2, 8)
    guitar.play(3, 12)
    guitar.play(3, 10)
    guitar.play(2, 8)
    guitar.play(3, 10)
    guitar.play(3, 8)
    guitar.play(2, 8)
    guitar.play(3, 8)
    # Third Part
    guitar.play(1, 0)
    return guitar


def test_guitar():
    guitar = Guitar(tuning="Drop D", frets=12)
    guitar.strum()
    return guitar


if __name__ == "__main__":
    guitar = test_guitar()
    #guitar = play_toxicity()
