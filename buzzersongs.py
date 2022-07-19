import time
import simpleio
import notes

"""
    Based on the code found at https://github.com/robsoncouto/arduino-songs
    More songs are availabe there as well

    Example use:
        songs = BuzzerSongs(board.GP16)
        songs.play("starwars")
"""

class BuzzerSongs():
    bank = {
        "zeldaTempo": 88,
        "zeldaMelody": [
            # Based on the arrangement at https://www.flutetunes.com/tunes.php?id=169
            notes.NOTE_AS4,-2,  notes.NOTE_F4,8,  notes.NOTE_F4,8,  notes.NOTE_AS4,8, #1
            notes.NOTE_GS4,16,  notes.NOTE_FS4,16,  notes.NOTE_GS4,-2,
            notes.NOTE_AS4,-2,  notes.NOTE_FS4,8,  notes.NOTE_FS4,8,  notes.NOTE_AS4,8,
            notes.NOTE_A4,16,  notes.NOTE_G4,16,  notes.NOTE_A4,-2,
            notes.REST,1,

            notes.NOTE_AS4,4,  notes.NOTE_F4,-4,  notes.NOTE_AS4,8,  notes.NOTE_AS4,16,  notes.NOTE_C5,16, notes.NOTE_D5,16, notes.NOTE_DS5,16,#7
            notes.NOTE_F5,2,  notes.NOTE_F5,8,  notes.NOTE_F5,8,  notes.NOTE_F5,8,  notes.NOTE_FS5,16, notes.NOTE_GS5,16,
            notes.NOTE_AS5,-2,  notes.NOTE_AS5,8,  notes.NOTE_AS5,8,  notes.NOTE_GS5,8,  notes.NOTE_FS5,16,
            notes.NOTE_GS5,-8,  notes.NOTE_FS5,16,  notes.NOTE_F5,2,  notes.NOTE_F5,4,

            notes.NOTE_DS5,-8, notes.NOTE_F5,16, notes.NOTE_FS5,2, notes.NOTE_F5,8, notes.NOTE_DS5,8, #11
            notes.NOTE_CS5,-8, notes.NOTE_DS5,16, notes.NOTE_F5,2, notes.NOTE_DS5,8, notes.NOTE_CS5,8,
            notes.NOTE_C5,-8, notes.NOTE_D5,16, notes.NOTE_E5,2, notes.NOTE_G5,8,
            notes.NOTE_F5,16, notes.NOTE_F4,16, notes.NOTE_F4,16, notes.NOTE_F4,16,notes.NOTE_F4,16,notes.NOTE_F4,16,notes.NOTE_F4,16,notes.NOTE_F4,16,notes.NOTE_F4,8, notes.NOTE_F4,16,notes.NOTE_F4,8,

            notes.NOTE_AS4,4,  notes.NOTE_F4,-4,  notes.NOTE_AS4,8,  notes.NOTE_AS4,16,  notes.NOTE_C5,16, notes.NOTE_D5,16, notes.NOTE_DS5,16,#15
            notes.NOTE_F5,2,  notes.NOTE_F5,8,  notes.NOTE_F5,8,  notes.NOTE_F5,8,  notes.NOTE_FS5,16, notes.NOTE_GS5,16,
            notes.NOTE_AS5,-2, notes.NOTE_CS6,4,
            notes.NOTE_C6,4, notes.NOTE_A5,2, notes.NOTE_F5,4,
            notes.NOTE_FS5,-2, notes.NOTE_AS5,4,
            notes.NOTE_A5,4, notes.NOTE_F5,2, notes.NOTE_F5,4,

            notes.NOTE_FS5,-2, notes.NOTE_AS5,4,
            notes.NOTE_A5,4, notes.NOTE_F5,2, notes.NOTE_D5,4,
            notes.NOTE_DS5,-2, notes.NOTE_FS5,4,
            notes.NOTE_F5,4, notes.NOTE_CS5,2, notes.NOTE_AS4,4,
            notes.NOTE_C5,-8, notes.NOTE_D5,16, notes.NOTE_E5,2, notes.NOTE_G5,8,
            notes.NOTE_F5,16, notes.NOTE_F4,16, notes.NOTE_F4,16, notes.NOTE_F4,16,notes.NOTE_F4,16,notes.NOTE_F4,16,notes.NOTE_F4,16,notes.NOTE_F4,16,notes.NOTE_F4,8, notes.NOTE_F4,16,notes.NOTE_F4,8],
        "birthdayTempo": 88,
        "birthdayMelody": [
            # Based on the arrangement at https://musescore.com/user/8221/scores/26906
            notes.NOTE_C4,4, notes.NOTE_C4,8,
            notes.NOTE_D4,-4, notes.NOTE_C4,-4, notes.NOTE_F4,-4,
            notes.NOTE_E4,-2, notes.NOTE_C4,4, notes.NOTE_C4,8,
            notes.NOTE_D4,-4, notes.NOTE_C4,-4, notes.NOTE_G4,-4,
            notes.NOTE_F4,-2, notes.NOTE_C4,4, notes.NOTE_C4,8,

            notes.NOTE_C5,-4, notes.NOTE_A4,-4, notes.NOTE_F4,-4,
            notes.NOTE_E4,-4, notes.NOTE_D4,-4, notes.NOTE_AS4,4, notes.NOTE_AS4,8,
            notes.NOTE_A4,-4, notes.NOTE_F4,-4, notes.NOTE_G4,-4,
            notes.NOTE_F4,-2],
        "starwarsTempo": 120,
        "starwarsMelody": [
            # Score available at https://musescore.com/user/202909/scores/1141521
            # The tenor saxophone part was used
            notes.NOTE_A4,-4, notes.NOTE_A4,-4, notes.NOTE_A4,16, notes.NOTE_A4,16, notes.NOTE_A4,16, notes.NOTE_A4,16, notes.NOTE_F4,8, notes.REST,8,
            notes.NOTE_A4,-4, notes.NOTE_A4,-4, notes.NOTE_A4,16, notes.NOTE_A4,16, notes.NOTE_A4,16, notes.NOTE_A4,16, notes.NOTE_F4,8, notes.REST,8,
            notes.NOTE_A4,4, notes.NOTE_A4,4, notes.NOTE_A4,4, notes.NOTE_F4,-8, notes.NOTE_C5,16,

            notes.NOTE_A4,4, notes.NOTE_F4,-8, notes.NOTE_C5,16, notes.NOTE_A4,2, #4
            notes.NOTE_E5,4, notes.NOTE_E5,4, notes.NOTE_E5,4, notes.NOTE_F5,-8, notes.NOTE_C5,16,
            notes.NOTE_A4,4, notes.NOTE_F4,-8, notes.NOTE_C5,16, notes.NOTE_A4,2,
            
            notes.NOTE_A5,4, notes.NOTE_A4,-8, notes.NOTE_A4,16, notes.NOTE_A5,4, notes.NOTE_GS5,-8, notes.NOTE_G5,16, #7 
            notes.NOTE_DS5,16, notes.NOTE_D5,16, notes.NOTE_DS5,8, notes.REST,8, notes.NOTE_A4,8, notes.NOTE_DS5,4, notes.NOTE_D5,-8, notes.NOTE_CS5,16,

            notes.NOTE_C5,16, notes.NOTE_B4,16, notes.NOTE_C5,16, notes.REST,8, notes.NOTE_F4,8, notes.NOTE_GS4,4, notes.NOTE_F4,-8, notes.NOTE_A4,-16, #9
            notes.NOTE_C5,4, notes.NOTE_A4,-8, notes.NOTE_C5,16, notes.NOTE_E5,2,

            notes.NOTE_A5,4, notes.NOTE_A4,-8, notes.NOTE_A4,16, notes.NOTE_A5,4, notes.NOTE_GS5,-8, notes.NOTE_G5,16, #7 
            notes.NOTE_DS5,16, notes.NOTE_D5,16, notes.NOTE_DS5,8, notes.REST,8, notes.NOTE_A4,8, notes.NOTE_DS5,4, notes.NOTE_D5,-8, notes.NOTE_CS5,16,

            notes.NOTE_C5,16, notes.NOTE_B4,16, notes.NOTE_C5,16, notes.REST,8, notes.NOTE_F4,8, notes.NOTE_GS4,4, notes.NOTE_F4,-8, notes.NOTE_A4,-16, #9
            notes.NOTE_A4,4, notes.NOTE_F4,-8, notes.NOTE_C5,16, notes.NOTE_A4,2],
        "miiTempo": 114,
        "miiMelody": [
            # Score available at https://musescore.com/user/16403456/scores/4984153
            # Uploaded by Catalina Andrade 
  
            notes.NOTE_FS4,8, notes.REST,8, notes.NOTE_A4,8, notes.NOTE_CS5,8, notes.REST,8,notes.NOTE_A4,8, notes.REST,8, notes.NOTE_FS4,8, # 1
            notes.NOTE_D4,8, notes.NOTE_D4,8, notes.NOTE_D4,8, notes.REST,8, notes.REST,4, notes.REST,8, notes.NOTE_CS4,8,
            notes.NOTE_D4,8, notes.NOTE_FS4,8, notes.NOTE_A4,8, notes.NOTE_CS5,8, notes.REST,8, notes.NOTE_A4,8, notes.REST,8, notes.NOTE_F4,8,
            notes.NOTE_E5,-4, notes.NOTE_DS5,8, notes.NOTE_D5,8, notes.REST,8, notes.REST,4,
            
            notes.NOTE_GS4,8, notes.REST,8, notes.NOTE_CS5,8, notes.NOTE_FS4,8, notes.REST,8,notes.NOTE_CS5,8, notes.REST,8, notes.NOTE_GS4,8, # 5
            notes.REST,8, notes.NOTE_CS5,8, notes.NOTE_G4,8, notes.NOTE_FS4,8, notes.REST,8, notes.NOTE_E4,8, notes.REST,8,
            notes.NOTE_E4,8, notes.NOTE_E4,8, notes.NOTE_E4,8, notes.REST,8, notes.REST,4, notes.NOTE_E4,8, notes.NOTE_E4,8,
            notes.NOTE_E4,8, notes.REST,8, notes.REST,4, notes.NOTE_DS4,8, notes.NOTE_D4,8, 

            notes.NOTE_CS4,8, notes.REST,8, notes.NOTE_A4,8, notes.NOTE_CS5,8, notes.REST,8,notes.NOTE_A4,8, notes.REST,8, notes.NOTE_FS4,8, # 9
            notes.NOTE_D4,8, notes.NOTE_D4,8, notes.NOTE_D4,8, notes.REST,8, notes.NOTE_E5,8, notes.NOTE_E5,8, notes.NOTE_E5,8, notes.REST,8,
            notes.REST,8, notes.NOTE_FS4,8, notes.NOTE_A4,8, notes.NOTE_CS5,8, notes.REST,8, notes.NOTE_A4,8, notes.REST,8, notes.NOTE_F4,8,
            notes.NOTE_E5,2, notes.NOTE_D5,8, notes.REST,8, notes.REST,4,

            notes.NOTE_B4,8, notes.NOTE_G4,8, notes.NOTE_D4,8, notes.NOTE_CS4,4, notes.NOTE_B4,8, notes.NOTE_G4,8, notes.NOTE_CS4,8, # 13
            notes.NOTE_A4,8, notes.NOTE_FS4,8, notes.NOTE_C4,8, notes.NOTE_B3,4, notes.NOTE_F4,8, notes.NOTE_D4,8, notes.NOTE_B3,8,
            notes.NOTE_E4,8, notes.NOTE_E4,8, notes.NOTE_E4,8, notes.REST,4, notes.REST,4, notes.NOTE_AS4,4,
            notes.NOTE_CS5,8, notes.NOTE_D5,8, notes.NOTE_FS5,8, notes.NOTE_A5,8, notes.REST,8, notes.REST,4, 

            notes.REST,2, notes.NOTE_A3,4, notes.NOTE_AS3,4, # 17 
            notes.NOTE_A3,-4, notes.NOTE_A3,8, notes.NOTE_A3,2,
            notes.REST,4, notes.NOTE_A3,8, notes.NOTE_AS3,8, notes.NOTE_A3,8, notes.NOTE_F4,4, notes.NOTE_C4,8,
            notes.NOTE_A3,-4, notes.NOTE_A3,8, notes.NOTE_A3,2,

            notes.REST,2, notes.NOTE_B3,4, notes.NOTE_C4,4, # 21
            notes.NOTE_CS4,-4, notes.NOTE_C4,8, notes.NOTE_CS4,2,
            notes.REST,4, notes.NOTE_CS4,8, notes.NOTE_C4,8, notes.NOTE_CS4,8, notes.NOTE_GS4,4, notes.NOTE_DS4,8,
            notes.NOTE_CS4,-4, notes.NOTE_DS4,8, notes.NOTE_B3,1,
            
            notes.NOTE_E4,4, notes.NOTE_E4,4, notes.NOTE_E4,4, notes.REST,8, # 25

            # repeats 1-25

            # finishes with 26
            notes.NOTE_FS4,8, notes.REST,8, notes.NOTE_A4,8, notes.NOTE_CS5,8, notes.REST,8, notes.NOTE_A4,8, notes.REST,8, notes.NOTE_FS4,8
        ]
    }

    options = ["zelda", "birthday", "starwars", "mii"]

    def __init__(self, pin):
        self.buzzer = pin
        if str(type(pin)) != "<class 'Pin'>":
            raise TypeError("Must provide pin")


    def play(self, song):
        if song not in self.options:
            print("options are:", *self.options)
            return
        m = song+"Melody"
        t = song+"Tempo"
        melody = self.bank[m]
        tempo = self.bank[t]
        buzzer = self.buzzer
        
        numNotes=len(melody)/2

        wholenote = (60 * 4) / tempo

        divider = 0
        noteDuration = 0

        # entire array is twice the size as the number of notes
        for thisNote in range(0,numNotes*2,2):

            # calculates the duration of each note
            divider = melody[thisNote + 1]
            if divider > 0:
                # regular note, just proceed
                noteDuration = (wholenote) / divider
            elif divider < 0:
                # dotted notes are represented with negative durations!!
                noteDuration = (wholenote) / abs(divider)
                noteDuration *= 1.5 # increases the duration in half for dotted notes

            # we only play the note for 90% of the duration, leaving 10% as a pause
            simpleio.tone(buzzer, melody[thisNote], duration = noteDuration*0.9)

            # Wait for the specief duration before playing the next note.
            time.sleep(noteDuration*0.1)

            # stop the waveform generation before the next note.
            simpleio.tone(buzzer,0,duration = 0)
        out = "done playing"
        print(out)
