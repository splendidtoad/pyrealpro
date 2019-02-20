from urllib.parse import quote


class Song:
    """A lightweight class based on the iReal Pro file format described at
    https://irealpro.com/ireal-pro-file-format/."""

    KEY_SIGNATURES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B', 'A-', 'Bb-', 'B-', 'C-', 'C#-',
                      'D-', 'Eb-', 'E-', 'F-', 'F#-', 'G-', 'G#-']

    TIME_SIGNATURES = ['T44', 'T34', 'T24', 'T54', 'T64', 'T74', 'T22', 'T32', 'T58', 'T68', 'T78', 'T98', 'T12']

    def __init__(self, **kwargs):

        # Required properties:
        self.title = kwargs['title']
        self.chord_progression = kwargs['chord_progression']

        if 'key' in kwargs and kwargs['key'] in Song.KEY_SIGNATURES:
            if kwargs['key'] not in Song.KEY_SIGNATURES:
                raise ValueError("'{}' is not a valid key signature.".format(kwargs['key']))
            self.key = kwargs['key']
        else:
            self.key = 'C'

        if 'composer' in kwargs:
            self.composer = kwargs['composer']
        else:
            self.composer = "Unknown"

        if 'style' in kwargs:
            self.style = kwargs['style']
        else:
            self.style = 'Medium Swing'

        if 'time_sig' in kwargs:
            validate_time_signature(kwargs['time_sig'])
            self.time_sig = kwargs['time_sig']
        else:
            self.time_sig = 'T44'

    @property
    def url(self):
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

    def __init__(self, chords, time_sig='T44'):
        validate_time_signature(time_sig)
        self.time_sig = time_sig
        self.beats = beats(time_sig)
        self.chords = []

        if type(chords) == str:
            self.chords.append(chords)
            for i in range(0, self.beats - 1):
                self.chords.append(' ')
        else:
            if len(chords) != self.beats:
                raise ValueError("Expected data for {} beats, got {} instead.".format(self.beats, len(chords)))
            self.chords = chords

    def __str__(self):
        return "".join(self.chords)


def beats(time_sig):
    """Given a time signature, return the number of beats."""
    validate_time_signature(time_sig)

    # "T12" is actually 12/8:
    if time_sig == "T12":
        return 12
    else:
        return int(list(time_sig)[1])


def validate_time_signature(time_sig):
    """Given a time signature string, test whether it is valid."""
    if time_sig not in Song.TIME_SIGNATURES:
        raise ValueError("'{}' is not a valid time signature.".format(time_sig))
