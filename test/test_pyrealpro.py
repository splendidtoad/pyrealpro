import unittest
import pyrealpro


#TestMissingMeasureTimeSignature

TITLE = "A Test Song"
CHORD_PROGRESSION = "[c   |c   |f   |g   ]"


class TestSongs(unittest.TestCase):
    """Tests related to the Song class."""

    def test_missing_title(self):
        """
        Test that instantiating a Song without a title raises a KeyError.
        """
        with self.assertRaises(KeyError):
            pyrealpro.Song(chord_progression=CHORD_PROGRESSION)

    def test_missing_chords(self):
        """
        Test that instantiating a Song without a chord progression raises a KeyError.
        """
        with self.assertRaises(KeyError):
            pyrealpro.Song(title=TITLE)

    def test_missing_key_signature(self):
        """
        Test that Songs default to the key of C if no key is provided.
        """
        s = pyrealpro.Song(title=TITLE, chord_progression=CHORD_PROGRESSION)
        self.assertEqual(s.key, "C", "Default Key Signature should be 'C'.")

    def test_missing_time_signature(self):
        """
        Test that Songs default to 4/4 time if no time signature is provided.
        """
        s = pyrealpro.Song(title=TITLE, chord_progression=CHORD_PROGRESSION)
        self.assertEqual(s.time_sig, 'T44', "Default Time Signature should be 'T44'.")

    def test_invalid_time_signature(self):
        """
        Test that an invalid time signature raises a ValueError.
        """
        with self.assertRaises(ValueError):
            pyrealpro.Song(title=TITLE, chord_progression=CHORD_PROGRESSION, time_sig="T45")

    def test_missing_style(self):
        """
        Test that a Song's style defaults to 'Medium Swing' of no style is provided.
        """
        s = pyrealpro.Song(title=TITLE, chord_progression=CHORD_PROGRESSION)
        self.assertEqual(s.style, 'Medium Swing', "Default style should be 'Medium Swing'.")


class TestMeasures(unittest.TestCase):
    """Tests related to the Measure class."""

    def test_default_measure_time_signature(self):
        """
        Test that a new Measure defaults to 4/4 if no time signature is provided.
        """
        m = pyrealpro.Measure()
        self.assertEqual(m.time_sig, 'T44', "Default time signature should be 'T44'.")

    def test_invalid_measure_time_signature(self):
        """
        Test that an invalid Measure key signature raises a ValueError.
        """
        with self.assertRaises(ValueError):
            pyrealpro.Measure('T45')


if __name__ == '__main__':
    unittest.main()


