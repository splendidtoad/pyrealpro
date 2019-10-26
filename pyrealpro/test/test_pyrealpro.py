import unittest

from pyrealpro.pyrealpro import *

TITLE = "A Test Song"
COMPOSER_NAME_FIRST = 'Arthur "Two-Sheds"'
COMPOSER_NAME_LAST = "Jackson"


class TestSongs(unittest.TestCase):
    """Tests related to the Song class."""

    def test_default_key_signature(self):
        """
        Test that Songs default to the key of C if no key is provided.
        """
        s = Song(title=TITLE)
        self.assertEqual(s.key, "C", "Default Key Signature should be 'C'.")

    def test_default_style(self):
        """
        Test that a Song's style defaults to 'Medium Swing' if no style is provided.
        """
        s = Song(title=TITLE)
        self.assertEqual(s.style, 'Medium Swing', "Default style should be 'Medium Swing'.")

    def test_invalid_style(self):
        """
        Test that attempting to specify an unsupported style raises a ValueError
        """
        with self.assertRaises(ValueError):
            Song(title=TITLE, style="Klezmer")

    def test_default_title(self):
        """
        Test that a Song's title defaults to 'Untitled' if none is provided.
        """
        s = Song()
        self.assertEqual(s.title, 'Untitled', "Default title should be 'Untitled'.")

    def test_default_composer(self):
        """
        Test that a Song's composer defaults to 'Unknown' if no style is provided.
        """
        s = Song(title=TITLE)
        self.assertEqual(s.composer_name, 'Unknown', "Default composer_name should be 'Unknown'.")

    def test_barline_and_ts_behavior(self):
        """
        Tests that the time signature of the first measure is always rendered, that the barline of the first measure is
        set to a double line, and that the barline of the last measure
        is always set to the final double bar (unless they are repeat brackets.)
        """
        m1 = Measure(chords='C')
        m2 = Measure(chords='G')
        s = Song(title=TITLE, composer_name_first=COMPOSER_NAME_FIRST, composer_name_last=COMPOSER_NAME_LAST, measures=[m1, m2])
        self.assertEqual(s.url(urlencode=False),
                         'irealbook://A Test Song=Jackson Arthur "Two-Sheds"=Medium Swing=C=n=[T44C   |G   Z')
        m3 = Measure(chords='A', barline_open='{', time_sig=TimeSignature(3, 4))
        m4 = Measure(chords='D', barline_close='}', time_sig=TimeSignature(3, 4))
        s2 = Song(title=TITLE, composer_name_first=COMPOSER_NAME_FIRST, composer_name_last=COMPOSER_NAME_LAST, measures=[m3, m4])

        self.assertEqual(s2.url(urlencode=False),
                         'irealbook://A Test Song=Jackson Arthur "Two-Sheds"=Medium Swing=C=n={T34A  |D  }')

    # TODO: test expected song URL


