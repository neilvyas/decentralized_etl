"""
Decentralized ETL
-----------------

A demonstration of using a decorator registry to write a modular,
extensible, and loosely-coupled data model and ETL pipeline.

Usage:
    app.py <logfile> [--outfile=<outfile>]
    app.py run_multiple <log_directory> [--outfile=<outfile>]
    app.py (-h | --help | --version)

Options:
    -h, --help           Show this screen and exit.
    --outfile=<outfile>  File to write final effects to, if needed. [default: None]
"""
from decentralized_etl import app
from docopt import docopt


args = docopt(__doc__)

if __name__ == "__main__":
    pass
