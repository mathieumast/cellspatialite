#!/usr/bin/env python
'''Usage: cellspatialite.py INPUT OUTPUT [-c|--config=<CONFIG_FILE>]

Arguments:
  INPUT             input data directory
  OUTPUT            output database file

Options:
  -c, --config CONFIG_FILE    Use config file [default: config.json]
  -h --help                   Show this screen
'''
from docopt import docopt
from treatment import Treatment

def main():
    print('Cell spatialite')
    args = docopt(__doc__)

    input = args['INPUT']
    ouput = args['OUTPUT']

    print('Run traitment')
    Treatment(input, ouput).start()


if __name__ == '__main__':
    main()