class TestMeasures(unittest.TestCase):
    """Tests related to the Measure class."""

    def test_default_measure_time_signature(self):
        """
        Test that a new Measure defaults to 4/4 if no time signature is provided.
        """
        m = Measure(chords='C')
        self.assertEqual(m.time_sig.__str__(), 'T44', "Default time signature should be 'T44'.")

    def test_chord_length_mismatch(self):
        """
        Test that trying to instantiate a Measure with a chords list that does not match the expected number of
        measures indicated by the time signature raises a ValueError.
        """
        with self.assertRaises(ValueError):
            # TODO test with random values
            Measure(chords=['C', ' ', ' '], time_sig=TimeSignature(4, 4))

    def test_measure_from_chord_string(self):
        """
        Test that instantiating a measure with a string representing a single chord builds the chords list correctly
        """
        # TODO test multiple time signatures
        m = Measure(chords='C', time_sig=TimeSignature(4, 4))
        expected_chords_list = ['C', ' ', ' ', ' ']
        self.assertListEqual(m.chords, expected_chords_list)

    def test_measure_string_from_chords_string(self):
        """
        Test that Measure.__str__() returns the expected value when a single chord is provided as a string.
        """
        # TODO test multiple time signatures
        m = Measure(chords='C', time_sig=TimeSignature(5, 4))
        expected_measure_string = 'C    |'
        self.assertEqual(m.__str__(), expected_measure_string)

    def test_measure_string_from_chords_list(self):
        """
        Test that Measure.__str__() returns the expected value when chords are provided as a list.
        """
        m = Measure(chords=['C', None, 'G7', None], time_sig=TimeSignature(4, 4))
        expected_measure_string = 'C G7 |'
        self.assertEqual(m.__str__(), expected_measure_string)

    def test_modulo_chord_padding(self):
        """
        Test that passing a list of chords that is smaller than the number of beats in the time signature returns a
        an evenly padded string if the number of beats is evenly divisible by the number of chords
        """
        chords = ['C', 'F']
        m = Measure(chords=chords, time_sig=TimeSignature(4, 4))
        self.assertEqual(m.__str__(), 'C F |')
        m = Measure(chords=chords, time_sig=TimeSignature(6, 4))
        self.assertEqual(m.__str__(), 'C  F  |')
        m = Measure(chords=['C', 'F', 'G'], time_sig=TimeSignature(6, 4))
        self.assertEqual(m.__str__(), 'C F G |')

    def test_staff_text(self):
        """
        Test that staff text is formatted correctly and in the expected position
        """
        m = Measure(chords='C', time_sig=TimeSignature(4, 4), staff_text="Test")
        self.assertEqual(m.__str__(), '<Test>C   |')
        m = Measure(chords=['C', 'F'], time_sig=TimeSignature(4, 4), staff_text='Test',
                              barline_open='{', barline_close='}')
        self.assertEqual(m.__str__(), '{<Test>C F }')
        m.render_ts = True
        self.assertEqual(m.__str__(), '{T44<Test>C F }')

    def test_barline_open(self):
        """
        Test opening barline options
        """
        m = Measure(chords='C', barline_open="")
        self.assertEqual(m.__str__(), 'C   |')
        m2 = Measure(chords='C', barline_open='[')
        self.assertEqual(m2.__str__(), '[C   |')
        m3 = Measure(chords='C', barline_open='{')
        m3.render_ts = True
        self.assertEqual(m3.__str__(), '{T44C   |')

    def test_barline_close(self):
        """
        Test closing barline options
        """
        m = Measure(chords='C', barline_close=None)
        self.assertEqual(m.__str__(), 'C   |')
        m = Measure(chords='C', barline_close='')
        self.assertEqual(m.__str__(), 'C   |')
        m2 = Measure(chords='C', barline_close=']')
        self.assertEqual(m2.__str__(), 'C   ]')
        m3 = Measure(chords='C', barline_close='}')
        self.assertEqual(m3.__str__(), 'C   }')
        m4 = Measure(chords='C', barline_close='Z')
        self.assertEqual(m4.__str__(), 'C   Z')

    def test_ending(self):
        """
        Test output of `ending` property
        """
        m = Measure(chords='C', ending='N1', barline_close='}')
        self.assertEqual(m.__str__(), 'N1C   }')
        m1 = Measure(chords=['C', 'G7'], ending="N2", barline_close='}', render_ts=True)
        self.assertEqual(m1.__str__(), 'T44N2C G7 }')

    def test_rehearsal_marks(self):
        """
        Test behavior of the rehearsal_marks property
        """
        m = Measure(chords='C', rehearsal_marks="*A", barline_open="[", render_ts=True)
        self.assertEqual(m.__str__(), '*A[T44C   |')
        m1 = Measure(chords=['G', 'C7'], rehearsal_marks=['*B', 'Q'])
        self.assertEqual(m1.__str__(), '*BG C7 Q|')
        with self.assertRaises(ValueError):
            Measure(chords='G', rehearsal_marks=['M'])


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
            ts = TimeSignature(beats, duration)
            self.assertEqual(ts.__str__(), expected_str)

    def test_invalid_signature(self):
        """Test that passing an invalid time signature to the beats() function raises a ValueError."""
        with self.assertRaises(ValueError):
            TimeSignature(4, 5)


class TestFullSong(unittest.TestCase):
    """Test construction and URL output of a complete song"""

    def test_blues(self):
        s = Song(title="Automation Blues", composer="pyrealpro", key='G', style='New Orleans Swing',
                 composer_name_first="Otto",
                 composer_name_last="Matonne")

        s.measures.append(Measure(chords='G7', barline_open='{', staff_text='Generated by pyrealpro'))
        s.measures.append(Measure(chords='G7'))
        s.measures.append(Measure(chords='G7'))
        s.measures.append(Measure(chords='G7', barline_close=']'))

        s.measures.append(Measure(chords='C7', barline_open='['))
        s.measures.append(Measure(chords='C7'))
        s.measures.append(Measure(chords='G7'))
        s.measures.append(Measure(chords='G7', barline_close=']'))

        s.measures.append(Measure(chords='D7', barline_open='['))
        s.measures.append(Measure(chords='C7'))

        s.measures.append(Measure(chords='G7', ending='N1'))
        s.measures.append(Measure(chords='D7', barline_close='}'))

        s.measures.append(Measure(chords='G7', ending='N2'))
        s.measures.append(Measure(chords='G7', barline_close='Z'))

        self.assertEqual(s.url(), "irealbook://Automation%20Blues=Matonne%20Otto=New%20Orleans%20Swing=G=n=%7BT44%3CGenerated%20by%20pyrealpro%3EG7%20%20%20%7CG7%20%20%20%7CG7%20%20%20%7CG7%20%20%20%5D%5BC7%20%20%20%7CC7%20%20%20%7CG7%20%20%20%7CG7%20%20%20%5D%5BD7%20%20%20%7CC7%20%20%20%7CN1G7%20%20%20%7CD7%20%20%20%7DN2G7%20%20%20%7CG7%20%20%20Z")
        self.assertEqual(s.url(urlencode=False), "irealbook://Automation Blues=Matonne Otto=New Orleans Swing=G=n={T44<Generated by pyrealpro>G7   |G7   |G7   |G7   ][C7   |C7   |G7   |G7   ][D7   |C7   |N1G7   |D7   }N2G7   |G7   Z")


if __name__ == '__main__':
    unittest.main()
