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

class Song:
    """A lightweight class based on the iReal Pro file format described at
    https://irealpro.com/ireal-pro-file-format/."""

    def __init__(self, **kwargs):
        """
        Initialize a new iRealPro Song object.
        :param kwargs:
        Required:

        - chord_progression: The song chord progression.

        Optional:
        - title: The Song Title (defaults to 'Untitled')
        - key: The song key signature (defaults to 'C')
        - composer: The song composer (defaults to 'Unknown')
        - style: The iRealPro song style (defaults to 'Medium Swing')
        - time_sig: A TimeSignature object. (Defaults to 4/4.)
        """
        # Required properties:

        self.chord_progression = kwargs['chord_progression']

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
            if kwargs['style'] in STYLES_JAZZ + STYLES_LATIN + STYLES_POP:
                self.style = kwargs['style']
            else:
                raise ValueError(f"{kwargs['style']} is not a valid iRealPro style.")
        else:
            self.style = 'Medium Swing'

        if 'time_sig' in kwargs:
            self.time_sig = kwargs['time_sig']
        else:
            self.time_sig = TimeSignature(4, 4)

    @property
    def url(self):
        """
        Render Song as an iRealPro data URL.
        """
        return quote("irealbook://{}={}={}={}=n={}{}".format(
            self.title,
            self.composer,
            self.style,
            self.key,
            self.time_sig,
            self.chord_progression
        ), safe=":/=")

    def __str__(self):
        return "<{} {}: {}>".format(type(self).__name__, id(self), self.title)


class Measure:
    """Represents a single measure."""

    def __init__(self, chords, time_sig=None):
        """
        Initialize an iRealPro measure.
        :param chords: A string representing a single chord, or a list of chords. If a list is provided, the list
                       length must match the number of beats indicated by the time signature.
        :param time_sig: The measure time signature.
        """
        if not time_sig:
            time_sig = TimeSignature(4, 4)
        self.time_sig = time_sig
        self.chords = []

        if type(chords) == str:
            self.chords.append(chords)
            for i in range(0, self.time_sig.beats - 1):
                self.chords.append(' ')
        else:
            if len(chords) != self.time_sig.beats:
                raise ValueError("Expected data for {} beats, got {} instead.".format(self.time_sig.beats, len(chords)))
            self.chords = chords

    def __str__(self):
        return "".join(self.chords)


class TimeSignature:
    VALID_SIGNATURES = ['T44', 'T34', 'T24', 'T54', 'T64', 'T74', 'T22', 'T32', 'T58', 'T68', 'T78', 'T98', 'T12']
    beats = 4
    duration = 4

    def __init__(self, beats=None, duration=None):
        if beats:
            self.beats = beats
        if duration:
            self.duration = duration
        if self.__str__() not in self.VALID_SIGNATURES:
            raise ValueError(f"{beats}/{duration} may be a valid time signature, but \"{self}\" \it is not supported by iRealPro.")

    def __str__(self):
        if self.beats == 12:  # Special case for 12/4, which iRealPro formats as simply "T12"
            return "T12"
        else:
            return f"T{self.beats}{self.duration}"
