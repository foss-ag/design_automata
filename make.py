#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse
import os
import shutil
from subprocess import call

DEBUG = True

DEFAULT_SIZE = 512
DEFAULT_COLOR = 'green'
DEFAULT_DIR = 'output'

ACCENT_PALETTE = [
    'green',
    'neon-green',
    'red',
    'crimson',
    'orange',
    'blue',
    'light-blue',
    'neon-blue',
    'violet',
    'purple',
    'magenta',
    'yellow',
    'orange',
    'neon-yellow',
    'lighter-grey',
    'dark-grey'
]

# Create an empty directory on path, if it does not already exist, otherwise do
# nothing
def mkdir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def export(colors: [str] = [DEFAULT_COLOR], form: [int] = [1], size: int = DEFAULT_SIZE, svg_dir: str = DEFAULT_DIR, png: bool = True, png_dir: str = DEFAULT_DIR):
    mkdir(svg_dir)
    mkdir(png_dir)

    # Open source file
    tree = ET.parse('src/base.ink.svg')
    root = tree.getroot()
    for f in form:
        for c in colors:
            if not c in ACCENT_PALETTE:
                print(c, "is not an accent color. Please choose one from the accent color list")
                continue

            if DEBUG:
                print("Generating files for color:", c)

            c_id = 'foss-ag_' + c;

            # Change color to the selected
            
            editAttribute(root, "star_left",'fill','url(#' + c_id + ')')
            editAttribute(root, "star_left",'stroke','url(#' + c_id + ')')
            
            # Disable Clip if needed
            if f == 2:
                editAttribute(root, "background","clip-path","")
            
            # write all changes to file
            tree.write(svg_dir + '/logoForm'+ str(f) + '_'  + c + '.svg')

            # Generate the .png-files, if it has been selected to do so
            if png:
                res = call(['inkscape',
                      '--export-png',
                      png_dir + '/logoForm' + str(f) + '_' + str(size) + 'px_' + c + '.png',
                      '--export-height=' + str(size),
                      svg_dir + '/logoForm'+ str(f) + '_'  + c + '.svg'])

                if res != 0:
                    # The build failed. Abort the process
                    return res

    # Building was successful for all files
    return 0
    
    #only call this after tree has been build
def editAttribute(root: str, node_id: str, name: str, value: str):
    t = root.find(".//*[@id='" + node_id + "']") #node needs an id to be found and changed
    t.set(name,value)

    return 0 #After all changes please call tree.write

def main():
    # Commandline options
    parser = argparse.ArgumentParser(description = 'Generate FOSS-AG design bitmaps from SVG source files')

    parser.add_argument('-a', '--all', action = 'store_true', help = 'Build all colors available')
    parser.add_argument('--clean', action = 'store_true', help = 'Remove all generated files. All other options will be ignored')
    parser.add_argument('-p', '--png_only', action = 'store_true', help = 'Only store the png files. The SVG files will still need to be generated, but will be stored in the tmp dir')
    parser.add_argument('-v', '--svg_only', action = 'store_true', help = 'Only generate the SVG files')
    parser.add_argument('-s', '--size', nargs = '?', type = int, default = DEFAULT_SIZE, help = 'The size the generated bitmap file(s) should have. Default is ' + str(DEFAULT_SIZE))
    parser.add_argument('-c', '--colors', nargs = '*', default = [DEFAULT_COLOR], help = 'The colors the script should generate. Default is single ' + DEFAULT_COLOR + ' version. This argument will be ignored when the --all flag is set')
    parser.add_argument('-r', '--form', nargs = '*', default = [1], help = 'Form-Factor: round (1), rect (2)')

    # Read command line input
    args = parser.parse_args()

    # If the clean flag is set, remove the output dir and exit
    if args.clean:
        if not os.path.exists(DEFAULT_DIR):
            print('No files found. Nothing to do for clean')
            return 0

        print('Removing generated files')
        shutil.rmtree(DEFAULT_DIR)
        return 0

    # Check for argument combinations that don't make sense
    if args.png_only and args.svg_only:
        print('--png_only and --svg_only cannot be set at the same time. Aborting')
        return 1

    # Make sure all colors are built when the all option is set
    if args.all:
        args.colors = ACCENT_PALETTE
        args.form = [1,2] # 1 = round, 2 = rectangle

    svg_dir = DEFAULT_DIR
    if args.png_only:
        svg_dir = "/tmp"

    print('Building the following colors:', args.colors)

    return export(args.colors, args.form, args.size, svg_dir, not args.svg_only, DEFAULT_DIR)

if __name__ == "__main__":
    main()
