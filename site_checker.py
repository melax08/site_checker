import requests
from socket import gethostbyname
from time import sleep

SLEEP_SECONDS = 1
REQUEST_HEADERS = {
    'User-Agent': 'melax08 Site Checker v1'
}


def if_color(amount):
    """Make not zero string red color"""
    if amount > 0:
        amount = "\033[91m{}".format(amount)+"\033[0m"
        return amount
    else:
        return amount


with open("list_sites.txt") as file:
    sites_file = file.read()
    sites_list = sites_file.split()


two = three = four = five = unreach = 0

for site in sites_list:
    try:
        response = requests.get('http://' + site, headers=REQUEST_HEADERS)
        print(f'{response.status_code} - {site} ({gethostbyname(site)}) -> '
              f'{response.url} - {response.elapsed.total_seconds()}')
        if response.status_code == 200:
            two += 1
        elif 300 <= response.status_code < 400:
            three += 1
        elif 400 <= response.status_code < 500:
            four += 1
        elif response.status_code > 499:
            five += 1
        sleep(SLEEP_SECONDS)
    except requests.ConnectionError:
        print(f'000 - {site} - unreachable')
        unreach += 1
    except KeyboardInterrupt:
        print('The program was stopped by the user')
        quit()

print(f'Sites checked: {len(sites_list)} | 200: {two} | 3xx: {three} | 4xx: {if_color(four)} | 5xx: {if_color(five)} | unreached: {if_color(unreach)}')