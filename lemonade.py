import cherrypy
import youtube
import json
import os

class Lemon:
    @cherrypy.expose
    def index(self):
        with open("static/index.html") as fr:
            content = fr.read()
        return content
    
    @cherrypy.expose
    def creep(self, url, kind):
        if kind == "list":
            us = youtube.delist(url)
            # ts = (youtube.creep(u) for u in us)
            us = list(us)
            max_workers = min(max(len(url)//2, 5), 15)
            ts = youtube.multi_creep(us, max_workers)
            res_ = [{"title": title, "info": list(info)} for title, info in ts]
            res = json.dumps(res_)
        elif kind == "channel":
            pass
        elif kind == "atom":
            title, info = youtube.creep(url)
            res = json.dumps({"title": title, "info": list(info)})

        return res

conf = {
    "/": {
        "tools.staticdir.root": os.path.abspath(os.getcwd())
    },
    "/static": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": "./static"
    }
}
cherrypy.quickstart(Lemon(), "/", conf)