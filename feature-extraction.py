# Script used for feature extraction from segmented nodule images.

import mahotas
import argparse
from itertools import chain

def write_row(output, items, name=None):
    if name:
        output.write(name)
    for it in items:
        output.write(',')
        output.write(str(it))
    output.write('\n')

parser = argparse.ArgumentParser(description='Feature extraction using mahotas')
parser.add_argument(
    'fnames', metavar='input_file_name', nargs='+', type=str, help='Image files names')
parser.add_argument(
    "-o", "--output", default='output.csv', type=str, help="Directs the output to a name of your choice")
parser.add_argument(
    '--radius', default=8, action='store', type=int,
    help='Radius to use for LBP and Zernike  features (default = 8)')
parser.add_argument(
    '--points', default=6, action='store', type=int,
    help='Nr of points to use for LBP features (default = 6)')

args = parser.parse_args();

output = open(args.output, 'w')
colnames = []

# Naming the columns
from mahotas.features.lbp import lbp_names
colnames.extend(lbp_names(args.radius, args.points))

for i in range(54):
    colnames.append("pftas")

for i in range(25):
    colnames.append("zernike")

write_row(output, colnames)

# Feature extraction
for fname in args.fnames:

    rows = []
    im = mahotas.imread(fname).max(2)

    lpb_row = mahotas.features.lbp(im, args.radius, args.points)
    rows.append(lpb_row)
    pftas_row = mahotas.features.pftas(im)
    rows.append(pftas_row)
    zernike_row = mahotas.features.zernike(im, args.radius, 8)
    rows.append(zernike_row)
    
    write_row(output, chain.from_iterable(rows), fname)

output.close()
        
