from socket import gethostbyname
from time import sleep
from collections import defaultdict
from typing import Union
import urllib3

import requests

from constants import (SLEEP_SECONDS, REQUEST_HEADERS, REQUEST_TIMEOUT, VERIFY,
                       SITES_LIST_FILE, START_BAD_STATUS_CODE)


def if_color(amount: Union[str, int]) -> Union[str, int]:
    """Makes not zero string or number red color."""
    return f'\033[91m{amount}\033[0m' if amount else amount


def print_check_result(data: dict, bad_requests: list) -> None:
    """Print check results."""
    total = sum(data.values())
    unreached = if_color(data.pop('unreached', 0))
    statuses = sorted(data.items())
    result = [f'Sites checked: {total}']
    for status_code, count in statuses:
        if status_code >= START_BAD_STATUS_CODE:
            count = if_color(count)
        result.append(f'{status_code}: {count}')
    if unreached:
        result.append(f'unreached: {unreached}')
    print(' | '.join(result))

    if bad_requests:
        print('\nList of problems:')
        print('\n'.join(bad_requests))


def checker(sites_list: list) -> None:
    """Check every site in list and return conclusion."""
    checker_data = defaultdict(int)
    bad_requests = []

    if not len(sites_list):
        print('The list of sites is empty!')
        raise SystemExit(1)

    for site in sites_list:
        try:
            response = requests.get(
                'http://' + site,
                headers=REQUEST_HEADERS,
                timeout=REQUEST_TIMEOUT,
                verify=VERIFY
            )
            response_info = (
                f'{response.status_code} - {site} ({gethostbyname(site)}) -> '
                f'{response.url} - {response.elapsed.total_seconds()}'
            )
            print(response_info)

            if response.status_code >= START_BAD_STATUS_CODE:
                bad_requests.append(response_info)

            checker_data[response.status_code] += 1
            sleep(SLEEP_SECONDS)
        except requests.RequestException:
            response_info = f'000 - {site} - unreachable'
            print(response_info)
            checker_data['unreached'] += 1
            bad_requests.append(response_info)
        except KeyboardInterrupt:
            print('The program was stopped by the user. '
                  'Here are some partial results:')
            print_check_result(checker_data, bad_requests)
            raise SystemExit(1)

    print_check_result(checker_data, bad_requests)


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    with open(SITES_LIST_FILE) as file:
        sites = [site.strip() for site in file.read().split()]
    checker(sites)
