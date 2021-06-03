from Music import Note, Scale
from Instruments import Guitar
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QComboBox, QGridLayout


class MainWindow(QWidget):
    def __init__(self):
        # Initialize
        super().__init__()
        self.setWindowTitle("Arkie's Guitar App")
        self.setFixedWidth(1000)
        self.setFixedHeight(500)
        # Data
        self.instrument = Guitar()
        # Widgets
        self.root_label = MyLabel(self, "Root Note: ")
        self.modifier_label = MyLabel(self, "Natural/Flat/Sharp: ")
        self.scale_label = MyLabel(self, "Scale Type: ")
        self.tuning_label =  MyLabel(self, "Guitar Tuning: ")
        self.mode_label = MyLabel(self, "Note/Tab View: ")
        self.bottom_label = MyLabel(self, "")
        self.labels = [self.root_label, self.modifier_label,
                       self.scale_label, self.tuning_label, self.mode_label]
        self.root_combo = MyComboBox(self, Note.letter_values)
        self.modifier_combo = MyComboBox(self, Note.modifiers)
        self.scale_combo = MyComboBox(self, Scale.scale_intervals)
        self.tuning_combo = MyComboBox(self, Guitar.tunings)
        self.mode_combo = MyComboBox(self, {"Notes":[], "Tabs":[]})
        self.buttons = [self.root_combo, self.modifier_combo,
                        self.scale_combo, self.tuning_combo, self.mode_combo]
        # Layout
        self.layout = QGridLayout()
        for k, (label, button) in enumerate(zip(self.labels, self.buttons)):
            self.layout.addWidget(label, 2 * k, 0)
            self.layout.addWidget(button, 2 * k + 1, 0)
        self.layout.addWidget(self.instrument.widget, 2 * k + 2, 0)
        self.layout.addWidget(self.bottom_label, 2 * k + 3, 0)
        self.setLayout(self.layout)
        # Initialize
        self.update_all()
        # Show
        self.show()

    def update_all(self):
        # Get Values from Combo Boxes
        root = self.root_combo.currentText()
        modifier = Note.modifiers[self.modifier_combo.currentText()]
        scale = self.scale_combo.currentText()
        tuning = self.tuning_combo.currentText()
        mode = self.mode_combo.currentText()
        # Apply Inputs
        self.instrument.scale.root = Note(root + modifier)
        self.instrument.scale.scale = scale
        self.instrument.tuning = tuning
        self.instrument.widget.mode = mode
        self.instrument.update()
        # Change View
        self.bottom_label.setText(str(self.instrument.scale))


class MyLabel(QLabel):
    def __init__(self, window, text):
        super().__init__(window)
        self.setText(text)
        

class MyComboBox(QComboBox):
    def __init__(self, window, dictionary):
        super().__init__(window)
        self.addItems(dictionary.keys())
        self.currentIndexChanged.connect(window.update_all)


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(True)
    result = MainWindow()
    app.exec_()
