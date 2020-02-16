0.19.1 Release Notes
===============================

Bitcoin Knots version *0.19.1.knots20200215* is now available from:

  <https://bitcoinknots.org/files/0.19.x/0.19.1.knots20200215/>

This release includes new features, various bug fixes and performance
improvements, as well as updated translations.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/bitcoinknots/bitcoin/issues>

To receive security and update notifications, please subscribe to:

  <https://bitcoinknots.org/list/announcements/join/>

How to Upgrade
==============

If you are running an older version, shut it down. Wait until it has completely
shut down (which might take a few minutes for older versions), then run the
installer (on Windows) or just copy over `/Applications/Bitcoin-Qt` (on Mac)
or `bitcoind`/`bitcoin-qt` (on Linux).

Upgrading directly from a version of Bitcoin Knots that has reached its EOL is
possible, but it might take some time if the datadir needs to be migrated. Old
wallet versions of Bitcoin Knots are generally supported.

Compatibility
==============

Bitcoin Knots is supported on operating systems using the Linux kernel,
macOS 10.10+, and Windows 7 and newer. It is not recommended to use
Bitcoin Knots on unsupported systems.

From Bitcoin Knots 0.17.0 onwards, macOS versions earlier than 10.10 are no
longer supported, as Bitcoin Knots is now built using Qt 5.9.x which requires
macOS 10.10+. Additionally, Bitcoin Knots does not yet change appearance when
macOS "dark mode" is activated.

Users running macOS Catalina may need to "right-click" and then choose "Open"
to open the Bitcoin Knots .dmg. This is due to new signing requirements
imposed by Apple, which the Bitcoin Knots project does not implement.

Notable changes
===============

New RPC
-------

- `getgeneralinfo` is an experimental method to give you the client version as
  a string, the user-agent string, data directory, blocks directory, and time
  the node started.

Updated RPC
-----------

- The `createmultisig` and `addmultisigaddress` methods will now return an
  output descriptor (in addition to what they already returned previously).

- If the new IP->AS map support is enabled (by loading a map file), the
  `getpeerinfo` method will include a "mapped_as" key with the AS number for
  the peer's IP.

GUI changes
-----------

- Additional support for manipulating PSBTs, including fee bumping and a new
  "PSBT Operations" dialog, have been added.

- When entering a slightly-wrong Bech32 address, the first incorrect character
  will be distinguished in an underlined, bold, yellow colour.

PSBT (BIP174) change
--------------------

- Support for serialization of the `GLOBAL_XPUB` field has been added.

P2P changes
-----------

- Experimental support for using IP->AS map files (not included) in peer
  selection to mitigate the Erebus attack and similar threats. To load a map
  file, use the new `-asmap` option.

- If Tor is installed system-wide, but not running or accessible, Bitcoin Knots
  will run its own private instance for incoming connections over Tor only
  (including pairing with wallets). If you don't want Knots to communicate over
  Tor for some reason, you can disable this with the `-torexecute=0` option.
  In that case, we would appreciate if you report your reasons for not wanting
  this enabled to the PR for Bitcoin Core here:
      https://github.com/bitcoin/bitcoin/pull/15421

0.19.1 change log
=================

Detailed release notes follow. This overview includes changes that affect
behavior, not code moves, refactors and string updates. Changes specific to
Bitcoin Knots (beyond Core) are flagged with an asterisk ('*') before the
description.

### Consensus
- n/a    *Update chain params and add a new checkpoint at block 617,056 (luke-jr)

### P2P protocol and network code
- #16702 *supplying and using asmap to improve IP bucketing in addrman (naumenkogs, sipa)
- #18023 *Fix some asmap issues (sipa)
- #17812 *asmap functional tests and feature refinements (jonatack)
- #15421 *torcontrol: Launch a private Tor instance when not already running (luke-jr)

### Wallet
- #16963 Fix `unique_ptr` usage in boost::signals2 (promag)
- #17924 Bug: IsUsedDestination shouldn't use key id as script id for ScriptHash (instagibbs)
- #17843 Reset reused transactions cache (fjahr)

### RPC and other APIs
- #17687 cli: Fix fatal leveldb error when specifying -blockfilterindex=basic twice (brakmic)
- #17445 zmq: Fix due to invalid argument and multiple notifiers (promag)
- #17156 psbt: check that various indexes and amounts are within bounds (achow101)
- #16463 *psbt: Implement serialization support for GLOBAL_XPUB field (achow101)
- #17958 *implement getgeneralinfo (brakmic)
- #18032 *Output a descriptor in createmultisig and addmultisigaddress (achow101)

### GUI
- #17695 disable File-\>CreateWallet during startup (fanquake)
- #17634 Fix comparison function signature (hebasto)
- #18062 Fix unintialized WalletView::progressDialog (promag)
- #18123 *Fix race in WalletModel::pollBalanceChanged (ryanofsky)
- #17492 *bump fee returns PSBT on clipboard for watchonly-only wallets (fanquake)
- #17509 *save and load PSBT (Sjors)
- #18027 *"PSBT Operations" dialog (gwillen)
- #17955 *Paste button in Open URI dialog (emilengler)
- #17998 *Shortcut to close ModalOverlay (emilengler)
- #18121 *Throttle GUI update pace when -reindex (hebasto)
- #18133 *Fix various edge case bugs in QValidatedLineEdit (luke-jr)
- n/a    *Point out position of invalid characters in Bech32 addresses (luke-jr)

### Tests and QA
- #17416 Appveyor improvement - text file for vcpkg package list (sipsorcery)
- #17488 fix "bitcoind already running" warnings on macOS (fanquake)
- #17980 add missing #include to fix compiler errors (kallewoof)

### Platform support
- #17736 Update msvc build for Visual Studio 2019 v16.4 (sipsorcery)
- #17364 Updates to appveyor config for VS2019 and Qt5.9.8 + msvc project fixes (sipsorcery)
- #17887 bug-fix macos: give free bytes to `F_PREALLOCATE` (kallewoof)

### Miscellaneous
- #17897 init: Stop indexes on shutdown after ChainStateFlushed callback (jimpo)
- #17857 scripts: Fix symbol-check & security-check argument passing (fanquake)
- #18100 Update univalue subtree (MarcoFalke)
- #17916 *windows: Enable heap terminate-on-corruption (fanquake)
- #18014 *Optimized siphash implementation (elichai)

Credits
=======

Thanks to everyone who directly contributed to this release:

- Aaron Clauson
- Andrew Chow
- Elichai Turkel
- Emil Engler
- Fabian Jahr
- fanquake
- Gleb Naumenko
- Glenn Willen
- Gregory Sanders
- Harris
- Hennadii Stepanov
- Jim Posen
- João Barbosa
- Jon Atack
- Karl-Johan Alm
- Luke Dashjr
- MarcoFalke
- Pieter Wuille
- Russell Yanofsky
- Sjors Provoost
- Wladimir J. van der Laan

As well as to everyone that helped with translations on
[Transifex](https://www.transifex.com/bitcoin/bitcoin/).
