import site_checker

if __name__ == '__main__':
    print('Please, write a list of sites below. '
          'Format: site1.com site2.com site3.com')
    site_checker.checker(input().split())
