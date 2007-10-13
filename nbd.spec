Name:           nbd
Version:        2.9.7
Release:        2%{dist}
Summary:        Network Block Device user-space tools (TCP version)

Group:          Applications/System
License:        GPL+
URL:            http://nbd.sourceforge.net/
Source0:        http://downloads.sourceforge.net/nbd/nbd-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  
#Requires:       

%description 
Tools for the Linux Kernel's network block device, allowing you to use
remote block devices over a TCP/IP network.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README simple_test nbd-tester-client.c cliserv.h
%{_mandir}/man*/nbd*
%{_bindir}/nbd-server
%{_sbindir}/nbd-client

%changelog
* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-2
- package cleanups

* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-1
- update to 2.9.7

