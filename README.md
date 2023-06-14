# Script for checking the work of migrated sites

### Requirements

* Python 3.6+

### How to use

Clone the repo and change directory to it:
```shell
git clone https://github.com/melax08/site_checker.git && cd site_checker
```

Create venv and activate it:

```shell
python3 -m venv venv && source venv/bin/activate
```

Install requirements from **requirements.txt**:
```shell
python3 -m pip install --upgrade pip && pip install -r requirements.txt
```

Fill in the sites.txt file like this with a list of your sites:
```text
example.com
example2.com
example3.com
```

Run **site_checker.py** in directory with script:
```shell
python3 site_checker.py
```

### Settings
You can change the settings of the script. All of them you can find in file **constants.py**.
Here is a description of some settings:

**SLEEP_SECONDS** - time in seconds between checking each site. Default: 1.

**REQUEST_HEADERS** - a dictionary with parameters that will be passed in the request headers. By default, there is only one setting here - User-Agent.

**REQUEST_TIMEOUT** - request timeout specified in seconds. Default: 10.

**VERIFY** - whether to disallow invalid or self-signed certificates. Default: False