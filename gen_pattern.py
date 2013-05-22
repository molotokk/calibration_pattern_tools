#/usr/bin/env python

from svgfig import *
#import sys
import argparse



class PatternMaker:
    def __init__(self, pattern_type):
        self.pattern_type = pattern_type
        self.columns = 8
        self.rows = 6
        self.output = 'out.svg'
        self.units = 'mm'
        self.spacing = None
        self.radius = None
        self.width = 210
        self.height = 297
        self.g = SVG("g") # the svg group container
        return

    def recalculateParameters(self):
        # If circle or square spacing is not defined, calculate it to fit page dimensions
        if not args.spacing:
            if (self.pattern_type == 'checkerboard'): # hack to correctly arrange the checkerboard pattern
                w_spacing = math.floor(args.page_width * 0.95 / (args.columns + 1))
                h_spacing = math.floor(args.page_height * 0.95 / (args.rows + 1))
            else:
                w_spacing = math.floor(args.page_width / (args.columns))
                h_spacing = math.floor(args.page_height / (args.rows))
            self.spacing = min(w_spacing, h_spacing)

        if self.radius is None:
            self.radius = self.spacing / 5.0
        return

    def printParameters(self):
        print("Spacing      : %s %s" % (self.spacing, self.units))
        print("Rows         : %s" % (self.rows) )
        print("Columns      : %s" % (self.columns) )
        return

    def generatePattern(self):
        self.recalculateParameters()
        self.printParameters()

        #dict for easy lookup of pattern type
        mp = {"circles": self.__make_circles_pattern,
              "acircles": self.__make_acircles_pattern,
              "checkerboard": self.__make_checkerboard_pattern}
        mp[self.pattern_type]()
        return

    def savePattern(self, output_file):
        c = canvas(self.g, width="%d%s" % (self.width, self.units),
                   height="%d%s" % (self.height, self.units),
                   viewBox="0 0 %d %d" % (self.width, self.height))
        c.save(output_file)

        # View the generate file
        #c.inkview(output_file)
        return

    def __make_circles_pattern(self):
        r =self.spacing / 5.0  # radius is a 5th of the spacing TODO parameterize
        c_margin = (self.width - (self.columns + 1) * self.spacing) / 2
        r_margin = (self.height - (self.rows + 1) * self.spacing) / 2
        for x in range(1, self.columns + 1):
            for y in range(1, self.rows + 1):
                dot = SVG("circle", cx=x *self.spacing + c_margin, cy=y * self.spacing + r_margin, r=r, fill="black",
                    stroke="none")
                self.g.append(dot)
        return

    def __make_acircles_pattern(self):
        r =self.spacing / 5.0
        c_margin = (self.width - (self.columns - 1) * self.spacing) / 2
        r_margin = (self.height - (self.rows - 1) * self.spacing) / 2
        for i in range(0, self.columns):
            for j in range(0, self.rows):
                if ((i + j) % 2): # similar to checkerboard
                    dot = SVG("circle", cx=(i) * self.spacing + c_margin, cy=(j) * self.spacing + r_margin, width=self.spacing,
                        height=self.spacing, r=r, fill="black", stroke="none")
                    #dot = SVG("circle", cx= ((j*2 + i%2)*spacing) +self.spacing , cy=self.height - (i *self.spacing +self.spacing) , r=r, fill="black")
                    self.g.append(dot)
        return

    def __make_checkerboard_pattern(self):
        # center the pattern in the middle of the page
        c_margin = float((self.width - (self.columns + 1) *self.spacing) / 2)
        r_margin = float((self.height - (self.rows + 1) *self.spacing) / 2)
        #print c_margin, r_margin
        for i in range(0, self.columns + 1): # we need to draw internal corners
            for j in range(0, self.rows + 1):
                if ((i + j) % 2):
                    dot = SVG("rect", x=(i) * self.spacing + c_margin, y=(j) * self.spacing + r_margin, width=self.spacing,
                        height=self.spacing, fill="black", stroke="none")
                    self.g.append(dot)
        return




    #def makePattern(cols,rows,output,p_type,units,square_size,page_width,page_height):
    #    width = page_width
    #   self.spacing = square_size
    #    height = page_height
    #    r =self.spacing / 5.0
    #    g = SVG("g") # the svg group container
    #    for x in range(1,cols+1):
    #      for y in range(1,rows+1):
    #        if "circle" in p_type:
    #          dot = SVG("circle", cx=x *self.spacing, cy=y *self.spacing, r=r, fill="black")
    #        g.append(dot)
    #    c = canvas(g,width="%d%s"%(width,units),height="%d%s"%(height,units),viewBox="0 0 %d %d"%(width,height))
    #    c.inkview(output)


if __name__ == "__main__":

    # parse command line options
    parser = argparse.ArgumentParser(description=("Script to generate optical calibration patterns."
                                                  " Currently supported are checkerboard, circles and assymetrical "
                                                  " circles calibration targets."))
    parser.add_argument("type", choices=['circles', 'acircles', 'checkerboard'], help="Calibration target type.")
    parser.add_argument("-o", "--output", default='out.svg', help="Pattern save file.  Default: out.svg")

    group_r_c = parser.add_argument_group("arrangement of markers")
    group_r_c.add_argument("-s", "--spacing", type=int,
        help="Spacing between rows and columns of calibration points. In case of 'checkerboard' pattern spacing  \
        is equal to square size.",
        default=None)
    group_r_c.add_argument("-r", "--rows", type=int, default=8)
    group_r_c.add_argument("-c", "--columns", type=int, default=6)

    group_size = parser.add_argument_group("pre-defined paper sizes")
    group_size.add_argument("-p", "--paper_type", choices=['letter', 'a4', 'a3'], default='a4',
        help="Note: Using the predefined sizes, units are automatically reset to mm.  Default: ISO A4")

    group_w_h = parser.add_argument_group("custom paper size definition")
    group_w_h.add_argument("-u", "--units", choices=['mm', 'cm', 'in'], default='mm', help="Default:  mm")
    group_w_h.add_argument("-W", "--page_width", type=float)
    group_w_h.add_argument("-H", "--page_height", type=float)

    args = parser.parse_args()

    print("\nGenerating calibration pattern\n")

    # Choose used paper size
    paper_sizes = {"us": ['mm', 216, 279], "a4": ['mm', 210, 297], "a3": ['mm', 297, 420]}
    if not (args.page_width and args.page_height):
        [args.units, args.page_width, args.page_height] = paper_sizes[args.paper_type]

        print("Paper size   : %s" % (args.paper_type))
        print(" width   :   %s" % (args.page_width))
        print(" height  :   %s" % (args.page_height))


    pm = PatternMaker(args.type)
    pm.units = args.units
    pm.width = args.page_width
    pm.height = args.page_height
    pm.rows = args.rows
    pm.columns = args.columns

    pm.generatePattern()
    pm.savePattern(args.output)

    print("saved as     : %s" % (args.output))
    print("\ndone.")

