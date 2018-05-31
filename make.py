#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse
import os
import shutil
from subprocess import call

DEBUG = True

SRC_FOLDER = 'src/'

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

def export(base_file: str, colors: [str] = [DEFAULT_COLOR], size: int = DEFAULT_SIZE, svg_dir: str = DEFAULT_DIR, png: bool = True, png_dir: str = DEFAULT_DIR):
    mkdir(svg_dir)
    mkdir(png_dir)

    # Open source file
    tree = ET.parse(SRC_FOLDER + base_file + '.ink.svg')
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

        tree.write(svg_dir + '/' + base_file + '_' + c + '.svg')

        # Generate the .png-files, if it has been selected to do so
        if png:
            res = call(['inkscape',
                  '--export-png',
                  png_dir + '/' + base_file + '_' + str(size) + 'px_' + c + '.png',
                  '--export-height=' + str(size),
                  svg_dir + '/' + base_file + '_' + c + '.svg'])

            if res != 0:
                # The build failed. Abort the process
                return res

    # Building was successful for all files
    return 0

def main():
    # Commandline options
    parser = argparse.ArgumentParser(description = 'Generate FOSS-AG design bitmaps from SVG source files')

    parser.add_argument('-a', '--all', action = 'store_true', help = 'Build all colors and all flavours available')
    parser.add_argument('--clean', action = 'store_true', help = 'Remove all generated files. All other options will be ignored')
    parser.add_argument('-p', '--png_only', action = 'store_true', help = 'Only store the png files. The SVG files will still need to be generated, but will be stored in the tmp dir')
    parser.add_argument('-v', '--svg_only', action = 'store_true', help = 'Only generate the SVG files')
    parser.add_argument('-s', '--size', nargs = '?', type = int, default = DEFAULT_SIZE, help = 'The size the generated bitmap file(s) should have. Default is ' + str(DEFAULT_SIZE))
    parser.add_argument('-c', '--colors', nargs = '*', default = [DEFAULT_COLOR], help = 'The colors the script should generate. Default is single ' + DEFAULT_COLOR + ' version. This argument will be ignored when the --all flag is set')
    parser.add_argument('-r', '--round', action = 'store_true', help = 'Build the round version of the logo. Overwritten by all')
    parser.add_argument('-q', '--quadratic', action = 'store_true', help = 'Build the quadratic version. This is default and only needed when building multiple versions.')

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

    # The files that are used to build from. By default it is the quadratic base
    # file
    base_files = []
    if not args.all:
        if args.round:
            base_files.append('logo_round')
        if args.quadratic:
            base_files.append('logo_square')

        # If none are set, the default base.ink.svg will be built
        if not args.round and not args.quadratic:
            base_files.append('logo_square')

    # Make sure all colors and flavours are built when the all option is set
    if args.all:
        args.colors = ACCENT_PALETTE
        base_files.append('logo_square')
        base_files.append('logo_round')

    svg_dir = DEFAULT_DIR;
    if args.png_only:
        svg_dir = "/tmp"

    print('Building the following colors:', args.colors)

    successful = True
    for flavour in base_files:
        print('Making file: ', flavour)
        export(flavour, args.colors, args.size, svg_dir, not args.svg_only, DEFAULT_DIR)

if __name__ == "__main__":
    main()
