from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QComboBox, QVBoxLayout


NOTE_VALUES = {"A" : 0, "A#" : 1, "B" : 2, "C" : 3, "C#" : 4, "D" : 5,
               "D#" : 6, "E" : 7, "F" : 8, "F#" : 9,"G" : 10, "G#" : 11
               }
INTERVALS = {"Major" : [2, 4, 5, 7, 9, 11],
             "Minor" : [2, 3, 5, 7, 8, 10],
             "Harmonic Minor" : [2, 3, 5, 7, 8, 11],
             "Melodic Minor" : [2, 3, 5, 7, 9, 11]
             }
TUNINGS = {"Standard": ["E", "A", "D", "G", "B", "E"],
           "Drop D": ["D", "A", "D", "G", "B", "E"]
           }  


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arkie's Guitar App")
        self.setFixedWidth(800)
        self.setFixedHeight(500)
        # Add Widgets
        self.labels = [MyLabel(self, "Root Note: "), 
                       MyLabel(self, "Scale Type: "),
                       MyLabel(self, "Guitar Tuning: "),
                       MyLabel(self, "Stuff will go here")]
        self.buttons = [MyComboBox(self, NOTE_VALUES), 
                        MyComboBox(self, INTERVALS), 
                        MyComboBox(self, TUNINGS),
                        RefreshButton(self)]
        # Layout
        self.layout = QVBoxLayout()
        for k, (label, button) in enumerate(zip(self.labels, self.buttons)):
            self.layout.addWidget(label, 2*k)
            self.layout.addWidget(button, 2*k+1)
        self.setLayout(self.layout)
        # Show
        self.show()


class MyLabel(QLabel):
    def __init__(self, window, text):
        super().__init__(window)
        self.setText(text)
        

class MyComboBox(QComboBox):
    def __init__(self, window, dictionary):
        super().__init__(window)
        self.addItems(dictionary.keys())  
      

class RefreshButton(QPushButton):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.setText("Get Tab")
        self.clicked.connect(self.graph)
        
    def graph(self):
        root = self.window.buttons[0].currentText()
        name = self.window.buttons[1].currentText()
        tuning = self.window.buttons[2].currentText()
        scale = Scale(root, name=name)
        guitar = Guitar(tuning=tuning)
        guitar.get_valid_notes(scale)
        self.window.labels[3].setText(guitar.chart)


class Scale:
    def __repr__(self):
        return str(self.notes)
    
    def __init__(self, root, name="Major"):
        self.root = root
        self.name = name
        self.get_scale_notes()
        
    def get_scale_notes(self):
        notes = [NOTE_VALUES[self.root]]
        for interval in INTERVALS[self.name]:
            note = (notes[0] + interval) % 12
            notes.append(note)
        self.notes = notes


class Guitar:
    def __repr__(self):
        return str(self.strings)
    
    def __init__(self, tuning="Standard", frets=24):
        self.tuning = tuning
        self.frets = frets
        self.get_strings()
        self.get_fretboard_values()
        
    def get_strings(self):
        strings = []
        notes = TUNINGS[self.tuning]
        for note in notes:
            strings.append(NOTE_VALUES[note])
        self.strings =  strings

    def get_fretboard_values(self):
        fretboard = []
        for i, root in enumerate(self.strings):
            string = []
            for fret in range(self.frets + 1):
                note = (root + fret) % 12
                string.append(note)
            fretboard.append(string)
        self.fretboard = fretboard
        
    def get_valid_notes(self, scale):
        notes = scale.notes
        chart = ""
        for s in reversed(range(len(self.strings))):
            string = ""
            for fret in range(self.frets + 1):
                if self.fretboard[s][fret] in notes:
                    string += "-" + str(fret) + "-|"
                else:
                    if fret >=10:
                        string += "----|"
                    else:
                        string += "---|"
            string += "\n"
            chart += string
        self.chart = chart
        print(chart)


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(True)
    result = MainWindow()
    app.exec_()
