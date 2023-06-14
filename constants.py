from pathlib import Path

SLEEP_SECONDS: int = 1
REQUEST_HEADERS: dict = {
    'User-Agent': 'melax08 Site Checker v1'
}
REQUEST_TIMEOUT: int = 10
VERIFY: bool = False
SITES_LIST_FILE = Path(__file__).parent / 'sites.txt'
