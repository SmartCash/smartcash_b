%define bdbv 4.8.30
%global selinux_variants mls strict targeted

%if 0%{?_no_gui:1}
%define _buildqt 0
%define buildargs --with-gui=no
%else
%define _buildqt 1
%if 0%{?_use_qt4}
%define buildargs --with-qrencode --with-gui=qt4
%else
%define buildargs --with-qrencode --with-gui=qt5
%endif
%endif

Name:		smartcash
Version:	0.12.0
Release:	2%{?dist}
Summary:	Peer to Peer Cryptographic Currency

Group:		Applications/System
License:	MIT
URL:		https://smartcash.org/
Source0:	https://smartcash.org/bin/smartcash-core-%{version}/smartcash-%{version}.tar.gz
Source1:	http://download.oracle.com/berkeley-db/db-%{bdbv}.NC.tar.gz

Source10:	https://raw.githubusercontent.com/smartcash/smartcash/v%{version}/contrib/debian/examples/smartcash.conf

#man pages
Source20:	https://raw.githubusercontent.com/smartcash/smartcash/v%{version}/doc/man/smartcashd.1
Source21:	https://raw.githubusercontent.com/smartcash/smartcash/v%{version}/doc/man/smartcash-cli.1
Source22:	https://raw.githubusercontent.com/smartcash/smartcash/v%{version}/doc/man/smartcash-qt.1

#selinux
Source30:	https://raw.githubusercontent.com/smartcash/smartcash/v%{version}/contrib/rpm/smartcash.te
# Source31 - what about smartcash-tx and bench_smartcash ???
Source31:	https://raw.githubusercontent.com/smartcash/smartcash/v%{version}/contrib/rpm/smartcash.fc
Source32:	https://raw.githubusercontent.com/smartcash/smartcash/v%{version}/contrib/rpm/smartcash.if

Source100:	https://upload.wikimedia.org/wikipedia/commons/4/46/SmartCash.svg

%if 0%{?_use_libressl:1}
BuildRequires:	libressl-devel
%else
BuildRequires:	openssl-devel
%endif
BuildRequires:	boost-devel
BuildRequires:	miniupnpc-devel
BuildRequires:	autoconf automake libtool
BuildRequires:	libevent-devel


Patch0:		smartcash-0.12.0-libressl.patch


%description
SmartCash is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of smartcashs is carried out collectively by the network.

%if %{_buildqt}
%package core
Summary:	Peer to Peer Cryptographic Currency
Group:		Applications/System
Obsoletes:	%{name} < %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
%if 0%{?_use_qt4}
BuildRequires:	qt-devel
%else
BuildRequires:	qt5-qtbase-devel
# for /usr/bin/lrelease-qt5
BuildRequires:	qt5-linguist
%endif
BuildRequires:	protobuf-devel
BuildRequires:	qrencode-devel
BuildRequires:	%{_bindir}/desktop-file-validate
# for icon generation from SVG
BuildRequires:	%{_bindir}/inkscape
BuildRequires:	%{_bindir}/convert

%description core
SmartCash is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of smartcashs is carried out collectively by the network.

This package contains the Qt based graphical client and node. If you are looking
to run a SmartCash wallet, this is probably the package you want.
%endif


%package libs
Summary:	SmartCash shared libraries
Group:		System Environment/Libraries

%description libs
This package provides the smartcashconsensus shared libraries. These libraries
may be used by third party software to provide consensus verification
functionality.

Unless you know need this package, you probably do not.

%package devel
Summary:	Development files for smartcash
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files and static library for the
smartcashconsensus shared library. If you are developing or compiling software
that wants to link against that library, then you need this package installed.

Most people do not need this package installed.

%package server
Summary:	The smartcash daemon
Group:		System Environment/Daemons
Requires:	smartcash-utils = %{version}-%{release}
Requires:	selinux-policy policycoreutils-python
Requires(pre):	shadow-utils
Requires(post):	%{_sbindir}/semodule %{_sbindir}/restorecon %{_sbindir}/fixfiles %{_sbindir}/sestatus
Requires(postun):	%{_sbindir}/semodule %{_sbindir}/restorecon %{_sbindir}/fixfiles %{_sbindir}/sestatus
BuildRequires:	systemd
BuildRequires:	checkpolicy
BuildRequires:	%{_datadir}/selinux/devel/Makefile

