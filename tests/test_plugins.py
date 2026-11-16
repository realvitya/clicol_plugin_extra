import unittest
from socket import gaierror

from netaddr import IPNetwork
from clicol._compat import iter_entry_points
from clicol_plugin_extra import dnsresolve
from clicol_plugin_extra.dnsresolve import DNSresolve
from clicol_plugin_extra.ipcalc import IPCalc
from clicol_plugin_extra.macvendor import MACVendor


class ExtraPluginTests(unittest.TestCase):
    def test_installed_entry_points(self):
        points = dict((point.name, point) for point in iter_entry_points('clicol.plugins'))
        for name, plugin in (('DNSresolve', DNSresolve), ('IPCalc', IPCalc), ('MACVendor', MACVendor)):
            self.assertIs(points[name].load(), plugin)

    def test_ipv4_network(self):
        output = IPCalc.showip(IPNetwork('192.168.0.2/27'))
        self.assertIn('number of ips:\t32 - 2 = 30', output)
        self.assertIn('first host:\t192.168.0.1', output)
        self.assertIn('last host:\t192.168.0.30', output)

    def test_single_address_and_point_to_point(self):
        for network, size in (('192.0.2.1/32', 1), ('192.0.2.0/31', 2)):
            self.assertIn('number of ips:\t%s\r\n' % size, IPCalc.showip(IPNetwork(network)))

    def test_large_ipv6_network(self):
        output = IPCalc.showip(IPNetwork('2001:db8::/64'))
        self.assertIn('number of ips:\t18446744073709551616 - 2 = 18446744073709551614', output)
        self.assertIn('first host:\t2001:db8::1', output)

    def test_mac_vendor_lookup_and_formatting(self):
        colors = {'BOS': r'(?:\b)', 'description': '', 'default': ''}
        plugin = MACVendor(({'outtype': 'inline'}, colors))
        output = plugin.plugin_preprocess('9cf4.8ee4.f398')
        self.assertIn('Apple', output)
        self.assertIsNone(plugin.org('not-a-mac'))

    def test_dns_lookup_without_network(self):
        original = dnsresolve.gethostbyaddr
        try:
            dnsresolve.gethostbyaddr = lambda name: ('example.test', [], ['192.0.2.1'])
            self.assertIn('example.test', DNSresolve.resolve('192.0.2.1'))
            self.assertEqual(DNSresolve.resolve(' '), '')

            def unknown(name):
                raise gaierror('Unknown host')

            dnsresolve.gethostbyaddr = unknown
            self.assertEqual(DNSresolve.resolve('unknown.test'), 'Host/IP unknown')
        finally:
            dnsresolve.gethostbyaddr = original


if __name__ == '__main__':
    unittest.main()
