import os
import json
import argparse
import requests
from fucker import Fucker
from logger import logger
from ObjDict import ObjDict
from utils import getConfigPath, getRealPath, versionCmp

DEFAULT_CONFIG = {
    "username": "",
    "password": "",
    "proxies": {},
    "logLevel": "INFO"
}
# get config or create one if not exist
if os.path.isfile(getConfigPath()):
    with open(getConfigPath(), 'r') as f:
        config = ObjDict(json.load(f))
else:
    config = ObjDict(DEFAULT_CONFIG)
    with open(getConfigPath(), 'w') as f:
        json.dump(config, f)

# parse auguments
parser = argparse.ArgumentParser(prog="ZHS Fucker")
parser.add_argument("-c", "--course", type=str, required=True, help="CourseId or recruitAndCourseId, can be found in URL")
parser.add_argument("-v", "--videos", type=str, nargs="+", help="Video IDs(fileId), can be found in URL, won't work if -c is recruitAndCourseId")
parser.add_argument("-u", "--username", type=str, help="if not set anywhere, will be prompted")
parser.add_argument("-p", "--password", type=str, help="If not set anywhere, will be prompted. Be careful, it will be stored history")
parser.add_argument("-s", "--speed", type=float, help="Video Play Speed")
parser.add_argument("-t", "--threshold", type=float, help="Video End Threshold, above this will be considered finished, overloaded when there are questions left unanswered")
parser.add_argument("-l", "--limit", type=int, help="Time Limit (in minutes, 0 for no limit), default is 0")
parser.add_argument("-d", "--debug", action="store_true", help="Debug Mode")
parser.add_argument("--proxy", type=str, help="HTTP Proxy Server, e.g: http://127.0.0.1:8080")

args = parser.parse_args()

logger.setLevel("DEBUG" if args.debug else config.logLevel)
username = args.username or config.username
password = args.password or config.password
proxies = config.proxies
if args.proxy:
    match args.proxy.split("://")[0].lower():
        case "http"|"https":
            proxies["http"] = args.proxy
            proxies["https"] = args.proxy
        case "socks4":
            proxies["socks4"] = args.proxy
        case "socks5":
            proxies["socks5"] = args.proxy
        case _:
            raise ValueError("Unsupported proxy type or invalid proxy URL")

# check update
with open(getRealPath("meta.json"), "r") as f:
    try:
        j = ObjDict(json.load(f))
        url = f"https://raw.githubusercontent.com/VermiIIi0n/fuckZHS/{j.branch}/meta.json"
        r = ObjDict(requests.get(url).json())
        current = j.version
        latest = r.version
        if versionCmp(current, latest) < 0:
            print("*********************************\n"+
                f"New version available: {latest}\n"+
                f"Current version: {current}\n"+
                "*********************************\n")
    except Exception:
        pass


fucker = Fucker(proxies=proxies, speed=args.speed, end_thre=args.threshold, limit=args.limit or 0) # create an instance, now we are talking... or fucking

# first you need to login to get cookies
fucker.login(username, password)
# if you cannot use selenium, you can add cookies manually by setting cookies property of Fucker
# notice that cookies of zhihuishu.com expires if you login again in other browser session
# fucker.cookies = {}

# auto detect mode
if args.videos:
    for v in args.videos:
        print(f"fucking {v}")
        fucker.fuckVideo(course_id=args.course, file_id=v)
else:
    fucker.fuckCourse(course_id=args.course)
# use fuckCourse method to fuck the entire course
# fucker.fuckCourse(course_id="")

# or if you want to fuck a video, use fuckVideo method
# fucker.fuckVideo(course_id="", file_id="")

# check the source code or README to find more info
