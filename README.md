# Script for checking the work of migrated sites
The script is used to check the operability of the migrated sites and is especially useful if there are a large number of sites and manually checking these sites will take a long time.

site_checker.py - main script. Allows you to check the operation of sites from the list that you must specify in advance in the list_sites.txt file.
fast_checker.py - script that uses functions from site_checker.py, but you don't have to specify the list of sites in advance. The list of sites is specified while the program is running.

How to use?
site_checker.py:
1. Write a list of sites to a file list_sites.txt.
2. By analogy with the sites that already in this list