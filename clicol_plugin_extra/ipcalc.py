#!/usr/bin/env python
"""
 CLICOL plugin package for IP calculator

 example output:
 ...
"""
from __future__ import print_function
from __future__ import unicode_literals
from builtins import input
from netaddr import IPNetwork, IPAddress


class IPCalc:
    loadonstart = True
    cmap = dict()
    setup = dict()
    regex = ()
    __IPCALC_KEY = 'I'
    keybinds = (__IPCALC_KEY)

    def __init__(self, setup):
        (self.setup, self.cmap) = setup

    @staticmethod
    def showip(ip):
        output = ""
        output += "ipaddress:\t%s\r\n" % ip.ip
        output += "network/nm:\t%s\r\n" % ip.cidr
        output += "prefixlen:\t%s\r\n" % ip.prefixlen
        output += "netmask:\t%s\r\n" % ip.netmask
        if ip.version == 4:
            output += "wildcard:\t%s\r\n" % IPAddress(IPNetwork('255.255.255.255').value - ip.netmask.value)
        output += "network:\t%s\r\n" % ip.network
        output += "broadcast:\t%s\r\n" % ip.broadcast
        if len(ip) <= 2:
            output += "number of ips:\t%s\r\n" % len(ip)
        else:
            output += "number of ips:\t%s - 2 = %s\r\n" % (len(ip), len(ip) - 2)
        output += "first host:\t%s\r\n" % IPAddress(ip.first)
        output += "last host:\t%s\r\n" % IPAddress(ip.last)

        return output

    def plugin_command(self, cmd):
        if cmd == self.__IPCALC_KEY:
            str = input("\r" + " " * 100 + "\rIP: ")
            #  Support 10.0.0.0 255.255.0.0 format
            str = str.replace(" ", "/")
            print(self.showip(IPNetwork(str)))

    def plugin_help(self, command):
        if command == self.__IPCALC_KEY:
            return " Start IP calculator"
        else:
            return ""

    def plugin_test(self):
        ip = IPNetwork('192.168.0.2/27')
        return "plugin.ipcalc", "\n command(%s):%s" % \
               (self.__IPCALC_KEY, " ipcalc 192.168.0.2/27:\r\n" + self.showip(ip))
