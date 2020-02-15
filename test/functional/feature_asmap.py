#!/usr/bin/env python3
# Copyright (c) 2020 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test asmap config argument for ASN-based IP bucketing.

Verify node behaviour and debug log when launching bitcoind in these cases:

1. `bitcoind` with no -asmap arg, using /16 prefix for IP bucketing

2. `bitcoind -asmap=<absolute path>`, using the unit test skeleton asmap

3. `bitcoind -asmap=<relative path>`, using the unit test skeleton asmap

4. `bitcoind -asmap/-asmap=` with no file specified, using the default asmap

5. `bitcoind -asmap` with no file specified and a missing default asmap file

6. `bitcoind -asmap` with an empty (unparsable) default asmap file

The tests are order-independent.

"""
import os
import shutil

from test_framework.test_framework import BitcoinTestFramework

DEFAULT_ASMAP_FILENAME = 'ip_asn.map' # defined in src/init.cpp
VERSION = 'fec61fa21a9f46f3b17bdcd660d7f4cd90b966aad3aec593c99b35f0aca15853'

def expected_messages(filename):
    return ['Opened asmap file "{}" (59 bytes) from disk'.format(filename),
            'Using asmap version {} for IP bucketing'.format(VERSION)]

class AsmapTest(BitcoinTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = False
        self.num_nodes = 1

    def test_without_asmap_arg(self):
        self.log.info('Test bitcoind with no -asmap arg passed')
        self.stop_node(0)
        with self.node.assert_debug_log(['Using /16 prefix for IP bucketing']):
            self.start_node(0)

    def test_asmap_with_absolute_path(self):
        self.log.info('Test bitcoind -asmap=<absolute path>')
        self.stop_node(0)
        filename = os.path.join(self.datadir, 'my-map-file.map')
        shutil.copyfile(self.asmap_raw, filename)
        with self.node.assert_debug_log(expected_messages(filename)):
            self.start_node(0, ['-asmap={}'.format(filename)])
        os.remove(filename)

    def test_asmap_with_relative_path(self):
        self.log.info('Test bitcoind -asmap=<relative path>')
        self.stop_node(0)
        name = 'ASN_map'
        filename = os.path.join(self.datadir, name)
        shutil.copyfile(self.asmap_raw, filename)
        with self.node.assert_debug_log(expected_messages(filename)):
            self.start_node(0, ['-asmap={}'.format(name)])
        os.remove(filename)

    def test_default_asmap(self):
        shutil.copyfile(self.asmap_raw, self.default_asmap)
        for arg in ['-asmap', '-asmap=']:
            self.log.info('Test bitcoind {} (using default map file)'.format(arg))
            self.stop_node(0)
            with self.node.assert_debug_log(expected_messages(self.default_asmap)):
                self.start_node(0, [arg])
        os.remove(self.default_asmap)

    def test_default_asmap_with_missing_file(self):
        self.log.info('Test bitcoind -asmap with missing default map file')
        self.stop_node(0)
        msg = "Error: Could not find asmap file \"{}\"".format(self.default_asmap)
        self.node.assert_start_raises_init_error(extra_args=['-asmap'], expected_msg=msg)

    def test_empty_asmap(self):
        self.log.info('Test bitcoind -asmap with empty map file')
        self.stop_node(0)
        with open(self.default_asmap, "w", encoding="utf-8") as f:
            f.write("")
        msg = "Error: Could not parse asmap file \"{}\"".format(self.default_asmap)
        self.node.assert_start_raises_init_error(extra_args=['-asmap'], expected_msg=msg)
        os.remove(self.default_asmap)

    def run_test(self):
        self.node = self.nodes[0]
        self.datadir = os.path.join(self.node.datadir, self.chain)
        self.default_asmap = os.path.join(self.datadir, DEFAULT_ASMAP_FILENAME)
        self.asmap_raw = os.path.join(self.datadir, "test-asmap.raw")
        with open(self.asmap_raw, "wb") as f:
            f.write(b"\xfb\x03\xec\x0f\xb0\x3f\xc0\xfe\x00\xfb\x03\xec\x0f\xb0\x3f\xc0\xfe\x00\xfb\x03\xec\x0f\xb0\xff\xff\xfe\xff\xed\xb0\xff\xd4\x86\xe6\x28\x29\x00\x00\x40\x00\x00\x40\x00\x40\x99\x01\x00\x80\x01\x80\x04\x00\x00\x05\x00\x06\x00\x1c\xf0\x39")

        self.test_without_asmap_arg()
        self.test_asmap_with_absolute_path()
        self.test_asmap_with_relative_path()
        self.test_default_asmap()
        self.test_default_asmap_with_missing_file()
        self.test_empty_asmap()


if __name__ == '__main__':
    AsmapTest().main()
