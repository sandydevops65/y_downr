import urllib.request
import urllib.parse as parse
from http.cookiejar import CookieJar
import re
import gzip
from www_header import headers 

def urlopen(req):
	try:
		res = urllib.request.urlopen(req)
	except Exception as e:
		# print(e)
		res = None
	return res

request = lambda url: urllib.request.Request(url, headers=headers.main)
