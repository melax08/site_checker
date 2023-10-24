from pathlib import Path
from typing import Union
import argparse

DEFAULT_SLEEP_TIME: Union[int, float] = 1
DEFAULT_SITES_FILENAME: str = 'sites.txt'
DEFAULT_SITES_FILE_PATH = Path(__file__).parent / DEFAULT_SITES_FILENAME
DEFAULT_REQUEST_USER_AGENT: str = 'melax08 Site Checker v1'


def configure_arguments():
    parser = argparse.ArgumentParser(description='melax08 site checker')

    parser.add_argument(
        '-s',
        '--sleep',
        type=float,
        default=DEFAULT_SLEEP_TIME,
        help=(f'Sleep seconds between checking sites. '
              f'Default: {DEFAULT_SLEEP_TIME}')
    )

    parser.add_argument(
        '-f',
        '--file',
        type=Path,
        default=DEFAULT_SITES_FILE_PATH,
        help=(f'Specify the path to the file that stores the list of sites to '
              f'check. Default: {DEFAULT_SITES_FILE_PATH}')

    )

    parser.add_argument(
        '-ua',
        '--user-agent',
        default=DEFAULT_REQUEST_USER_AGENT,
        help=(f'Specify the value for the `User-Agent` request header when '
              f'requesting sites. Default: {DEFAULT_REQUEST_USER_AGENT}')
    )

    parser.add_argument(
        '-l',
        '--list',
        nargs='*',
        help='Set sites to check without using a file with a list of sites.'
    )

    parser.add_argument(
        '-v',
        '--verify',
        action='store_true',
        help=('Requests verifies SSL certificates for HTTPS requests, '
              'just like a web browser. By default ignore verifying the '
              'SSL certificate.')
    )

    return parser.parse_args()
