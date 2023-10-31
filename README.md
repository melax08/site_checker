# Python CLI website and URLs checker

<div>
  <a href="#how-it-works">How it works?</a>&nbsp;&nbsp;&nbsp;
  <a href="#Installation">Installation</a>&nbsp;&nbsp;&nbsp;
  <a href="#How-to-use">How to use</a>&nbsp;&nbsp;&nbsp;
  <a href="#Usage-examples">Usage examples</a>&nbsp;&nbsp;&nbsp;
  <a href="#FAQ">FAQ</a>&nbsp;&nbsp;&nbsp;

</div>

## Information

### Description

This program with CLI-interface will help webmasters, system administrators and programmers check the availability of the list of migrated websites and URLs.

Imagine a situation: you need to **transfer 100+ websites** from one hosting to another, and then check their performance. Manually checking such a number of sites can take a very long time. With this program, you just need to list the necessary sites in a file, launch it and go drink coffee ☕

### How it works?

1. You specify the list of URLs to check using one of the methods described in <a href="#How-to-use">how to use section</a>.
2. The program starts making requests to every URL and then, checks the <a href="https://en.wikipedia.org/wiki/List_of_HTTP_status_codes">response status codes</a>.
In addition, the program checks the size of the requested page if the response code is `200 (OK)`. 
3. While the program is running, you will see the progress of requests, status codes and <a href="#Output-explanation">other information</a>.
4. At the end, the program will display a list of problematic requests: those with a status code of `4xx` or `5xx` or `200` with an empty page content.

### Features

- 🕑 **Saves time:** the program will check for you all the URLs that you specify to it and report their availability.
- 🪄 **Easy to use:** via a Cli interface, similar to any default Linux program.
- 🌴 **Without exotic libraries:** for the program to work, only one library is needed: `requests` (and related to it).


### Requirements

* Python 3.6+

### Author

Ilya Malashenko (github: melax08, telegram: @ScreamOFF)

## Documentation

### Installation

Clone the repository and go to the root directory with the program:
```shell
git clone https://github.com/melax08/site_checker.git && cd site_checker
```

Create `python` virtual environment and activate it:
```shell
python3 -m venv venv && source venv/bin/activate
```

Install requirements from the `requirements.txt` file:
```shell
python3 -m pip install --upgrade pip && pip install -r requirements.txt
```

Fill the `sites.txt` file with a list of URLs that require accessibility checking. You can also select a different site list file or specify a site list interactively. More details in the section <a href="#How-to-use">How to use</a>.
```text
example.com
example2.com
example3.com
```

### How to use

Go to the source directory and run the main program with the key `--help` 

```shell
cd src
```

```shell
python3 site_checker.py --help
```

In `help` you can see the whole list of application options.

### Keys

`-s` or `--sleep` - pause time in seconds between requests to specified sites. Default: 1 second. This setting is needed in order not to bring down a barrage of web requests on your server or hosting, in order to avoid HTTP flooding.

`-f` or `--file` - path to a file with a list of URLs to check. Default: `sites.txt` in directory with application (`site_checker/src/sites.txt`).

`-ua` or `--user-agent` - allows you to set your own value for the `User-Agent` request header. Default: `melax08 Site Checker v*`

`-l` or `--list` - allows you to specify a list of sites to check directly in this argument. When using this argument, the `--file` argument will not work.

`-v` or `--verify` - verifies SSL certificates for HTTPS requests just like a web browser. By default, ignore verifying the SSL certificate and allow self-signed certificates.

### Usage examples

![checker_example.png](readme_files/checker_example.png)

Simple usage with default arguments.
```shell
python3 site_checker.py
```

Specify the path to your file with a list of URLs (`-f`), with a pause of 5 seconds between checks (`-s`) and custom User-Agent request header (`-ua`).

```shell
python3 site_checker.py -f /path/to/some/file.txt -s 5 -ua "My custom user-agent"
```

Check the list of sites specified after `-l` argument:

```shell
python3 site_checker.py -l example.com facebook.com google.com
```

### Output explanation

Using the example of a Google request:

```shell
200 - http://google.com (142.250.187.142) -> http://www.google.com/ - 0.42356
```

* `200` - the response status code.
* `http://google.com` - source requested URL.
* `142.250.187.142` - IP of the requested host.
* `http://www.google.com/` - destination URL after all redirects.
* `0.42356` - time spent on request in seconds.

### Additional settings
You can also change some settings of the script in `constants.py` file.
Here is a description of some settings:

`REQUEST_TIMEOUT` - request timeout specified in seconds. Default: 10.

### FAQ

- Why not async?

Because the main purpose of this program to delicately check availability of the specified URls. Async requests may increase load on server and make websites unavailable.

### Roadmap

- [x] Create MVP of CLI application.
- [ ] Add interactive mode.
- [ ] Analysis of requests with errors.
- [ ] Ability to specify IP for sites (as in the `/etc/hosts` file).
