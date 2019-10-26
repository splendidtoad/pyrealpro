from urllib.parse import quote

KEY_SIGNATURES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B', 'A-', 'Bb-', 'B-', 'C-', 'C#-',
                      'D-', 'Eb-', 'E-', 'F-', 'F#-', 'G-', 'G#-']

STYLES_JAZZ = ["Afro 12/8",
               "Ballad Double Time Feel",
               "Ballad Even",
               "Ballad Melodic",
               "Ballad Swing",
               "Blue Note",
               "Bossa Nova",
               "Doo Doo Cats",
               "Double Time Swing",
               "Even 8ths",
               "Even 8ths Open",
               "Even 16ths",
               "Guitar Trio",
               "Gypsy Jazz",
               "Latin",
               "Latin/Swing",
               "Long Notes",
               "Medium Swing",
               "Medium Up Swing",
               "Medium Up Swing 2",
               "New Orleans Swing",
               "Second Line",
               "Slow Swing",
               "Swing Two/Four",
               "Trad Jazz",
               "Up Tempo Swing",
               "Up Tempo Swing 2", ]

STYLES_LATIN = ["Argentina: Tango",
                "Brazil: Bossa Acoustic",
                "Brazil: Bossa Electric",
                "Brazil: Samba",
                "Cuba: Bolero",
                "Cuba: Cha Cha Cha",
                "Cuba: Son Montuno 2-3",
                "Cuba: Son Montuno 3-2", ]

STYLES_POP = ["Bluegrass",
              "Country",
              "Disco",
              "Funk",
              "Glam Funk",
              "House",
              "Reggae",
              "Rock",
              "Rock 12/8",
              "RnB",
              "Shuffle",
              "Slow Rock",
              "Smooth",
              "Soul",
              "Virtual Funk", ]

STYLES_ALL = STYLES_JAZZ + STYLES_LATIN + STYLES_POP


class Song:
    """A lightweight class based on the iReal Pro file format described at
    https://irealpro.com/ireal-pro-file-format/."""

    # TODO handle composer last/first name consistently ("Foo Bar" gets parsed by irealpro as "Bar Foo", apparently "Last First"

    measures = None

    def __init__(self, **kwargs):
        """
        Initialize a new iRealPro Song object.
        :param kwargs:
        Required:

        Optional:
        - title: The Song Title (defaults to 'Untitled')
        - key: The song key signature (defaults to 'C')
        - composer: The song composer (defaults to 'Unknown')
        - style: The iRealPro song style (defaults to 'Medium Swing')
        - measures: A list of Measure objects.
        """
        # Required properties:

        if 'title' in kwargs:
            self.title = kwargs['title']
        else:
            self.title = 'Untitled'

        if 'key' in kwargs and kwargs['key'] in KEY_SIGNATURES:
            if kwargs['key'] not in KEY_SIGNATURES:
                raise ValueError("'{}' is not a valid key signature.".format(kwargs['key']))
            self.key = kwargs['key']
        else:
            self.key = 'C'

        if 'composer' in kwargs:
            self.composer = kwargs['composer']
        else:
            self.composer = "Unknown"

        if 'style' in kwargs:
            if kwargs['style'] in STYLES_ALL:
                self.style = kwargs['style']
            else:
                raise ValueError(f"{kwargs['style']} is not a valid iRealPro style.")
        else:
            self.style = 'Medium Swing'

        if 'measures' in kwargs:
            self.measures = kwargs['measures']

    def url(self, urlencode=True):
        """
        Render Song as an iRealPro data URL.
        """
        # If the first measure has no opening barline defined, make it a double barline
        if self.measures[0].barline_open == "":
            self.measures[0].barline_open = "["
        # If the last measure has no barline or the default barline, make it a final double barline
        if self.measures[-1].barline_close in ["", "|", None]:
            self.measures[-1].barline_close = "Z"
        # If this song has any measures defined, force the first one to render its time signature
        if len(self.measures) > 0:
            self.measures[0].render_ts = True
        if self.measures is not None:
            measures_str = "".join(m.__str__() for m in self.measures)
        else:
            measures_str = ""

        url = f"irealbook://{self.title}={self.composer}={self.style}={self.key}=n={measures_str}"

        if urlencode:
            return quote(url, safe=":/=")
        else:
            return url

    def __str__(self):
        return "<{} {}: {}>".format(type(self).__name__, id(self), self.title)


