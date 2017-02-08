#!/usr/bin/env python3

import sys
import urllib.request


def gest_error(code):
    print("ERROR !", code, file=sys.stderr)
    exit(84)
    return

def find_uuid(name):
    url = urllib.request.urlopen("http://tools.glowingmines.eu/convertor/nick/" + name)
    tmp = str(url.read())
    res = tmp.split(",")[1].split("\"offlineuuid\":")[1].split("\"")[1]
    res = res[:8] + '-' + res[8:]
    res = res[:13] + '-' + res[13:]
    res = res[:18] + '-' + res[18:]
    res = res[:23] + '-' + res[23:]
    return (res)

try:
    f = open("whitelist.json", "r")
except:
    gest_error("file could not be read")

file_str = f.read()
lines = file_str.split("\n")

names = []
uuids = []
l = 0
while l < len(lines):
    if len(lines[l]) > 3:
        sp = lines[l].split("\"uuid\": ")
        if (len(sp) > 1):
            uuid = sp[1].split("\"")[1]
        l += 1
        sp = lines[l].split("\"name\": ")
        if (len(sp) > 1):
            name = sp[1].split("\"")[1]
            names.append(name)
            real_uuid = find_uuid(name)
            print(real_uuid)
            uuids.append(real_uuid)
    l += 1

f.close()

to_write = "[\n"
for i in range(0, len(uuids)):
    to_write += "\t{\n"
    to_write += "\t\t\"uuid\": \"" + uuids[i] + "\",\n"
    to_write += "\t\t\"name\": \"" + names[i] + "\"\n"
    if i < len(uuids) - 1:
        to_write += "\t},\n"
    else:
        to_write += "\t}\n"
to_write += "]"

try:
    f = open("whitelist.json", "w")
except:
    gest_error("file could not be read")
f.write(to_write)
f.close()