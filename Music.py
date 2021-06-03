from musicalbeeps import Player


class Scale:
    scale_intervals = {"Major" : [2, 4, 5, 7, 9, 11],
                       "Minor" : [2, 3, 5, 7, 8, 10],
                       "Harmonic Minor" : [2, 3, 5, 7, 8, 11],
                       "Melodic Minor" : [2, 3, 5, 7, 9, 11],
                       "Chromatic" : range(1,12)}
    
    def __repr__(self):
        return str(self.root) + " " + self.scale + ": " + str(self.names)
    
    def __contains__(self, note):
        return note.note in self.notes
    
    def __init__(self, root="C", scale="Major"):
        self.root = Note(root, letter=root[0])
        self.scale = scale
        self.update()
        
    def update(self):
        self.intervals = Scale.scale_intervals[self.scale]
        names = [self.root]
        notes = [self.root.note]
        for interval in self.intervals:
            note = self.root + interval
            names.append(note)
            notes.append(note.note)
        self.names = names
        self.notes = notes
        self.rename()
        
    def rename(self):
        if len(self.intervals) <= 7:  # Rename #'s to b's
            letter = self.names[0].scale_name[0]
            for note in self.names:
                note.rename(letter)
                letter = Note.next_letter(letter)
                
    
    def index(self, note):
        if note in self:
            return self.notes.index(note.note)
        else:
            return None
        
    def play(self):
        for note in self.names:
            note.play()
        (self.root+12).play()


class Note:
    player = Player(0.1)
    modifiers = {"Natural": "", "Flat": "b", "Sharp": "#"}
    letter_values = {"C" : 0, "D" : 2, "E" : 4, 
                     "F" : 5, "G" : 7, "A" : 9, "B" : 11}
    
    @staticmethod
    def next_letter(letter):
        letters = list(Note.letter_values.keys())
        index = (letters.index(letter) + 1) % 7
        return letters[index]
    
    @staticmethod
    def get_pitch(note):
        octave = 4
        letter = note[0]
        pitch = Note.letter_values[letter]
        if len(note) > 1:
            symbols = note[1:]
            if symbols[0].isdigit():
                octave = int(symbols[0])
            pitch += symbols.count("#") - symbols.count("b")
        pitch += octave * 12
        return pitch
    
    def __repr__(self):
        return self.scale_name
    
    def __add__(self, other):
        return Note(self.pitch + other)
    
    def __init__(self, pitch, letter=None):
        if isinstance(pitch, str):
            pitch = Note.get_pitch(pitch)
        self.pitch = pitch
        self.note = pitch % 12
        self.octave = pitch // 12
        self.letter = letter
        self.play_name = self.get_play_name()
        self.scale_name = self.get_scale_name()
        
    def get_play_name(self, octave=True):
        letters = list(Note.letter_values.keys())
        values = list(Note.letter_values.values())
        if self.note in values:
            index = values.index(self.note)
            letter = letters[index]
            symbol = ""
        else:
            index = values.index(self.note - 1)
            letter = letters[index]
            symbol = "#"
        if octave:
            return letter + str(self.octave) + symbol
        else:
            return letter + symbol
        
    def get_scale_name(self):
        if self.letter is None:
            return self.get_play_name(octave=False)
        else:
            diff = (self.note - Note.letter_values[self.letter]) % 12
            if diff == 0:
                symbol = ""
            elif diff < 6:
                symbol = "#" * abs(diff)
            else:
                symbol = "b" * abs(12 - diff)
            scale_name = self.letter + symbol
            return scale_name
        
    def rename(self, letter):
        note = Note(self.pitch, letter=letter)
        self.scale_name = note.scale_name

    def play(self, time=0.25):
        Note.player.play_note(self.play_name, time)


def test_notes():
    for i in range(40, 55):
        note = Note(i, letter="C")
        print(i, note, note.octave, note.scale_name)
        note.play() 
    return note


def test_scale():
    #scale = Scale("G#")
    scale = Scale("Ab")
    print(scale)
    scale.play()
    return scale


if __name__ == "__main__":
    #note = test_notes()
    scale = test_scale()
