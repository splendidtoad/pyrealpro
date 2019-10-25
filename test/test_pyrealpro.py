import unittest
import pyrealpro

TITLE = "A Test Song"

class TestSongs(unittest.TestCase):
    """Tests related to the Song class."""

    def test_default_key_signature(self):
        """
        Test that Songs default to the key of C if no key is provided.
        """
        s = pyrealpro.Song(title=TITLE)
        self.assertEqual(s.key, "C", "Default Key Signature should be 'C'.")

    def test_default_style(self):
        """
        Test that a Song's style defaults to 'Medium Swing' if no style is provided.
        """
        s = pyrealpro.Song(title=TITLE)
        self.assertEqual(s.style, 'Medium Swing', "Default style should be 'Medium Swing'.")

    def test_invalid_style(self):
        """
        Test that attempting to specify an unsupported style raises a ValueError
        """
        with self.assertRaises(ValueError):
            pyrealpro.Song(title=TITLE, style="Klezmer")

    def test_default_title(self):
        """
        Test that a Song's title defaults to 'Untitled' if none is provided.
        """
        s = pyrealpro.Song()
        self.assertEqual(s.title, 'Untitled', "Default title should be 'Untitled'.")

    def test_default_composer(self):
        """
        Test that a Song's composer defaults to 'Unknown' if no style is provided.
        """
        s = pyrealpro.Song(title=TITLE)
        self.assertEqual(s.composer, 'Unknown', "Default composer should be 'Unknown'.")


class TestMeasures(unittest.TestCase):
    """Tests related to the Measure class."""

    def test_default_measure_time_signature(self):
        """
        Test that a new Measure defaults to 4/4 if no time signature is provided.
        """
        m = pyrealpro.Measure(chords='C')
        self.assertEqual(m.time_sig.__str__(), 'T44', "Default time signature should be 'T44'.")

    def test_chord_length_mismatch(self):
        """
        Test that trying to instantiate a Measure with a chords list that does not match the expected number of
        measures indicated by the time signature raises a ValueError.
        """
        with self.assertRaises(ValueError):
            # TODO test with random values
            pyrealpro.Measure(chords=['C', ' ', ' '], time_sig=pyrealpro.TimeSignature(4, 4))

    def test_measure_from_chord_string(self):
        """
        Test that instantiating a measure with a string representing a single chord builds the chords list correctly
        """
        # TODO test multiple time signatures
        m = pyrealpro.Measure(chords='C', time_sig=pyrealpro.TimeSignature(4, 4))
        expected_chords_list = ['C', ' ', ' ', ' ']
        self.assertListEqual(m.chords, expected_chords_list)

    def test_measure_string_from_chords_string(self):
        """
        Test that Measure.__str__() returns the expected value when a single chord is provided as a string.
        """
        # TODO test multiple time signatures
        m = pyrealpro.Measure(chords='C', time_sig=pyrealpro.TimeSignature(5, 4))
        expected_measure_string = 'C    |'
        self.assertEqual(m.__str__(), expected_measure_string)

    def test_measure_string_from_chords_list(self):
        """
        Test that Measure.__str__() returns the expected value when chords are provided as a list.
        """
        m = pyrealpro.Measure(chords=['C', None, 'G7', None], time_sig=pyrealpro.TimeSignature(4, 4))
        expected_measure_string = 'C G7 |'
        self.assertEqual(m.__str__(), expected_measure_string)

    def test_modulo_chord_padding(self):
        """
        Test that passing a list of chords that is smaller than the number of beats in the time signature returns a
        an evenly padded string if the number of beats is evenly divisible by the number of chords
        """
        chords = ['C', 'F']
        m = pyrealpro.Measure(chords=chords, time_sig=pyrealpro.TimeSignature(4, 4))
        self.assertEqual(m.__str__(), 'C F |')
        m = pyrealpro.Measure(chords=chords, time_sig=pyrealpro.TimeSignature(6, 4))
        self.assertEqual(m.__str__(), 'C  F  |')
        m = pyrealpro.Measure(chords=['C', 'F', 'G'], time_sig=pyrealpro.TimeSignature(6, 4))
        self.assertEqual(m.__str__(), 'C F G |')


class TestTimeSignatures(unittest.TestCase):
    """Tests related to time signature handling."""

    def test_expected_ts_str(self):
        """Test that TimeSignature __str__() returns the expected values."""

        expected_sigs = (
            (4, 4, 'T44'),
            (3, 4, 'T34'),
            (2, 4, 'T24'),
            (5, 4, 'T54'),
            (6, 4, 'T64'),
            (7, 4, 'T74'),
            (2, 2, 'T22'),
            (3, 2, 'T32'),
            (5, 8, 'T58'),
            (6, 8, 'T68'),
            (7, 8, 'T78'),
            (9, 8, 'T98'),
            (12, 4, 'T12')
        )

        for beats, duration, expected_str in expected_sigs:
            ts = pyrealpro.TimeSignature(beats, duration)
            self.assertEqual(ts.__str__(), expected_str)

    def test_invalid_signature(self):
        """Test that passing an invalid time signature to the beats() function raises a ValueError."""
        with self.assertRaises(ValueError):
            pyrealpro.TimeSignature(4, 5)


if __name__ == '__main__':
    unittest.main()


