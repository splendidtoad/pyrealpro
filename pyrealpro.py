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
        # TODO handling for 'chords' as either string or list
        # TODO self.chords should be a list
        # TODO if chords is a list, validate the length of the list against the time signature numerator
        self.chords = []
        # TODO support either a single string value (which implies that the chord lasts the full measure)
        #      OR a list.  If 'chords' is a string, then build self.chords out using that chord plus the rest of the
        #      measure with spaces per the time signature.  If it's a list, then validate the list length per the time
        #      signature and assign it to self.chords.







def validate_time_signature(time_sig):
    """Given a string, test whether it is valid."""
    if time_sig not in Song.TIME_SIGNATURES:
        raise ValueError("'{}' is not a valid time signature.".format(time_sig))
