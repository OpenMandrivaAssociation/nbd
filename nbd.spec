Name:           nbd
Version:        3.18
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

%description
Tools for the Linux Kernel's network block device, allowing you to use
remote block devices over a TCP/IP network.

%prep
%setup -q

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

%check
# wait longer for nbd-server to fully start,
# one second may not be enough on Fedora building infra
sed -i -e 's/sleep 1/sleep 10/' tests/run/simple_test
make check

%files
%doc README.md doc/proto.md doc/todo.txt
%license COPYING
%{_bindir}/nbd-server
%{_bindir}/nbd-trdump
%{_bindir}/gznbd
%{_mandir}/man*/nbd*
%{_sbindir}/nbd-client
%{_sbindir}/min-nbd-client
%config(noreplace) %{_sysconfdir}/sysconfig/nbd-server
%{_unitdir}/nbd-server.service
%{_unitdir}/nbd@.service
%{_unitdir}/nbd@.service.d
