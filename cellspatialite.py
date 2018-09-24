#!python
"""Usage: cellspatialite.py FILE [-c|--config=<CONFIG_FILE>]

Arguments:
  FILE     database file

Options:
  -c, --config CONFIG_FILE    Use config file (default config.json)
  -h --help                   Show this screen.
"""
from docopt import docopt
import treatment

print('Cell spatialite')

if __name__ == '__main__':
  args = docopt(__doc__)

  print('Run traitment with database %s' % (args['FILE']))
  trt = treatment.Treatment(args['FILE']).start()
