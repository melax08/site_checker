import site_checker

print('Please, write a list of sites below. Format: site1.com site2.com site3.com')
sites_list = input().split()

site_checker.checker(sites_list)