0.2.0 - The Measure __str__() method now adds a comma between all chords
        and spaces in the measure; this prevents iRealPro from choking on
        run-on chord names if a measure has a different chord for every 
        beat; for example, "EbG-Bb-C7" is now "Eb,G-,Bb-,C7"
        and "C   " is now "C, , , "
0.1.3 - Fix Song.ur() for Songs with no measures
      - Fix package/module namespacing

0.1.2 - Refactor to remove redundant top-level "pyrealpro" module  
      - Check in missing `doc` directory  
      - Add Changelog

0.1.1 - Fix package homepage URL

0.1.0 - Initial release