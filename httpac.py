import urllib.request
import urllib.parse
import http.cookiejar
import re
import time

tieba_url = "http://tieba.baidu.com"
token_url = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt=1385610373352&class=login&logintype=dialogLogin&callback=bd__cbs__rh1uhg"
login_url = "https://passport.baidu.com/v2/api/?login"
btn_url = "http://tieba.baidu.com/mo/q/pv?lp=sfrs_sign_like_click_show&_t=1386048146667"
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
user_name = "winden@yeah.net"
password = "185400ab"
cookie_file = "cookie2.txt"
sign_url = "http://tieba.baidu.com/mo/q/sign"


def ReadCookie(cookie_file):
    try:
        cj = http.cookiejar.MozillaCookieJar(cookie_file)
        cj.load()
    except:
        fp = open(cookie_file,'w')
        fp.write("")
        fp.close
        cj = http.cookiejar.MozillaCookieJar(cookie_file)
    return cj

def BuildOpener(cj):
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    return opener

def BuildReq(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',user_agent)
    return req

def BuildPostdata(user_name,password,token):
    postdata = {
        "username" : user_name, 
        "password" : password,
        "staticpage" : "http://www.baidu.com/cache/user/html/v3Jump.html",
        "charset" : "UTF-8",
        "token" : token,
        "tpl" : "mn",
        "apiver" : "v3",
        "tt" : "1385610476365",
        "safeflg" : "0",
        "u" : tieba_url,
        "isPhone" : "false",
        "quick_user" : "0",
        "logintype" : "dialogLogin",
        "splogin" : "rate",
        "verifycode" : "",
        "mem_pass" : "on",
        "ppui_logintime" : "103013",
        "callback" : "parent.bd__pcbs__an5hr1",
        "connection" : "keep-alive"
    }
    postdata = urllib.parse.urlencode(postdata)
    postdata = postdata.encode('utf-8')
    return postdata

def FindFavTieba(data):
    data = data.decode('utf-8')
    fav_tiebas = re.findall('<a class="j_forumTile_wrapper forumTile_wrapper" href="(.+?)&amp',data)
    return fav_tiebas

def FindTbs(data):
    data = data.decode('utf-8')
    tbs = re.findall('"tbs" : "(\w+)"',data)[0]
    kw = re.findall('"kw" : "(.+?)"',data)[0]
    fid = re.findall('"fid" : "(\d+)"',data)[0]
    signdata = {
            'tbs': tbs,
            'is_like' : 1,
            'fid' : fid
            }
    signdata = urllib.parse.urlencode(signdata)
    signdata = '?kw='+kw+'&'+signdata
    return signdata

if __name__ == "__main__":
    fp = open("1.html",'wb')

    cj = ReadCookie(cookie_file)
    opener = BuildOpener(cj)

    req = BuildReq(tieba_url)
    data = opener.open(req)

    req = BuildReq(token_url)
    data = opener.open(req).read()
    token = re.findall('"token" : "(\w+)"',data.decode('utf-8'))[0]

    postdata = BuildPostdata(user_name,password,token)
    req = BuildReq(login_url)
    data = opener.open(req,postdata)

    req = BuildReq(tieba_url)
    data = opener.open(req).read()
    fav_tiebas = FindFavTieba(data)

    for fav_tieba in fav_tiebas:
        req = BuildReq(urllib.parse.urljoin(tieba_url,fav_tieba))
        data = opener.open(req).read()
        postdata = FindTbs(data)
        url = urllib.parse.urljoin(sign_url,postdata)
        print(url)
        req = BuildReq(url)
        data = opener.open(req).read()
        fp.write(data)
        time.sleep(2)
    cj.save()