class Measure:
    """Represents a single measure."""

    BARLINES_OPEN = [
        "[",  # opening double bar line
        "{",  # opening repeat bar line

    ]

    BARLINES_CLOSE = [
        "|",  # single bar line
        "]",  # closing double bar line
        "}",  # closing repeat bar line
        "Z",  # Final thick double bar line
    ]

    REHEARSAL_MARKS = [
        "*A",  # A section
        "*B",  # B section
        "*C",  # C Section
        "*D",  # D Section
        "*V",  # Verse
        "*i",  # Intro
        "S",  # Segno
        "Q",  # Coda
        "f",  # Fermata
    ]

    ENDINGS = [
        "N1",  # First ending
        "N2",  # Second Ending
        "N3",  # Third Ending
        "N0",  # No text Ending
    ]

    chords = None
    time_sig = None
    rehearsal_marks = None
    render_ts = False
    barline_open = None
    barline_close = None
    ending = None
    staff_text = None

    def __init__(self, chords, time_sig=None, rehearsal_marks=[], barline_open="", barline_close=None, ending="",
                 staff_text="", render_ts=False):
        """
        Initialize an iRealPro measure.
        :param chords: A string representing a single chord, or a list of chords. If a list is provided, the list
                       length must match the number of beats indicated by the time signature.
        :param time_sig: The measure time signature.
        """
        if time_sig is None:
            time_sig = TimeSignature(4, 4)
        self.time_sig = time_sig
        self.rehearsal_marks = rehearsal_marks
        if barline_open is None:
            barline_open = ""
        self.barline_open = barline_open
        self.ending = ending
        # Measure should always have an ending barline
        if barline_close is None or barline_close == "":
            barline_close = "|"
        self.barline_close = barline_close
        self.staff_text = staff_text
        self.ending = ending
        self.render_ts = render_ts
        if type(chords) == str:
            self.chords = [chords]
            for i in range(0, self.time_sig.beats - 1):
                self.chords.append(' ')
        elif len(chords) == self.time_sig.beats:
            # Replace any instances of `None` with spaces
            self.chords = [' ' if c is None else c for c in chords]
        elif self.time_sig.beats % len(chords) == 0:
            # If beats modulo chords length is zero, then spread them out evenly to fill the measure
            pad = int((self.time_sig.beats - len(chords)) / len(chords))
            self.chords = []
            for chord in chords:
                self.chords.append(chord)
                for i in range(0, pad):
                    self.chords.append(' ')
        else:
            raise ValueError("Expected data for {} beats, got {} instead.".format(self.time_sig.beats, len(chords)))
        if type(rehearsal_marks) == str:
            self.rehearsal_marks = [rehearsal_marks]
        else:
            self.rehearsal_marks = rehearsal_marks

    def __str__(self):
        chords_str = "".join(self.chords)
        if self.render_ts:
            ts = self.time_sig
        else:
            ts = ""
        if self.staff_text != "":
            staff_text = f"<{self.staff_text}>"
        else:
            staff_text = ""
        # TODO add support for rehearsal marks
        return f"{self.barline_open}{ts}{staff_text}{self.ending}{chords_str}{self.barline_close}"


class TimeSignature:
    VALID_TIME_SIGNATURES = ['T44', 'T34', 'T24', 'T54', 'T64', 'T74', 'T22', 'T32', 'T58', 'T68', 'T78', 'T98', 'T12']
    beats = None
    duration = None

    def __init__(self, beats=4, duration=4):
        if beats:
            self.beats = beats
        if duration:
            self.duration = duration
        if self.__str__() not in self.VALID_TIME_SIGNATURES:
            raise ValueError(
                f"{beats}/{duration} may be a valid time signature, but \"{self}\" is not supported by iRealPro."
            )

    def __str__(self):
        if self.beats == 12:  # Special case for 12/4, which iRealPro formats as simply "T12"
            return "T12"
        else:
            return f"T{self.beats}{self.duration}"
