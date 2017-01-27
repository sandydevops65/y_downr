from www_access import urlopen, request, parse, re
from www_header import headers
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip

title_pat = re.compile(r"<title>\n?(.*?)\n?</title>")
page_pat = re.compile(r'"url_encoded_fmt_stream_map":"(.*?)"')
list_pat = re.compile(r'<a class="pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link ".*?href="(.*?)".*?>')
base_url = "https://youtube.com"
qual_map = {"small": "240p", "medium": "360p", "hd720": "720p", "large": "1080p"}

def gen_info(match, title):
    ds = (dict(parse.parse_qsl(m)) for m in match.group(1).split(","))
    for i,d in enumerate(ds):
        quality = qual_map[d["quality"]]
        fmt = d["type"].split(";")[0].split("/")[-1]
        url = d["url"] + "&" + parse.urlencode({"title": title})
        yield (quality, fmt, url)

def creep(url):
    url = parse.urljoin(base_url, url)
    req = request(url)
    req.add_header(*headers.gzip)
    res = urlopen(req)
    if res:
        data = res.read()
        html = gzip.decompress(data).decode("unicode_escape")
        title = title_pat.search(html).group(1)
        match = page_pat.search(html)
        info = gen_info(match, title) if match else []
    else:
        title, info = (None, [])

    return title, info

def delist(url):
    url = parse.urljoin(base_url, url)
    req = request(url)
    res = urlopen(req)
    if res:
        html = res.read().decode("unicode_escape")
        matches = list_pat.finditer(html)
        return (match.group(1) for match in matches)

def multi_creep_as(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_url = {executor.submit(creep, url): url for url in urls}
        for future in as_completed(future_url):
            try:
                data = future.result()
            except Exception as e:
                print(e)
            else:
                yield data

def multi_creep(urls, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for data in executor.map(creep, urls):
            yield data




    