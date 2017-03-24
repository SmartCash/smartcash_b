SmartCash Core 0.14.99
=====================

Setup
---------------------
SmartCash Core is the original SmartCash client and it builds the backbone of the network. It downloads and, by default, stores the entire history of SmartCash transactions (which is currently more than 100 GBs); depending on the speed of your computer and network connection, the synchronization process can take anywhere from a few hours to a day or more.

To download SmartCash Core, visit [smartcashcore.org](https://smartcashcore.org/en/releases/).

Running
---------------------
The following are some helpful notes on how to run SmartCash on your native platform.

### Unix

Unpack the files into a directory and run:

- `bin/smartcash-qt` (GUI) or
- `bin/smartcashd` (headless)

### Windows

Unpack the files into a directory, and then run smartcash-qt.exe.

### OS X

Drag SmartCash-Core to your applications folder, and then run SmartCash-Core.

### Need Help?

* See the documentation at the [SmartCash Wiki](https://en.smartcash.it/wiki/Main_Page)
for help and more information.
* Ask for help on [#smartcash](http://webchat.freenode.net?channels=smartcash) on Freenode. If you don't have an IRC client use [webchat here](http://webchat.freenode.net?channels=smartcash).
* Ask for help on the [SmartCashTalk](https://smartcashtalk.org/) forums, in the [Technical Support board](https://smartcashtalk.org/index.php?board=4.0).

Building
---------------------
The following are developer notes on how to build SmartCash on your native platform. They are not complete guides, but include notes on the necessary libraries, compile flags, etc.

- [OS X Build Notes](build-osx.md)
- [Unix Build Notes](build-unix.md)
- [Windows Build Notes](build-windows.md)
- [OpenBSD Build Notes](build-openbsd.md)
- [Gitian Building Guide](gitian-building.md)

Development
---------------------
The SmartCash repo's [root README](/README.md) contains relevant information on the development process and automated testing.

- [Developer Notes](developer-notes.md)
- [Release Notes](release-notes.md)
- [Release Process](release-process.md)
- [Source Code Documentation (External Link)](https://dev.visucore.com/smartcash/doxygen/)
- [Translation Process](translation_process.md)
- [Translation Strings Policy](translation_strings_policy.md)
- [Travis CI](travis-ci.md)
- [Unauthenticated REST Interface](REST-interface.md)
- [Shared Libraries](shared-libraries.md)
- [BIPS](bips.md)
- [Dnsseed Policy](dnsseed-policy.md)
- [Benchmarking](benchmarking.md)

### Resources
* Discuss on the [SmartCashTalk](https://smartcashtalk.org/) forums, in the [Development & Technical Discussion board](https://smartcashtalk.org/index.php?board=6.0).
* Discuss project-specific development on #smartcash-core-dev on Freenode. If you don't have an IRC client use [webchat here](http://webchat.freenode.net/?channels=smartcash-core-dev).
* Discuss general SmartCash development on #smartcash-dev on Freenode. If you don't have an IRC client use [webchat here](http://webchat.freenode.net/?channels=smartcash-dev).

### Miscellaneous
- [Assets Attribution](assets-attribution.md)
- [Files](files.md)
- [Fuzz-testing](fuzzing.md)
- [Reduce Traffic](reduce-traffic.md)
- [Tor Support](tor.md)
- [Init Scripts (systemd/upstart/openrc)](init.md)
- [ZMQ](zmq.md)

License
---------------------
Distributed under the [MIT software license](/COPYING).
This product includes software developed by the OpenSSL Project for use in the [OpenSSL Toolkit](https://www.openssl.org/). This product includes
cryptographic software written by Eric Young ([eay@cryptsoft.com](mailto:eay@cryptsoft.com)), and UPnP software written by Thomas Bernard.
