import json
from bioconvert.bam2json import BAM2JSON
from bioconvert import bioconvert_data
from easydev import TempFile, md5


def ordered(obj):
    """
    recursively sort any lists it finds.
    Also convert dictionaries to lists of (key, value) pairs so that they're orderable.
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def read_bamtools_json(path):
    """
    json generated by bamtools are actually list of JSON.
    Each read is converted to a json which is independant from the others

    :return: list of dictionnary corresponding to JSON
    :rtype: LIST of JSON
    """
    with open(path, 'r') as jsonfile:
        json_list = []
        for line in jsonfile:
            json_list.append(json.loads(line))
    # Remove filename content which is necessary going to be different
    for read in json_list:
        del read['filename']
    return json_list


def test_conv():
    infile = bioconvert_data("test_measles.sorted.bam")
    outfile = bioconvert_data("test_measles.sorted.json")
    with TempFile(suffix=".json") as tempfile:
        # Make conversion
        convert = BAM2JSON(infile, tempfile.name)
        convert(method="bamtools")
        # Load both json files
        ori = read_bamtools_json(outfile)
        gen = read_bamtools_json(tempfile.name)
        # Check whether both list are identical
        assert ordered(gen) == ordered(ori)