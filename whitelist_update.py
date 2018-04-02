#!/usr/bin/env python3

import sys
import urllib.request

if len(sys.argv) <= 1:
    updateAll = True
else:
    if (sys.argv[1] == "-h"):
        print("USAGE :")
        print("\t./whitelist [pseudonyme]")
        print("° pseudonyme is the pseudonyme you want to add to the whitelist with the correct uuid.")
        print("° Don't pass any argument if you need to update the full uuid list.")
        print("° The whitelis.json file should be in the same directory as the script file.")
        exit(0)
    updateAll = False
    toAdd = sys.argv[1]

def gest_error(code):
    print("ERROR !", code, file=sys.stderr)
    exit(84)
    return

def find_uuid(name):
    try:
        url = urllib.request.urlopen("http://tools.glowingmines.eu/convertor/nick/" + name)
        tmp = str(url.read())
        res = tmp.split(",")[1].split("\"offlineuuid\":")[1].split("\"")[1]
        res = res[:8] + '-' + res[8:]
        res = res[:13] + '-' + res[13:]
        res = res[:18] + '-' + res[18:]
        res = res[:23] + '-' + res[23:]
    except:
        return (None)
    return (res)

try:
    f = open("whitelist.json", "r")
except:
    gest_error("file could not be read")

try:
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
                real_uuid = find_uuid(name) if updateAll else uuid
                if real_uuid == None:
                    print("could not read uuid for "+ name)
                    uuids.append(uuid)
                else:
                    if updateAll:
                        print(real_uuid + " : " + name)
                    uuids.append(real_uuid)
        l += 1
    if (not(updateAll)):
        names.append(toAdd)
        uuids.append(find_uuid(toAdd))
except:
    gest_error("failed to load file")

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
    f.write(to_write)
    f.close()
except:
    gest_error("file could not be overwritten")

print("Done.")
