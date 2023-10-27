import re
import sys
from typing import List, Dict, Tuple, Optional
from socket import gethostbyname
from time import sleep
from collections import defaultdict
from typing import Union
import urllib3

import requests
from requests.exceptions import HTTPError
from requests.models import Response

from constants import (REQUEST_TIMEOUT, START_BAD_STATUS_CODE, ERROR_EXIT_CODE,
                       MIN_CONTENT_LENGTH, SUCCESS_EXIT_CODE)
from configs import configure_arguments
from exceptions import BadSite


class Checker:
    EXIT_ITEM: str = '0'
    URL_REGEXP: str = (
        r'(?P<protocol>https?://)?'
        r'(?:(?P<host>[.\w-]+\.(?:xn\-\-[\w]+|[A-Za-z]{2,}))|'
        r'(?P<ip>(?:[0-9]{1,3}\.){3}[0-9]{1,3}))'
        r'(?P<port>:\d+)?'
        r'(?P<path>/.+)?'
    )
    PROBLEM_TEMPLATE = (
            'Requested url: {}\n'
            'Destination url: {}\n'
            'Response status code: {}\n'
            'Error reason: {}\n'
            'Redirects: {}'
    )

    def __init__(self, args):
        self.args = args
        self.__sites_to_check: List[str] = self.__get_sites_to_check()
        self.__checked_sites: Dict[str, dict] = dict()
        self.__interactive_menu: Optional[str] = None

    def __get_sites_to_check(self) -> List[str]:
        """
        Return the list of sites to check.
        If argument `list` is not empty, return the content of this argument.
        Else, try to open the file, specified in argument `file` and then,
        return the list of domains in it.
        """
        if self.args.list is not None:
            return self.args.list

        try:
            with open(self.args.file, 'r') as file:
                sites = []
                for domain in file.readlines():
                    domain = domain.strip()
                    if not domain.startswith('#') and domain:
                        sites.append(domain)

                if not len(sites):
                    raise RuntimeError(
                        f'ERROR! File {self.args.file} is empty. '
                        f'There is nothing to check.'
                    )
                return sites

        except FileNotFoundError:
            print(
                f'ERROR! File with list of sites not found: {self.args.file}',
                file=sys.stderr
            )
            raise SystemExit(ERROR_EXIT_CODE)
        except RuntimeError as error:
            print(str(error), file=sys.stderr)
            raise SystemExit(ERROR_EXIT_CODE)

    def start_checking(self):
        """Begins checking sites to collect information about the
        functionality of URLs."""
        try:
            self.__checked_sites.clear()

            for site in self.__sites_to_check:
                self.__check_site(site)
                sleep(self.args.sleep)

            self.__calculate_results()
            self.__print_results()
        except KeyboardInterrupt:
            print('The program was stopped by the user.')
            self.__calculate_results()
            self.__print_results()

            raise SystemExit(ERROR_EXIT_CODE)

        try:
            self.__run_interactive_error_checking()
        except KeyboardInterrupt:
            raise SystemExit(ERROR_EXIT_CODE)

    def __print_errors_menu(self):
        """Print interactive menu with errors."""
        if self.__interactive_menu is None:
            message = ['Here are responses with errors:']
            message.extend(
                [
                    f'{number}: {url}'
                    for number, url in self.__sites_with_error_map.items()
                ]
            )
            self.__interactive_menu = '\n'.join(message)

        print(self.__interactive_menu)

    def __check_selected_item(self, item: str):
        """Checks the validity of a user-specified menu item."""
        if item == self.EXIT_ITEM:
            raise SystemExit(SUCCESS_EXIT_CODE)
        return (not item.isnumeric()
                or int(item) not in self.__sites_with_error_map)

    def __run_interactive_error_checking(self):
        if self.__sites_with_error_map:
            self.__print_errors_menu()
            print('Select the number of response you want to check, '
                  'or 0 to exit.')
            selected_item = input()
            while self.__check_selected_item(selected_item):
                print(f'Please, write a correct number or 0 to exit:')
                selected_item = input()

            self.__print_information_about_error(int(selected_item))
            print('\nTo another check, press enter.')
            input()
            self.__run_interactive_error_checking()

    @staticmethod
    def __processing_redirects(redirects: Optional[list]) -> Optional[str]:
        """Generate information message about redirects."""
        if redirects:
            redirects_message = [f'({len(redirects)}):']
            for redirect in redirects:
                redirects_message.append(
                    f'- {redirect.url} -> {redirect.headers["Location"]}'
                )

            return '\n'.join(redirects_message)

    def __print_information_about_error(self, number: int):
        """Print all information about user-specified problem."""
        url = self.__sites_with_error_map[number]
        response_data = self.__checked_sites[url]
        redirects = self.__processing_redirects(response_data.get('history'))
        print(self.PROBLEM_TEMPLATE.format(
            url,
            response_data.get('destination_url'),
            response_data.get('status_code'),
            response_data.get('err_reason'),
            redirects
        ))

    def __calculate_results(self) -> None:
        """Calculate site checking information."""
        statuses = defaultdict(int)
        sites_with_errors = []

        for url, result in self.__checked_sites.items():
            status_code = result.get('status_code')
            statuses[status_code] += 1

            if result.get('err_reason') is not None:
                sites_with_errors.append(url)

        sites_with_error_map = {
            index: site for index, site in enumerate(sites_with_errors, 1)
        }

        self.__statuses = statuses
        self.__sites_with_error_map = sites_with_error_map

    def __print_results(self) -> None:
        """Prints general information based on site scan results."""
        if self.__checked_sites:
            result = [f'Sites checked: {len(self.__checked_sites)}']
            statuses = self.__statuses.copy()
            unreached = statuses.pop(None, None)
            statuses = sorted(statuses.items())

            for status_code, count in statuses:
                if status_code >= START_BAD_STATUS_CODE:
                    count = self.colorize(count)
                result.append(f'{status_code}: {count}')

            if unreached:
                result.append(f'unreached: {self.colorize(unreached)}')

            print(' | '.join(result))

    @classmethod
    def __check_content_length(
            cls, response: Response
    ) -> Tuple[str, Optional[str]]:
        """
        Check the content length of response with status code 200.
        This is necessary because some sites may give a 200 response code,
        but will not work correctly, returning a blank page.
        """
        if (response.status_code == requests.codes.ok
                and len(response.content) < MIN_CONTENT_LENGTH):
            return (cls.colorize('!'),
                    f'Content length is too small: {len(response.content)}')

        return '', None

    def __check_site(self, site: str) -> None:
        """Makes HTTP-request to the specified URL, collects information about
        the request."""
        try:
            url, domain = self.__parse_url(site)
        except BadSite as error:
            print(str(error))
            return

        try:
            response = requests.get(url, **self.__configure_request_params())

            alert, possible_error = self.__check_content_length(response)

            response_info = (
                f'{response.status_code}{alert} - {url} '
                f'({gethostbyname(domain)}) -> '
                f'{response.url} - {response.elapsed.total_seconds()}'
            )
            print(response_info)

            self.__checked_sites[url] = {
                'response_overall_info': response_info,
                'status_code': response.status_code,
                'headers': response.headers,
                'history': response.history,
                'err_reason': possible_error,
                'destination_url': response.url
            }

            response.raise_for_status()

        except HTTPError as error:
            self.__checked_sites[url]['err_reason'] = str(error)
        except requests.RequestException as error:
            response_info = f'000 - {site} - unreachable'
            print(response_info)
            self.__checked_sites[url] = {
                'response_overall_info': response_info,
                'status_code': None,
                'headers': None,
                'history': None,
                'err_reason': str(error),
                'destination_url': None
            }

    @classmethod
    def __parse_url(cls, site: str) -> Tuple[str, str]:
        """
        Trying to parse the site url from string.
        Return URL to request and host.
        """
        url = re.search(cls.URL_REGEXP, site)
        if url is None:
            raise BadSite(f'BAD SITE: {site}. Skip.')

        return (
            f'{url.group("protocol") or "http://"}'
            f'{url.group("host") or url.group("ip")}'
            f'{url.group("port") or ""}'
            f'{url.group("path") or ""}'
        ), url.group("host") or url.group("ip")

    def __configure_request_headers(self) -> dict:
        """
        Configure dictionary with custom request headers.
        https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers
        """
        return {'User-Agent': self.args.user_agent}

    def __configure_request_params(self) -> dict:
        """Configure GET-request parameters."""
        return {
            'headers': self.__configure_request_headers(),
            'timeout': REQUEST_TIMEOUT,
            'verify': self.args.verify
        }

    @staticmethod
    def colorize(number: Union[str, int]) -> Union[str, int]:
        """Makes not zero string or number red color."""
        return f'\033[91m{number}\033[0m' if number else number


if __name__ == '__main__':
    args = configure_arguments()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    checker = Checker(args)
    checker.start_checking()
