#!/usr/bin/env python
"""
 CLICOL plugin package for MAC vendor lookup

 example output:
 ...
"""
from __future__ import print_function
from __future__ import unicode_literals
import re
import os

from netaddr import *
import pudb

class MACVendor:
    loadonstart = True
    cmap = dict()
    setup = dict()
    regex = ()
    outtype = "append"
    column = 85

    def __init__(self, setup):
        (self.setup, self.cmap) = setup
        self.regex = (re.compile(self.cmap['BOS']+r"(?<![:-])\b((?:[a-fA-F0-9]{2}[:-]){5}[a-fA-F0-9]{2})\b(?![:-])", re.M),
                      re.compile(self.cmap['BOS']+r"(?<!\.)\b((?:[a-fA-F0-9]{4}\.){2}[a-fA-F0-9]{4})\b(?!\.)", re.M))

        if 'outtype' in self.setup.keys():  #  Set output type (inline|append)
            if self.setup['outtype'] in ("inline", "append"):
                self.outtype = self.setup['outtype']
        if 'column' in self.setup.keys():  #  Set column for append
            self.column = int(self.setup['column'])

    def org(self, mac=""):
        obj = EUI(mac)
        try:
            return EUI(mac).oui.registration()['org']
        except:
            return None

    def preprocess(self, input, effects=[]):
        output = input
        macdb = dict()
        macs = self.regex[0].findall(input)
        macs.extend(self.regex[1].findall(input))
        for mac in macs:
            org = self.org(mac)
            if org:
                macdb[mac]=org

        if len(macdb) == 0:
            return output

        if self.outtype == 'inline':
            for mac in macdb.keys():
                output=output.replace(mac,"%s(%s)" % (mac,macdb[mac]))
        else:
            out = ""
            #  clean regex for backspaced output on devices
            r = re.compile('[\b]+ +[\b]+(.*)', re.UNICODE)
            for line in output.splitlines(True):
                strippedline = line
                match = r.match(line)
                if match:
                    strippedline = match.group(1)
                for mac in macdb.keys():
                    if mac in line:
                        line = line.replace("\r"," %s%sMAC: %s%s\r" % (" " * (self.column-len(strippedline)),self.cmap['description'],macdb[mac],self.cmap['default']))
                out += line
            output = out

        return output

    def test(self):
        return ("plugin.macvendor", "\n postprocess:%s" % self.postprocess("""
"""))

