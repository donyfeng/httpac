import urllib.request
import urllib.parse
import http.cookiejar
import re

tieba_url = "http://tieba.baidu.com"
token_url = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt=1385610373352&class=login&logintype=dialogLogin&callback=bd__cbs__rh1uhg"
login_url = "https://passport.baidu.com/v2/api/?login"
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
user_name = "donyfeng@outlook.com"
password = "185400"
cookie_file = "cookie.txt"

#read cookie. if no cookie file created, make one.
try:
    cj = http.cookiejar.MozillaCookieJar(cookie_file)
    cj.load()
except:
    fp = open(cookie_file,'w')
    fp.write("")
    fp.close
    cj = http.cookiejar.MozillaCookieJar(cookie_file)
    
#open html file 
fp = open("test.html",'wb')

#build a opener with cookie handling.
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

#Open tieba url to get cookies.
req = urllib.request.Request(tieba_url)
req.add_header('User-Agent',user_agent)
resp = opener.open(req)

#open token url to get token.
req = urllib.request.Request(token_url)
req.add_header('User-Agent',user_agent)
data = opener.open(req).read()

token = re.findall('"token" : "(\w+)"',data.decode('utf-8'))[0]

#post login data to login url.
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

req = urllib.request.Request(login_url)
req.add_header('User-Agent',user_agent)
resp = opener.open(req,postdata)

#Open tieba url to get favor tiebas
req = urllib.request.Request(tieba_url)
req.add_header('User-Agent',user_agent)
data = opener.open(req).read()
fp.write(data)

data = data.decode('utf-8')
fav_tiebas = re.findall('<a class="j_forumTile_wrapper forumTile_wrapper" href="(.+?)">',data)

#surf the fave tieba and sign

fav_tieba_url = urllib.parse.urljoin(tieba_url,fav_tiebas[3])
fav_tieba_url = re.sub(';','&',fav_tieba_url)

req = urllib.request.Request(fav_tieba_url)
req.add_header('User-Agent',user_agent)
data = opener.open(req).read()
data = data.decode('utf-8')

tbs = re.findall('"tbs" : "(\w+)"',data)[0]
kw = re.findall('"kw" : "(.+?)"',data)[0]
fid = re.findall('"fid" : "(\d+)"',data)[0]
signdata = {
        'tbs': tbs,
        'kw' : kw,
        'is_like' : 1,
        'fid' : fid
}
signdata = urllib.parse.urlencode(signdata,'gbk')

sign_url = "http://tieba.baidu.com/mo/q/sign?"
req = urllib.request.Request(sign_url+signdata)
req.add_header('User-Agent',user_agent)
req.add_header('Referer',fav_tieba_url)
data = opener.open(req).read()

req = urllib.request.Request(fav_tieba_url)
req.add_header('User-Agent',user_agent)
data = opener.open(req).read()

#save final html file and cookie
cj.save()
