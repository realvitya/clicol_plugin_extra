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

    def __init__(self, setup):
        (self.setup, self.cmap) = setup
        self.regex = (re.compile(self.cmap['BOS']+r"(?<![:-])\b((?:[a-fA-F0-9]{2}[:-]){5}[a-fA-F0-9]{2})\b(?![:-])", re.M),
                      re.compile(self.cmap['BOS']+r"(?<!\.)\b((?:[a-fA-F0-9]{4}\.){2}[a-fA-F0-9]{4})\b(?!\.)", re.M))

        if 'outtype' in self.setup.keys():  #  Set output type (inline|append)
            if self.setup['outtype'] in ("inline", "append"):
                self.outtype = self.setup['outtype']

    def org(self, mac=""):
        #pudb.set_trace()
        obj = EUI(mac)
        try:
            return EUI(mac).oui.registration()['org']
        except:
            return None
        """
            for AS in aspath.group(3).split():
                if AS in self.db.keys():
                    aslist += "%s(%s%s%s) " % (AS, self.cmap['important_value'], self.db[AS], self.cmap['default'])
                else:
                    aslist += "%s " % AS
            return "%s%s %s%s%s" % (aspath.group(1), aspath.group(2), aslist.rstrip(), aspath.group(4), aspath.group(5))
        """
    def preprocess(self, input, effects=[]):
        #pudb.set_trace()
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
            #pudb.set_trace()
            for line in output.splitlines(True):
                for mac in macdb.keys():
                    if mac in line:
                        #  need to fix tabbing by checking line length
                        line = line.replace("\r","\t%sMAC: %s\r" % ("\t" * ((81-len(line.lstrip('\b ')))//8),macdb[mac]))
                out += line
            output = out

        return output

    def test(self):
        return ("plugin.macvendor", "\n postprocess:%s" % self.postprocess("""
"""))

