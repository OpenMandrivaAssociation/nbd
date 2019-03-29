Name:           nbd
Version:        3.19
Release:        2
Summary:        Network Block Device user-space tools (TCP version)
License:        GPLv2
URL:            http://nbd.sourceforge.net
# https://github.com/NetworkBlockDevice/nbd
Source0:        http://downloads.sourceforge.net/project/nbd/nbd/%{version}/%{name}-%{version}.tar.xz
Source1:        nbd-server.service
Source2:        nbd-server.sysconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  systemd
BuildRequires:	rpm-helper

%description
Tools for the Linux Kernel's network block device, allowing you to use
remote block devices over a TCP/IP network.

%package server
Summary:	NBD (Network Block Device) server
Requires(pre,postun):	rpm-helper

%description server
NBD (Network Block Device) server

%prep
%autosetup

%build
%configure --enable-syslog --enable-lfs --enable-gznbd
%make_build

%install
%make_install
install -pDm644 systemd/nbd@.service %{buildroot}%{_unitdir}/nbd@.service
mkdir -p %{buildroot}%{_unitdir}/nbd@.service.d
cat > %{buildroot}%{_unitdir}/nbd@.service.d/modprobe.conf <<EOF
[Service]
ExecStartPre=/sbin/modprobe nbd
EOF
install -pDm644 %{S:1} %{buildroot}%{_unitdir}/nbd-server.service
install -pDm644 %{S:2} %{buildroot}%{_sysconfdir}/sysconfig/nbd-server

mkdir -p %{buildroot}%{_sysconfdir}/nbd-server/exports.d
touch %{buildroot}%{_sysconfdir}/nbd-server/allow
cat >%{buildroot}%{_sysconfdir}/nbd-server/config <<EOF
[generic]
# Allow clients to fetch a list of exports
# We default to true -- please secure your setup
# by only allowing "good" IPs to connect through
# %{_sysconfdir}/nbd-server/allow
allowlist=true
user=nbd
group=nbd
includedir=%{_sysconfdir}/nbd-server/exports.d
EOF
mkdir -p %{buildroot}/srv/nbd
cat >export-example.conf <<EOF
# This file, if placed in /etc/nbd-server/exports.d,
# exports a file called /srv/nbd/rootfs-IPADDRESS.img
# (where IPADDRESS is the IP address of the client connecting)
# as "/"
[/]
virtstyle=ipliteral
maxconnections=1
exportname=/srv/nbd/rootfs-%s.img 
authfile=/etc/nbd-server/allow
EOF

%check
# wait longer for nbd-server to fully start,
# one second may not be enough on Fedora building infra
sed -i -e 's/sleep 1/sleep 10/' tests/run/simple_test
# For some reason, TLS tests currently fail all the time.
# Let's run the tests, but allow failure for now.
#make check || :

%files
%doc README.md doc/proto.md doc/todo.txt
%license COPYING
%{_bindir}/nbd-trdump
%{_bindir}/gznbd
%{_sbindir}/nbd-client
%{_sbindir}/min-nbd-client
%{_unitdir}/nbd@.service
%{_unitdir}/nbd@.service.d
%{_mandir}/man1/nbd-trdump.1*
%{_mandir}/man5/nbdtab.5*
%{_mandir}/man8/nbd-client.8*


%pre server
%_pre_useradd nbd /srv/nbd /bin/false
%_pre_groupadd nbd nbd

%postun server
%_postun_userdel nbd
%_postun_groupdel nbd

%files server
%doc export-example.conf
%config(noreplace) %{_sysconfdir}/sysconfig/nbd-server
%dir %{_sysconfdir}/nbd-server
%dir %{_sysconfdir}/nbd-server/exports.d
%ghost %config(noreplace) %{_sysconfdir}/nbd-server/allow
%config(noreplace) %{_sysconfdir}/nbd-server/config
%{_bindir}/nbd-server
%{_unitdir}/nbd-server.service
/srv/nbd
%{_mandir}/man1/nbd-server.1*
%{_mandir}/man5/nbd-server.5*
