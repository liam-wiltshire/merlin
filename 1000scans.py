#!/usr/bin/env python
import re
import os
from Hooks.scans.parser import parse
from time import sleep
import gc

scanre=re.compile("https?://[^/]+/(?:showscan|waves).pl\?scan_id=([0-9a-zA-Z]+)")
i=0

with open("1000scans.txt") as f:
    for x in f:
        i+=1
        print "Processing scan %d..." % (i)
        scanid = scanre.match(x).group(1)
        parse(1, "scan", scanid).start()
        sleep(1)
        gc.collect()


os.remove("1000scans.txt");
print "Done."
