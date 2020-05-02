import requests
import re
import time
import logging
import platform
import os
from utility import tool
from urllib import parse
from html import unescape
import re

logger = logging.getLogger("fileLogger")

class GetVideo(object):
    @staticmethod
    def getUrl(video_url):
        header = {
            "Accept": "application/json, text/javascript, */*",
            "Origin": "https://www.clipconverter.cc",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                          "(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.clipconverter.cc/",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
            "Cookie": "_ga=GA1.2.326890702.1550755062; __test",
            "Accept-Encoding": "gzip, deflate, br"
        }
        send_data = {
            "mediaurl": "",      "filename": "",     "filetype": "",     "format": "",          "audiovol": 0,
            "audiochannel": 2,   "audiobr": 128,     "videobr": 224,     "videores": "352x288", "videoaspect": "",
            "customres": "320x240",     "timefrom-start": 1,             "timeto-end": 1,       "id3-artist": "",
            "id3-title": "",     "id3-album": "ClipConverter.cc",        "auto": 0,             "hash": "",
            "image": "",         "org-filename": "", "videoid": "",      "pattern": "",         "server": "",
            "serverinterface": "",                   "service": "",      "ref": "",             "lang": "en",
            "client_urlmap": "none",                 "ipv6": "false",     "addon_urlmap": "",    "cookie": "",
            "addon_cookie": "",  "addon_title": "",  "ablock": 1,        "clientside": 0,       "addon_page": "none",
            "verify": "",        "result": "",       "again": "",        "addon_browser": "",   "addon_version": "",
        }
        url = "https://www.clipconverter.cc/check.php"
        send_data["mediaurl"] = video_url
        # source = video_url
        # id = video_url.split("=")[1]
        s = requests.session()
        s.proxies={"http": "http://127.0.0.1:10809", "https": "http://127.0.0.1:10809"}
        s.headers.update(header)
        send = send_data.copy()
        data = s.post(url=url, data=send).json()
        send_data["verify"] = data["verify"]
        send_data["server"] = data["server"]
        send_data["serverinterface"] = data["serverinterface"]
        send_data["filename"] = data["filename"]
        send_data["filetype"] = "MP4"
        send_data["id3-artist"] = data["id3artist"]
        send_data["id3-title"] = data["id3title"]
        send_data["image"] = data["thumb"]
        send_data["org-filename"] = data["filename"]
        send_data["videoid"] = data["videoid"]
        send_data["pattern"] = data["pattern"]
        send_data["server"] = data["server"]
        send_data["serverinterface"] = data["serverinterface"]
        send_data["service"] = data["service"]
        # file_name = data["filename"]
        for i in data["url"]:
            # if "1080p" in i["text"] and "60fps" not in i["text"] or "720" in i["text"]:
            #     self.send_data["url"] = i["url"]
            #     size = re.findall("#size=(.*?)#audio", i["url"])[0]
            #     self.send_data["url"] += '|' + size
            #     break
            if "720p" in i["text"]:
                return i["url"]
        raise Exception("no url")
        # data = self.s.post(self.url, data=self.send_data).json()
        # get_check = "https://www.clipconverter.cc/convert/{}/?ajax".format(data["hash"])
        # res = requests.get(url=get_check).text
        # status_url = re.findall('statusurl = "(.*?)"', res)[0]
        # while True:
        #     data = self.s.get(url=status_url).json()
        #     error = 0
        #     try:
        #         if data["status"]["@attributes"]["step"] == "finished":
        #             download_url = data["downloadurl"].replace("http", "https")
        #             break
        #         time.sleep(4)
        #         logging.info("wait for cc finishing " + data["status"]["@attributes"]["info"])
        #     except KeyError:
        #         logging.error(res)
        #         error += 1
        #         if error > 6:
        #             raise KeyError
        # new_name = ""
        # for i in file_name:
        #     if i.isnumeric() or i.isalpha() or i.isspace():
        #         new_name += i
        # logging.info(new_name)
        # return download_url, new_name

    # def get_cover(self):
    #     url = "https://i1.ytimg.com/vi/{}/maxresdefault.jpg".format(self.id)
    #     # json_rpc("aria2.addUri", url=url, out=self.id + ".jpg")


def download(path, name, vid):
    url = "https://www.youtube.com/watch?v=" + vid
    want_quality = ["137", "298", "136", "22"]
    addition = " >nul 2>nul" if platform.system() == "Windows" else " >/dev/null 2>&1"
    ac_quality = "you-get -i {}".format(url)
    quality = os.popen(ac_quality).read()
    quality = re.findall("you-get --itag=(\\d+)", quality)
    print(quality)
    quality_get = ""
    for _ in want_quality:
        if _ in quality:
            quality_get = _
            break
    cmd = "you-get --no-caption --itag={} -o {} -O {} {} {} -x 127.0.0.1:8087".format(quality_get, path, name, url, addition)
    print(cmd)
    while os.system(cmd):
        print("test")
        time.sleep(10)

