import argparse
from pwnamappy.wpasec import ApiRetriever, FileRetriever
from pwnamappy.wigle import WigleMapper
from pwnamappy.io import CsvExporter, CsvImporter
from pwnamappy.log import Logger


def run_pipeline(logger, retriever, mapper, importer, exporter):
    nets = []
    if callable(retriever):
        logger.info('Retrieving networks')
        nets = retriever()
        logger.info(f'Got {len(nets)} unique networks')

    coordinates = {}
    if callable(importer):
        logger.info('Importing previous results')
        coordinates = importer()

    if len(nets) > 0 and callable(mapper):
        logger.info('Mapping networks')
        count = 0
        tries = 0
        for net in nets:
            if net in coordinates:
                continue
            logger.verbose(f'Mapping {net.addr} {net.name}')
            location = None
            try:
                location = mapper(net)
            except Exception as exception:
                logger.error(exception.__repr__())
                break
            if location and location.lat == 0.0 and location.lon == 0.0:
                location = None
            coordinates[net] = location
            tries = tries + 1
            if location:
                count = count + 1
            else:
                logger.verbose(f'No location found for {net.addr} {net.name}')
        logger.info(f'Mapped {count} out of {tries} networks')

    if callable(exporter):
        logger.info('Saving results')
        exporter(coordinates)


def main():
    parser = argparse.ArgumentParser(description='Plots wifis on map')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-ws', '--wpa-sec-key', type=str, default=None)
    group.add_argument('-wsf', '--input', metavar='in-file',
                       type=argparse.FileType('r'))
    parser.add_argument('-wg', '--wigle-key', type=str,
                        default=None, required=True)
    parser.add_argument('-f', '--file', default='pwnamappy.csv',
                        type=str)
    args = parser.parse_args()

    logger = Logger()

    retriever = None
    if args.wpa_sec_key:
        retriever = ApiRetriever(args.wpa_sec_key)
    elif args.input:
        retriever = FileRetriever(args.input)

    mapper = None
    if args.wigle_key:
        mapper = WigleMapper(args.wigle_key)

    destination = args.file

    input_contents = None
    try:
        with open(destination, 'r') as input_file:
            input_contents = input_file.readlines()
    except IOError as error:
        logger.info(f'Failed to parse input file: {error}')
    importer = None
    if input_contents:
        importer = CsvImporter(input_contents)

    exporter = CsvExporter(lambda: open(destination, 'w+'))

    run_pipeline(logger, retriever, mapper, importer, exporter)


if __name__ == '__main__':
    main()
