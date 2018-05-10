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

def mkdir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def export(colors: [str] = [DEFAULT_COLOR], size: int = DEFAULT_SIZE, svg_dir: str = DEFAULT_DIR, png: bool = True, png_dir: str = DEFAULT_DIR):
    mkdir(svg_dir)
    mkdir(png_dir)

    # Open source file
    tree = ET.parse('src/base.ink.svg')
    root = tree.getroot()

    for c in colors:
        if not c in ACCENT_PALETTE:
            print(c, "is not an accent color. Please choose one from the accent color list")
            continue

        if DEBUG:
            print("Generating files for color:", c)

        c_id = 'foss-ag_' + c;

        # Change color to the selected
        t = root.find(".//*[@id='path6107-4-3']")
        t.set('fill','url(#' + c_id + ')' )
        t.set('stroke','url(#' + c_id + ')' )

        tree.write(svg_dir + '/logo_' + c + '.svg')

        # Generate the .png-files, if it has been selected to do so
        if png:
            call(['inkscape',
                  '--export-png',
                  png_dir + '/logo' + str(size) + 'px_' + c + '.png',
                  '--export-height=' + str(size),
                  svg_dir + '/logo_' + c + '.svg'])

def main():
    # Commandline options
    parser = argparse.ArgumentParser(description = 'Generate FOSS-AG design bitmaps from SVG source files')

    parser.add_argument('-a', '--all', action = 'store_true', help = 'Build all colors available')
    parser.add_argument('--clean', action = 'store_true', help = 'Remove all generated files. All other options will be ignored')
    parser.add_argument('-p', '--png_only', action = 'store_true', help = 'Only store the png files. The SVG files will still need to be generated, but will be stored in the tmp dir')
    parser.add_argument('-v', '--svg_only', action = 'store_true', help = 'Only generate the SVG files')
    parser.add_argument('-s', '--size', nargs = '?', type = int, default = DEFAULT_SIZE, help = 'The size the generated bitmap file(s) should have. Default is ' + str(DEFAULT_SIZE))
    parser.add_argument('-c', '--colors', nargs = '*', default = [DEFAULT_COLOR], help = 'The colors the script should generate. Default is single ' + DEFAULT_COLOR + ' version. This argument will be ignored when the --all flag is set')

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

    svg_dir = DEFAULT_DIR;
    if args.png_only:
        svg_dir = "/tmp"

    print('Building the following colors:', args.colors)

    export(args.colors, args.size, svg_dir, not args.svg_only, DEFAULT_DIR)

if __name__ == "__main__":
    main()