%description server
This package provides a stand-alone smartcash-core daemon. For most users, this
package is only needed if they need a full-node without the graphical client.

Some third party wallet software will want this package to provide the actual
smartcash-core node they use to connect to the network.

If you use the graphical smartcash-core client then you almost certainly do not
need this package.

%package utils
Summary:	SmartCash utilities
Group:		Applications/System

%description utils
This package provides several command line utilities for interacting with a
smartcash-core daemon.

The smartcash-cli utility allows you to communicate and control a smartcash daemon
over RPC, the smartcash-tx utility allows you to create a custom transaction, and
the bench_smartcash utility can be used to perform some benchmarks.

This package contains utilities needed by the smartcash-server package.


%prep
%setup -q
%patch0 -p1 -b .libressl
cp -p %{SOURCE10} ./smartcash.conf.example
tar -zxf %{SOURCE1}
cp -p db-%{bdbv}.NC/LICENSE ./db-%{bdbv}.NC-LICENSE
mkdir db4 SELinux
cp -p %{SOURCE30} %{SOURCE31} %{SOURCE32} SELinux/


%build
CWD=`pwd`
cd db-%{bdbv}.NC/build_unix/
../dist/configure --enable-cxx --disable-shared --with-pic --prefix=${CWD}/db4
make install
cd ../..

./autogen.sh
%configure LDFLAGS="-L${CWD}/db4/lib/" CPPFLAGS="-I${CWD}/db4/include/" --with-miniupnpc --enable-glibc-back-compat %{buildargs}
make %{?_smp_mflags}

pushd SELinux
for selinuxvariant in %{selinux_variants}; do
	make NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile
	mv smartcash.pp smartcash.pp.${selinuxvariant}
	make NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile clean
done
popd


%install
make install DESTDIR=%{buildroot}

mkdir -p -m755 %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/smartcashd %{buildroot}%{_sbindir}/smartcashd

# systemd stuff
mkdir -p %{buildroot}%{_tmpfilesdir}
cat <<EOF > %{buildroot}%{_tmpfilesdir}/smartcash.conf
d /run/smartcashd 0750 smartcash smartcash -
EOF
touch -a -m -t 201504280000 %{buildroot}%{_tmpfilesdir}/smartcash.conf

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/smartcash
# Provide options to the smartcash daemon here, for example
# OPTIONS="-testnet -disable-wallet"

OPTIONS=""

# System service defaults.
# Don't change these unless you know what you're doing.
CONFIG_FILE="%{_sysconfdir}/smartcash/smartcash.conf"
DATA_DIR="%{_localstatedir}/lib/smartcash"
PID_FILE="/run/smartcashd/smartcashd.pid"
EOF
touch -a -m -t 201504280000 %{buildroot}%{_sysconfdir}/sysconfig/smartcash

mkdir -p %{buildroot}%{_unitdir}
cat <<EOF > %{buildroot}%{_unitdir}/smartcash.service
[Unit]
Description=SmartCash daemon
After=syslog.target network.target

[Service]
Type=forking
ExecStart=%{_sbindir}/smartcashd -daemon -conf=\${CONFIG_FILE} -datadir=\${DATA_DIR} -pid=\${PID_FILE} \$OPTIONS
EnvironmentFile=%{_sysconfdir}/sysconfig/smartcash
User=smartcash
Group=smartcash

Restart=on-failure
PrivateTmp=true
TimeoutStopSec=120
TimeoutStartSec=60
StartLimitInterval=240
StartLimitBurst=5

[Install]
WantedBy=multi-user.target
EOF
touch -a -m -t 201504280000 %{buildroot}%{_unitdir}/smartcash.service
#end systemd stuff

mkdir %{buildroot}%{_sysconfdir}/smartcash
mkdir -p %{buildroot}%{_localstatedir}/lib/smartcash

#SELinux
for selinuxvariant in %{selinux_variants}; do
	install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
	install -p -m 644 SELinux/smartcash.pp.${selinuxvariant} %{buildroot}%{_datadir}/selinux/${selinuxvariant}/smartcash.pp
done

