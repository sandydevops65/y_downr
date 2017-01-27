from collections import namedtuple

Headers = namedtuple("Headers", ["main", "post", "ajax", "gzip", "range"])
headers = Headers(
				  main={
		                'Upgrade-insecure-requests': '1',
		                'Accept': 'text/html,application/xhtml+xml,application/xml',
		                'User-agent': 'Mozilla/5.0 (Windows NT 6.1)'
		               },
				  post=('Content-Type', 'application/x-www-form-urlencoded'),
				  ajax=('X-Requested-With', 'XMLHttpRequest'),
				  gzip=('Accept-encoding', 'gzip, deflate'),
				  range=lambda start, end: ("Range", "bytes={}-{}".format(start, end))
				  )
