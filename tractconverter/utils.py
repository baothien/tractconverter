import os
import logging

from tractconverter.formats.tck import TCK
from tractconverter.formats.trk import TRK
from tractconverter.formats.fib import FIB
from tractconverter.formats.vtk import VTK

# Supported format
FORMATS = {"tck": TCK,
           "trk": TRK,
           "fib": FIB,
           "vtk": VTK}

# Input and output extensions.
EXT_ANAT = ".nii|.nii.gz"


def is_supported(filename):
    return detect_format(filename) is not None


def detect_format(filename):
    if not os.path.isfile(filename):
        return FORMATS.get(filename[-3:], None)

    for format in FORMATS.values():
        if format._check(filename):
            return format

    return None


def convert(input, output, verbose=False):
    from tractconverter.formats.header import Header

    nbFibers = 0
    fibers = []
    for i, f in enumerate(input):
        fibers.append(f)
        if (i + 1) % 100 == 0:
            output += fibers
            fibers = []

        if i % 1000 == 0:
            logging.info('(' + str(nbFibers) + "/" + str(input.hdr[Header.NB_FIBERS]) + ' fibers)')

        nbFibers += 1

    if len(fibers) > 0:
        output += fibers

    output.close()

    logging.info('Done! (' + str(nbFibers) + "/" + str(input.hdr[Header.NB_FIBERS]) + ' fibers)')

