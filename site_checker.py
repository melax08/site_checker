from socket import gethostbyname
from time import sleep
from collections import defaultdict

import requests

SLEEP_SECONDS: int = 1
REQUEST_HEADERS: dict = {
    'User-Agent': 'melax08 Site Checker v1'
}


def if_color(amount) -> str:
    """Makes not zero string or number red color."""
    return f'\033[91m{amount}\033[0m' if amount else amount


def print_check_result(results: dict, checked: int, unreached: int) -> None:
    """Print check results."""
    results = sorted(results.items())
    unreached = if_color(unreached)
    print(f'Sites checked: {checked}', end=' | ')
    for status_code, count in results:
        if status_code > 399:
            count = if_color(count)
        print(f'{status_code}: {count}', end=' | ')
    print(f'unreached: {unreached}')


def checker(sites_list: list) -> None:
    """Check every site in list and return conclusion."""
    total = 0
    unreached = 0
    status_code_count = defaultdict(int)

    if not len(sites_list):
        print('The list of sites is empty!')
        raise SystemExit(1)

    for site in sites_list:
        try:
            response = requests.get('http://' + site, headers=REQUEST_HEADERS)
            print(
                f'{response.status_code} - {site} ({gethostbyname(site)}) -> '
                f'{response.url} - {response.elapsed.total_seconds()}')

            status_code_count[response.status_code] += 1
            total += 1
            sleep(SLEEP_SECONDS)
        except requests.ConnectionError:
            print(f'000 - {site} - unreachable')
            unreached += 1
            total += 1
        except KeyboardInterrupt:
            print('The program was stopped by the user, here are results:')
            print_check_result(status_code_count, total, unreached)
            raise SystemExit(1)

    print_check_result(status_code_count, total, unreached)


if __name__ == '__main__':
    with open('list_sites.txt') as file:
        sites = file.read().split()
    checker(sites)
