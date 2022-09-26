import requests
from socket import gethostbyname
from time import sleep

SLEEP_SECONDS = 1
REQUEST_HEADERS = {
    'User-Agent': 'melax08 Site Checker v1'
}
RESULT = ('Sites checked: {} | '
          '200: {} | '
          '3xx: {} | '
          '4xx: {} | '
          '5xx: {} | '
          'unreached: {}')


def if_color(amount):
    """Makes not zero string or number red color."""
    if amount > 0:
        amount = "\033[91m{}".format(amount)+"\033[0m"
        return amount
    else:
        return amount


def checker(sites_list):
    """Main function."""
    status_code_count = {
        'total': 0,
        '200': 0,
        '3XX': 0,
        '4XX': 0,
        '5XX': 0,
        'unreached': 0
    }

    try:
        if len(sites_list) == 0:
            raise ValueError
    except ValueError:
        quit('The list of sites is empty!')

    for site in sites_list:
        try:
            response = requests.get('http://' + site, headers=REQUEST_HEADERS)
            print(
                f'{response.status_code} - {site} ({gethostbyname(site)}) -> '
                f'{response.url} - {response.elapsed.total_seconds()}')
            if response.status_code == 200:
                status_code_count['200'] += 1
            elif 300 <= response.status_code <= 399:
                status_code_count['3XX'] += 1
            elif 400 <= response.status_code <= 499:
                status_code_count['4XX'] += 1
            elif response.status_code >= 500:
                status_code_count['5XX'] += 1
            sleep(SLEEP_SECONDS)
        except requests.ConnectionError:
            print(f'000 - {site} - unreachable')
            status_code_count['unreached'] += 1
        except KeyboardInterrupt:
            quit('\nThe program was stopped by the user')
        status_code_count['total'] += 1

    status_code_count['4XX'] = if_color(status_code_count['4XX'])
    status_code_count['5XX'] = if_color(status_code_count['5XX'])
    status_code_count['unreached'] = if_color(status_code_count['unreached'])
    print(RESULT.format(*status_code_count.values()))


if __name__ == '__main__':
    with open("list_sites.txt") as file:
        sites_file = file.read()
        sites_list = sites_file.split()
    checker(sites_list)
