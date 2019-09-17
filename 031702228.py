# encoding=utf-8
import re
import json
import time
import jieba
import requests
import json
#1!张三,福建福州闽13599622362侯县上街镇福州大学10#111.

s0 = input()
#print(s0[:1])
#匹配等级

level = s0[0]
print(level)
s1 = s0[1:]

#匹配姓名

t2 = time.time()
rout = re.search(r'!(.+?),', s1)
name = rout.group()
pos = rout.span()
name = name[1:-1]
s2 = s1[pos[1]:]

#匹配手机号

rp = re.search(r'\d{11}', s2)
telnumber = rp.group()
pos = rp.span()
print(pos)
s3 = s2[0:pos[0]] + s2[pos[1]:]
print(s3)

#seg_list = jieba.cut(s3, cut_all=False)
#print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

#地址划分 gd的api

url = "https://restapi.amap.com/v3/geocode/geo?key=891fc6769c45ed042ef6729dde41fb28"


u = url + "&address=" + s3

wb = requests.get(u).text
content = json.loads(wb)
#soup = BeautifulSoup(wb)
print(content)
#print(content["geocodes"])
positon = content["geocodes"][0]["location"]
rurl = "https://restapi.amap.com/v3/geocode/regeo?output=JSON&key=891fc6769c45ed042ef6729dde41fb28&radius=100&extensions=base"

ru = rurl + "&location=" + positon

respond = requests.get(ru).text
respond = json.loads(respond)
print(respond)
if level == "1":
    #township doornumber
    city = content["geocodes"][0]["city"]
    township = respond["regeocode"]["addressComponent"]["township"]
    rt = re.search(r"." + township, s3)
    district = content["geocodes"][0]["district"]

    if city == '':
        city = content["geocodes"][0]["province"]
    if rt == None:
          township = ''
          rdt = re.search(r"." + district, s3)
          if rdt == None:
              district = ''
              rc = re.search(r"." + city, s3)
              tpos = rc.span()
          else:
              tpos = rdt.span()
    else:
        tpos = rt.span()
    s4 = s3[tpos[1]:-1]
    imformation = {

        "姓名": name,
        "手机": telnumber,
        "地址": [

            content["geocodes"][0]["province"],
            city,
            district,
            township,
            s4
        ]
    }

else:
    district = content["geocodes"][0]["district"]
    city = content["geocodes"][0]["city"]
    township = respond["regeocode"]["addressComponent"]["township"]
    rd = re.search(r'\d+号', s3)
    road = respond["regeocode"]["addressComponent"]["streetNumber"]["street"]
    rt = re.search(r"." + township, s3)
    if rt == None:
        township = ''
    if city == '':
        city = content["geocodes"][0]["province"]
    if rd == None:
        doornumber = ''
        road = ''
        if rt == None:
            township = ''
            rdt = re.search(r"." + district, s3)
            if rdt == None:
                district = ''
                rc = re.search(r"." + city, s3)
                dpos = rc.span()
            else:
                dpos = rdt.span()

        else:
            dpos = rt.span()
    else:
        doornumber = rd.group()
        dpos = rd.span()
    s4 = s3[dpos[1]:-1]




    imformation = {

        "姓名": name,
        "手机": telnumber,
        "地址": [

            content["geocodes"][0]["province"],
            city,
            district,
            township,
            road,
            doornumber,
            s4
        ]
    }

jdata = json.dumps(imformation, ensure_ascii=False)
print(jdata)

#1!张三,福建福州闽13599622362侯县上街镇福州大学10#111.
