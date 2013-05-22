Calibration Pattern Tools
=========================

Alexander Granizo 2013

Licence: MIT


gen_pattern is a python script useful for generation of various calibration patterns.  Symmetrical- / asymmetrical circles and checkerboard patterns are currently supported

	- Checkerboard
	- 
	- Asymetrical circles


Basic Usage
-----------


To get usage help, enter:

$ python gen_pattern.py --help 

Converting SVG files to PDF
---------------------------

Using Inkscape
--------------
Using Inkscape produces smaller files.
 
    $ inkscape pattern.svg --export-pdf=pattern.pdf 

Using Uniconvertor
------------------
Install the package python-uniconvertor.

    $ uniconvertor pattern.svg pattern.pdf


Printing the calibration pattern
--------------------------------

Print the PDF file choosing setting the option "Page Scaling" to None


