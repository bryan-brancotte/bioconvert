"""Convert :term:`CRAM` file to :term:`BAM` file"""
import os
from bioconvert import ConvBase
from easydev.multicore import cpu_count

import colorlog
logger = colorlog.getLogger(__name__)


class CRAM2BAM(ConvBase):
    """Convert :term:`CRAM` file to :term:`SAM` file

    The conversion requires the reference corresponding to the input file
    It can be provided as an argument in the constructor. Otherwise, 
    a local file with same name as the input file but an .fa extension is looked
    for. Otherwise, we ask for the user to provide the input file. This is 
    useful for the standalone application.

    """
    input_ext = [".cram"]
    output_ext = ".bam"

    def __init__(self, infile, outfile, reference=None, *args, **kargs):
        """.. rubric:: constructor

        :param str infile: input CRAM file
        :param str outfile: output BAM filename
        :param str reference: reference file in :term:`FASTA` format

        command used::

            samtools view -@ <thread> -Sh -T <reference> in.cram > out.bam

        .. note:: the API related to the third argument may change in the future.
        """
        super(CRAM2BAM, self).__init__(infile, outfile, *args, **kargs)

        self._default_method = "samtools"

        self.reference = reference
        if self.reference is None:
            logger.debug("No reference provided. Infering from input file")
            # try to find the local file replacing .sam by .fa
            reference = infile.replace(".cram", ".fa")
            if os.path.exists(reference):
                logger.debug("Reference found from inference ({})".format(reference))
            else:
                logger.debug("No reference found.")
                msg = "Please enter the reference corresponding "
                msg += "to the input BAM file:"
                reference = input(msg)
                if os.path.exists(reference) is False:
                    raise IOError("Reference required")
                else:
                    logger.debug("Reference exist ({}).".format(reference))

            self.reference = reference
        self.threads = cpu_count()

    def _method_samtools(self, *args, **kwargs):
        # -S means ignored (input format is auto-detected)
        # -b means output is BAM
        cmd = "samtools view -@ {} -Sb {} > {}".format(self.threads, 
            self.infile, self.outfile)


        self.execute(cmd)





