#!/usr/bin/env python3
# Copyright (c) 2018-2019 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test the deriveaddresses rpc call."""
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal

class ValidateaddressTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1

    def run_test(self):
        # Valid address
        address = "bcrt1q049ldschfnwystcqnsvyfpj23mpsg3jcedq9xv"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], True)
        assert 'error' not in res
        assert 'error_index' not in res

        # Valid capitalised address
        address = "BCRT1QPLMTZKC2XHARPPZDLNPAQL78RSHJ68U33RAH7R"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], True)
        assert 'error' not in res
        assert 'error_index' not in res

        # Invalid address without type specified
        address = "bcrtq049ldschfnwystcqnsvyfpj23mpsg3jcedq9xv"
        res = self.nodes[0].validateaddress(address)
        assert_equal(res['isvalid'], False)
        assert_equal(res['error'], "Invalid Base58 character in address")
        assert 'error_index' not in res

        # Address with no '1' separator
        address = "bcrtq049ldschfnwystcqnsvyfpj23mpsg3jcedq9xv"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error_index'], 0)
        assert_equal(res['error'], "Missing separator")

        # Address with no HRP
        address = "1q049ldschfnwystcqnsvyfpj23mpsg3jcedq9xv"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error_index'], 0)
        assert_equal(res['error'], "Invalid separator position")

        # Address with an invalid bech32 encoding character
        address = "bcrt1q04oldschfnwystcqnsvyfpj23mpsg3jcedq9xv"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error_index'], 8)
        assert_equal(res['error'], "Invalid Base 32 character")

        # Address with one error
        address = "bcrt1q049edschfnwystcqnsvyfpj23mpsg3jcedq9xv"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error_index'], 9)
        assert_equal(res['error'], "Invalid")

        # Address with one error, without type specified
        address = "bcrt1q049edschfnwystcqnsvyfpj23mpsg3jcedq9xv"
        res = self.nodes[0].validateaddress(address)
        assert_equal(res['isvalid'], False)
        assert_equal(res['error_index'], 9)
        assert_equal(res['error'], "Invalid")

        # Capitalised address with one error
        address = "BCRT1QPLMTZKC2XHARPPZDLNPAQL78RSHJ68U32RAH7R"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error_index'], 38)
        assert_equal(res['error'], "Invalid")

        # Valid multisig address
        address = "bcrt1qdg3myrgvzw7ml9q0ejxhlkyxm7vl9r56yzkfgvzclrf4hkpx9yfqhpsuks"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], True)

        # Multisig address with 2 errors
        address = "bcrt1qdg3myrgvzw7ml8q0ejxhlkyxn7vl9r56yzkfgvzclrf4hkpx9yfqhpsuks"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error_index'], 19)
        assert_equal(res['error'], "Invalid")

        # Address with 2 errors
        address = "bcrt1qfsawymtaadjet5sl7p9zw273wpvu9rgwq93y52"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error_index'], 22)
        assert_equal(res['error'], "Invalid")

        # Invalid but also too long
        address = "bcrt1q049edschfnwystcqnsvyfpj23mpsg3jcedq9xv049edschfnwystcqnsvyfpj23mpsg3jcedq9xv049edschfnwystcqnsvyfpj23m"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error_index'], 90)
        assert_equal(res['error'], "String too long")

        # Legacy address with no errors
        address = "muehQnn2P5NiiRCGg9HewAWrXLRy2d7TZE"
        res = self.nodes[0].validateaddress(address, "legacy")
        assert_equal(res['isvalid'], True)

        # Legacy address with one error
        address = "muehQnn2P5NhiRCGg9HewAWrXLRy2d7TZE"
        res = self.nodes[0].validateaddress(address, "legacy")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error'], "Invalid checksum for Base58 address")
        assert 'error_index' not in res

        # Legacy address with one error, without type specified
        address = "muehQnn2P5NhiRCGg9HewAWrXLRy2d7TZE"
        res = self.nodes[0].validateaddress(address)
        assert_equal(res['isvalid'], False)
        assert_equal(res['error'], "Invalid checksum for Base58 address")
        assert 'error_index' not in res

        # Legacy address with a non-Base58 character
        address = "muehQnn2P5NiiRCGO9HewAWrXLRy2d7TZE"
        res = self.nodes[0].validateaddress(address, "legacy")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error'], "Invalid Base58 character in address")

        # Legacy address with incorrect prefix for current network
        address = "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"
        res = self.nodes[0].validateaddress(address, "legacy")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error'], "Invalid prefix for Base58 address")

        # Bech32 address with incorrect HRP for current network
        address = "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"
        res = self.nodes[0].validateaddress(address, "bech32")
        assert_equal(res['isvalid'], False)
        assert_equal(res['error'], "Invalid HRP for Bech32 address")
        assert_equal(res['error_index'], 0)


if __name__ == '__main__':
    ValidateaddressTest().main()