%if %{_buildqt}
# qt icons
install -D -p share/pixmaps/smartcash.ico %{buildroot}%{_datadir}/pixmaps/smartcash.ico
install -p share/pixmaps/nsis-header.bmp %{buildroot}%{_datadir}/pixmaps/
install -p share/pixmaps/nsis-wizard.bmp %{buildroot}%{_datadir}/pixmaps/
install -p %{SOURCE100} %{buildroot}%{_datadir}/pixmaps/smartcash.svg
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/smartcash16.png -w16 -h16
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/smartcash32.png -w32 -h32
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/smartcash64.png -w64 -h64
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/smartcash128.png -w128 -h128
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/smartcash256.png -w256 -h256
%{_bindir}/convert -resize 16x16 %{buildroot}%{_datadir}/pixmaps/smartcash256.png %{buildroot}%{_datadir}/pixmaps/smartcash16.xpm
%{_bindir}/convert -resize 32x32 %{buildroot}%{_datadir}/pixmaps/smartcash256.png %{buildroot}%{_datadir}/pixmaps/smartcash32.xpm
%{_bindir}/convert -resize 64x64 %{buildroot}%{_datadir}/pixmaps/smartcash256.png %{buildroot}%{_datadir}/pixmaps/smartcash64.xpm
%{_bindir}/convert -resize 128x128 %{buildroot}%{_datadir}/pixmaps/smartcash256.png %{buildroot}%{_datadir}/pixmaps/smartcash128.xpm
%{_bindir}/convert %{buildroot}%{_datadir}/pixmaps/smartcash256.png %{buildroot}%{_datadir}/pixmaps/smartcash256.xpm
touch %{buildroot}%{_datadir}/pixmaps/*.png -r %{SOURCE100}
touch %{buildroot}%{_datadir}/pixmaps/*.xpm -r %{SOURCE100}

# Desktop File - change the touch timestamp if modifying
mkdir -p %{buildroot}%{_datadir}/applications
cat <<EOF > %{buildroot}%{_datadir}/applications/smartcash-core.desktop
[Desktop Entry]
Encoding=UTF-8
Name=SmartCash
Comment=SmartCash P2P Cryptocurrency
Comment[fr]=SmartCash, monnaie virtuelle cryptographique pair à pair
Comment[tr]=SmartCash, eşten eşe kriptografik sanal para birimi
Exec=smartcash-qt %u
Terminal=false
Type=Application
Icon=smartcash128
MimeType=x-scheme-handler/smartcash;
Categories=Office;Finance;
EOF
# change touch date when modifying desktop
touch -a -m -t 201511100546 %{buildroot}%{_datadir}/applications/smartcash-core.desktop
%{_bindir}/desktop-file-validate %{buildroot}%{_datadir}/applications/smartcash-core.desktop

# KDE protocol - change the touch timestamp if modifying
mkdir -p %{buildroot}%{_datadir}/kde4/services
cat <<EOF > %{buildroot}%{_datadir}/kde4/services/smartcash-core.protocol
[Protocol]
exec=smartcash-qt '%u'
protocol=smartcash
input=none
output=none
helper=true
listing=
reading=false
writing=false
makedir=false
deleting=false
EOF
# change touch date when modifying protocol
touch -a -m -t 201511100546 %{buildroot}%{_datadir}/kde4/services/smartcash-core.protocol
%endif

# man pages
install -D -p %{SOURCE20} %{buildroot}%{_mandir}/man1/smartcashd.1
install -p %{SOURCE21} %{buildroot}%{_mandir}/man1/smartcash-cli.1
%if %{_buildqt}
install -p %{SOURCE22} %{buildroot}%{_mandir}/man1/smartcash-qt.1
%endif

# nuke these, we do extensive testing of binaries in %%check before packaging
rm -f %{buildroot}%{_bindir}/test_*

%check
make check
srcdir=src test/smartcash-util-test.py
test/functional/test_runner.py --extended

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%pre server
getent group smartcash >/dev/null || groupadd -r smartcash
getent passwd smartcash >/dev/null ||
	useradd -r -g smartcash -d /var/lib/smartcash -s /sbin/nologin \
	-c "SmartCash wallet server" smartcash
exit 0

%post server
%systemd_post smartcash.service
# SELinux
if [ `%{_sbindir}/sestatus |grep -c "disabled"` -eq 0 ]; then
for selinuxvariant in %{selinux_variants}; do
	%{_sbindir}/semodule -s ${selinuxvariant} -i %{_datadir}/selinux/${selinuxvariant}/smartcash.pp &> /dev/null || :
done
%{_sbindir}/semanage port -a -t smartcash_port_t -p tcp 8332
%{_sbindir}/semanage port -a -t smartcash_port_t -p tcp 8333
%{_sbindir}/semanage port -a -t smartcash_port_t -p tcp 18332
%{_sbindir}/semanage port -a -t smartcash_port_t -p tcp 18333
%{_sbindir}/fixfiles -R smartcash-server restore &> /dev/null || :
%{_sbindir}/restorecon -R %{_localstatedir}/lib/smartcash || :
fi

%posttrans server
%{_bindir}/systemd-tmpfiles --create

%preun server
%systemd_preun smartcash.service

%postun server
%systemd_postun smartcash.service
# SELinux
if [ $1 -eq 0 ]; then
	if [ `%{_sbindir}/sestatus |grep -c "disabled"` -eq 0 ]; then
	%{_sbindir}/semanage port -d -p tcp 8332
	%{_sbindir}/semanage port -d -p tcp 8333
	%{_sbindir}/semanage port -d -p tcp 18332
	%{_sbindir}/semanage port -d -p tcp 18333
	for selinuxvariant in %{selinux_variants}; do
		%{_sbindir}/semodule -s ${selinuxvariant} -r smartcash &> /dev/null || :
	done
	%{_sbindir}/fixfiles -R smartcash-server restore &> /dev/null || :
	[ -d %{_localstatedir}/lib/smartcash ] && \
		%{_sbindir}/restorecon -R %{_localstatedir}/lib/smartcash &> /dev/null || :
	fi
fi

%clean
rm -rf %{buildroot}

%if %{_buildqt}
%files core
%defattr(-,root,root,-)
%license COPYING db-%{bdbv}.NC-LICENSE
%doc COPYING smartcash.conf.example doc/README.md doc/bips.md doc/files.md doc/multiwallet-qt.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%attr(0755,root,root) %{_bindir}/smartcash-qt
%attr(0644,root,root) %{_datadir}/applications/smartcash-core.desktop
%attr(0644,root,root) %{_datadir}/kde4/services/smartcash-core.protocol
%attr(0644,root,root) %{_datadir}/pixmaps/*.ico
%attr(0644,root,root) %{_datadir}/pixmaps/*.bmp
%attr(0644,root,root) %{_datadir}/pixmaps/*.svg
%attr(0644,root,root) %{_datadir}/pixmaps/*.png
%attr(0644,root,root) %{_datadir}/pixmaps/*.xpm
%attr(0644,root,root) %{_mandir}/man1/smartcash-qt.1*
%endif

%files libs
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/shared-libraries.md
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/developer-notes.md doc/shared-libraries.md
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files server
%defattr(-,root,root,-)
%license COPYING db-%{bdbv}.NC-LICENSE
%doc COPYING smartcash.conf.example doc/README.md doc/REST-interface.md doc/bips.md doc/dnsseed-policy.md doc/files.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%attr(0755,root,root) %{_sbindir}/smartcashd
%attr(0644,root,root) %{_tmpfilesdir}/smartcash.conf
%attr(0644,root,root) %{_unitdir}/smartcash.service
%dir %attr(0750,smartcash,smartcash) %{_sysconfdir}/smartcash
%dir %attr(0750,smartcash,smartcash) %{_localstatedir}/lib/smartcash
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/smartcash
%attr(0644,root,root) %{_datadir}/selinux/*/*.pp
%attr(0644,root,root) %{_mandir}/man1/smartcashd.1*

%files utils
%defattr(-,root,root,-)
%license COPYING
%doc COPYING smartcash.conf.example doc/README.md
%attr(0755,root,root) %{_bindir}/smartcash-cli
%attr(0755,root,root) %{_bindir}/smartcash-tx
%attr(0755,root,root) %{_bindir}/bench_smartcash
%attr(0644,root,root) %{_mandir}/man1/smartcash-cli.1*



%changelog
* Fri Feb 26 2016 Alice Wonder <buildmaster@librelamp.com> - 0.12.0-2
- Rename Qt package from smartcash to smartcash-core
- Make building of the Qt package optional
- When building the Qt package, default to Qt5 but allow building
-  against Qt4
- Only run SELinux stuff in post scripts if it is not set to disabled

* Wed Feb 24 2016 Alice Wonder <buildmaster@librelamp.com> - 0.12.0-1
- Initial spec file for 0.12.0 release

# This spec file is written from scratch but a lot of the packaging decisions are directly
# based upon the 0.11.2 package spec file from https://www.ringingliberty.com/smartcash/
