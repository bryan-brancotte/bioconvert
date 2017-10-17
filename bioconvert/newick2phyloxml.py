"""Convert :term:`NEWICK` file to :term:`PHYLOXML` file"""
import os

from bioconvert import ConvBase
from easydev.multicore import cpu_count

import colorlog
logger = colorlog.getLogger(__name__)


class NEWICK2PHYLOXML(ConvBase):
    """Convert :term:`NEWICK` file to :term:`PHYLOXML` file

    This tool just needs an input newick file, that will be
    converted into phyloxml format.
    """
    input_ext = [".nhx", ".nh", ".nw"]
    output_ext = [".phyloxml",".xml"]

    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile: input Newick tree file
        :param str outfile: output filename

        command used::

            gotree reformat phyloxml -f newick 

        """
        super(NEWICK2PHYLOXML, self).__init__(infile, outfile, *args, **kargs)
        self.threads = cpu_count()

    def __call__(self):
        cmd = "gotree reformat phyloxml -f newick -i {} -o {}".format(self.infile,
                                                                      self.outfile)
        try:
            self.execute(cmd)
        except:
            logger.debug("FIXME. The ouput message from gotree is on stderr...")
