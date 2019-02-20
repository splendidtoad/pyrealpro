import unittest
import pyrealpro

TITLE = "A Test Song"
CHORD_PROGRESSION_STRING = "[C   |x   |F   |G   ]"
INVALID_TIME_SIGNATURE = 'T45'


class TestSongs(unittest.TestCase):
    """Tests related to the Song class."""

    def test_missing_title(self):
        """
        Test that instantiating a Song without a title raises a KeyError.
        """
        with self.assertRaises(KeyError):
            pyrealpro.Song(chord_progression=CHORD_PROGRESSION_STRING)

    def test_missing_chords(self):
        """
        Test that instantiating a Song without a chord progression raises a KeyError.
        """
        with self.assertRaises(KeyError):
            pyrealpro.Song(title=TITLE)

    def test_default_key_signature(self):
        """
        Test that Songs default to the key of C if no key is provided.
        """
        s = pyrealpro.Song(title=TITLE, chord_progression=CHORD_PROGRESSION_STRING)
        self.assertEqual(s.key, "C", "Default Key Signature should be 'C'.")

    def test_default_time_signature(self):
        """
        Test that Songs default to 4/4 time if no time signature is provided.
        """
        s = pyrealpro.Song(title=TITLE, chord_progression=CHORD_PROGRESSION_STRING)
        self.assertEqual(s.time_sig, 'T44', "Default Time Signature should be 'T44'.")

    def test_invalid_time_signature(self):
        """
        Test that an invalid time signature raises a ValueError.
        """
        with self.assertRaises(ValueError):
            pyrealpro.Song(title=TITLE, chord_progression=CHORD_PROGRESSION_STRING, time_sig=INVALID_TIME_SIGNATURE)

    def test_default_style(self):
        """
        Test that a Song's style defaults to 'Medium Swing' if no style is provided.
        """
        s = pyrealpro.Song(title=TITLE, chord_progression=CHORD_PROGRESSION_STRING)
        self.assertEqual(s.style, 'Medium Swing', "Default style should be 'Medium Swing'.")

    def test_default_composer(self):
        """
        Test that a Song's composer defaults to 'Unknown' if no style is provided.
        """
        s = pyrealpro.Song(title=TITLE, chord_progression=CHORD_PROGRESSION_STRING)
        self.assertEqual(s.composer, 'Unknown', "Default composer should be 'Unknown'.")


class TestMeasures(unittest.TestCase):
    """Tests related to the Measure class."""

    def test_default_measure_time_signature(self):
        """
        Test that a new Measure defaults to 4/4 if no time signature is provided.
        """
        m = pyrealpro.Measure(chords='C')
        self.assertEqual(m.time_sig, 'T44', "Default time signature should be 'T44'.")

    def test_invalid_measure_time_signature(self):
        """
        Test that an invalid Measure key signature raises a ValueError.
        """
        with self.assertRaises(ValueError):
            pyrealpro.Measure(chords='C', time_sig=INVALID_TIME_SIGNATURE)

    def test_chord_length_mismatch(self):
        """
        Test that trying to instantiate a Measure with a chords list that does not match the expected number of
        measures indicated by the time signature raises a ValueError.
        """
        with self.assertRaises(ValueError):
            # TODO test with random values
            pyrealpro.Measure(chords=['C', ' ', ' '], time_sig='T44')

    def test_measure_from_chord_string(self):
        """
        Test that instantiating a measure with a string representing a single chord builds the chords list correctly
        """
        # TODO test multiple time signatures
        m = pyrealpro.Measure(chords='C', time_sig='T44')
        expected_chords_list = ['C', ' ', ' ', ' ']
        self.assertListEqual(m.chords, expected_chords_list)

    def test_measure_string_from_chords_string(self):
        """
        Test that Measure.__str__() returns the expected value when a single chord is provided as a string.
        """
        # TODO test multiple time signatures
        m = pyrealpro.Measure(chords='C', time_sig='T54')
        expected_measure_string = 'C    '
        self.assertEqual(m.__str__(), expected_measure_string)

    def test_measure_string_from_chords_list(self):
        """
        Test that Measure.__str__() returns the expected value when chords are provided as a list.
        """
        m = pyrealpro.Measure(chords=['C', ' ', 'G7', ' '], time_sig='T44')
        expected_measure_string = 'C G7 '
        self.assertEqual(m.__str__(), expected_measure_string)


class TestTimeSignatures(unittest.TestCase):
    """Tests related to time signature handling."""

    def test_beats(self):
        """Test that the beats() function returns the expected value."""
        expected_values = {
            'T44': 4,
            'T34': 3,
            'T24': 2,
            'T54': 5,
            'T64': 6,
            'T74': 7,
            'T22': 2,
            'T32': 3,
            'T58': 5,
            'T68': 6,
            'T78': 7,
            'T98': 9,
            'T12': 12
        }

        for time_sig, expected_beats in expected_values.items():
            beats = pyrealpro.beats(time_sig)
            self.assertEqual(beats, expected_beats)

    def test_invalid_beats_arg(self):
        """Test that passing an invalid time signature to the beats() function raises a ValueError."""
        with self.assertRaises(ValueError):
            pyrealpro.beats(INVALID_TIME_SIGNATURE)


if __name__ == '__main__':
    unittest.main()


