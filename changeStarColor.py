#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse

# Commandline options
parser = argparse.ArgumentParser(description='Modify svg fill colors')
parser.add_argument('newColor', nargs='?', default='foss-ag_green',
                   help='color in hex (default foss-ag green: #14b967)')

# Read command line input
args = parser.parse_args()

# Open original file
tree = ET.parse('src/base.ink.svg')
root = tree.getroot()
# Search tag
c = root.find(".//*[@id='path6107-4-3']")
c.set('fill','url(#' + args.newColor + ')' )
c.set('stroke','url(#' + args.newColor + ')' )


# Write to tmp file
tree.write('output/tmp.svg')
