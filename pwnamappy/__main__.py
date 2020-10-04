import argparse
import sys
from pwnamappy.wpasec import ApiRetriever
from pwnamappy.wpasec import FileRetriever
from pwnamappy.wiggle import WiggleMapper
from pwnamappy.output import CsvFormatter
from pwnamappy.log import Logger


def run_pipeline(logger, retriever, mapper, formatter):
    nets = []
    if callable(retriever):
        logger.info('Retrieving networks')
        nets = retriever()
        logger.info('Got %d unique networks' % len(nets))

    coordinates = {}
    if len(nets) > 0 and callable(mapper):
        logger.info('Mapping networks')
        for net in nets:
            logger.verbose('Mapping %s %s' % (net.addr, net.name))
            location = None
            try:
                location = mapper(net)
            except Exception as exception:
                logger.info(exception.__repr__())
                break
            if location:
                coordinates[net] = location
            else:
                logger.info('No location found for %s %s' % (net.addr, net.name))
        logger.info('Mapped %d networks' % len(coordinates))

    if len(coordinates) > 0 and callable(formatter):
        logger.info('Saving results')
        formatter(coordinates)


def main():
    parser = argparse.ArgumentParser(description='Plots wifis on map')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-ws', '--wpa-sec-key', type=str, default=None)
    group.add_argument('-f', '--input', metavar='in-file',
                       type=argparse.FileType('r'))
    parser.add_argument('-wg', '--wiggle-key', type=str,
                        default=None, required=True)
    parser.add_argument('-o', '--output', metavar='out-file',
                        type=argparse.FileType('w'))
    args = parser.parse_args()

    retriever = None
    if args.wpa_sec_key:
        retriever = ApiRetriever(args.wpa_sec_key)
    elif args.input:
        retriever = FileRetriever(args.input)

    mapper = None
    if args.wiggle_key:
        mapper = WiggleMapper(args.wiggle_key)

    destination = None
    if args.output:
        destination = args.output
    else:
        destination = sys.stdout

    formatter = CsvFormatter(destination)

    logger = Logger()

    run_pipeline(logger, retriever, mapper, formatter)


if __name__ == '__main__':
    main()