def dealURLs(urls, hd):
    rs = {}
    if hd:
        for i in urls:
            if "itag=137" in i: # 1080P
                rs["vURL"] = i
            if "itag=141" in i: # 256k
                rs["sURL"] = i
                rs["sd"] = 10
            if "itag=140" in i and rs.get("sURL", -1) < 9: # 128k
                rs["sURL"] = i
            if "itag=139" in i and rs.get("sURL", -1) < 8: # 48k
                rs["sURL"] = i
    if not hd or rs.get("vURL") is None or rs.get("sURL") is None:
        rs.pop("sURL")
        for i in urls:
            if "itag=22" in i:
                rs["vURL"] = i
            if "itag=18" in i and rs.get("vURL") is None:
                rs["vURL"] = i
    return rs

def getVideoUrl1(vid):
    url = "https://www.youtube.com/watch?v=" + vid
    header = {"Content-Type": "application/x-www-form-urlencoded", 
                "Origin": "null",
                "content-type": "application/x-www-form-urlencoded",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                }
    sess = tool.Session()
    s = sess.post("http://www.lilsubs.com/", data={"url": url}, headers=header, useProxy=True).text
    s = re.findall('target="_blank" href="(.*?)"', s)
    return s

def getVideoUrl2(vid):
    s = tool.Session()
    url = "https://www.findyoutube.net"
    s.headers.update({
        "origin": "https://www.findyoutube.net",
        "referer": "https://www.findyoutube.net/"
    })
    rs = s.get(url, useProxy=True).text
    csrf = re.findall('csrf_token" type="hidden" value="([^"]+)', rs)[0]
    post = {
        "url": "https://www.youtube.com/watch?v=" + vid,
        "proxy": "Random",
        "submit": "Download",
        "csrf_token": csrf
    }
    rs = s.post("https://www.findyoutube.net/result", data=post, useProxy=True).text
    urls = re.findall('href=(.*?) download="test.mp4">', rs)
    for i in range(len(urls)):
        urls[i] = unescape(urls[i])
    return urls

def getVideoUrl3(vid):
    s = tool.Session()
    s.headers.update({
            "Sec-Fetch-Dest": "empty",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://www.y2b.xyz",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Referer": "https://www.y2b.xyz/",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
    })
    raw = s.get("https://www.y2b.xyz/", useProxy=True).text
    csrf = re.findall('csrf_token = "([^"]+)', raw)[0]
    s.headers.update({
        "X-XSRF-TOKEN": parse.unquote(s.cookies.get_dict()["XSRF-TOKEN"]),
        "X-CSRF-TOKEN": csrf
    })
    rs = s.post("https://www.y2b.xyz/analysis", 
                json={"url":"https://www.youtube.com/watch?v={}".format(vid),"channel":"one"},
                useProxy=True)
    if rs.status_code != 200:
        return ""
    ret = []
    rs = rs.json()
    for i in rs["formats"]:
        ret.append(i["url"])

def getVideoUrl(vid):
    func = [getVideoUrl1, getVideoUrl2, getVideoUrl3]
    for i in func:
        try:
            rs = i(vid)
            if len(rs) > 0:
                return rs
        except:
            pass
    return ""

class VideoManager:
    def __init__(self, vid: str, hd: bool=False):
        self.vid: str = vid
        self._dmer1: tool.DownloadManager = None
        self._dmer2: tool.DownloadManager = None
        self._o: str = None
        self._hd: bool = hd
        self._vURL: str = None
        self._sURL: str = None
    
    def getVideo(self):
        rs = None
        for func in [getVideoUrl1, getVideoUrl2, getVideoUrl3]:
            try:
                rs = dealURLs(func(self.vid), self._hd)
                if rs.get("vURL") is not None:
                    break
            except:
                pass
        if rs is None:
            return False, ""
        parser = tool.getSettingConf()
        proxy = dict(parser.items("Proxy"))
        jsonrpc = parser.get("Aria", "jsonrpc")
        ffmpegArgs = parser.get("FFMPEG", "args")
        ffmpegPath = parser.get("FFMPEG", "path")
        cmd = ffmpegPath + " -i {} -i {} " + ffmpegArgs + " {}"
        self._dmer1 = tool.DownloadManager(rs["vURL"], proxy=proxy, jsonrpc=jsonrpc, files=self.vid + "_v")
        self._dmer1.download()
        if rs.get("sURL") is not None:
            self._dmer2 = tool.DownloadManager(rs["sURL"], proxy=proxy, jsonrpc=jsonrpc, files=self.vid + "_s")
            self._dmer2.download()
            if self._dmer2.waitForFinishing() != 1:
                return False, ""
        if self._dmer1.waitForFinishing() != 1:
            return False, ""
        
        if self._dmer2 is not None:
            _a = self._dmer2.telFileLocate()
            _v = self._dmer1.telFileLocate()
            self._o = self._dmer1.getDirs() + self.vid + "_merged.mp4"
            if os.path.exists(self._o):
                os.remove(self._o)
            if os.system(cmd.format(_a, _v, self._o)) != 0:
                return False
            return True, self._o
        else:
            return True, self._dmer1.telFileLocate()
    
    def deleteFile(self):
        self._dmer1.deleteFile()
        if self._dmer2 is not None:
            self._dmer2.deleteFile()
            os.remove(self._o)

# if __name__ == "__main__":
#     print(GetVideo.getUrl("https://www.youtube.com/watch?v=7FDyF8gVoL8"))
    # download2("bBrUrgNf5y8")
    # s = GetVideo("https://www.youtube.com/watch?v=7FDyF8gVoL8")
    # print(s.first())