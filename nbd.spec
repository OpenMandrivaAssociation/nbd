Name:           nbd
Version:        2.9.7
Release:        4%{dist}
Summary:        Network Block Device user-space tools (TCP version)

Group:          Applications/System
License:        GPL+
URL:            http://nbd.sourceforge.net/
Source0:        http://downloads.sourceforge.net/nbd/nbd-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glib2-devel
BuildRequires:  /usr/include/gnu/stubs-32.h

%description 
Tools for the Linux Kernel's network block device, allowing you to use
remote block devices over a TCP/IP network.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

# Include 32bit nbd-client on 64bit hosts because it is needed in client initrd's
%ifarch x86_64
  sed -i "s/SIZEOF_UNSIGNED_LONG_INT 8/SIZEOF_UNSIGNED_LONG_INT 4/" config.h
  export RPM_OPT_FLAGS=${RPM_OPT_FLAGS//-m64/-m32}
  # <jakub> warren: you can try compiling it with -static-libgcc, the
  #         binary doesn't seem to be threaded and so unlikely uses 
  #         pthread_cleanup_push/pop
  gcc $RPM_OPT_FLAGS -static-libgcc -o nbd-client-32 nbd-client.c;
%endif

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Include 32bit nbd-client on 64bit hosts because it is needed in client initrd's
%ifarch x86_64
  install -m 755 nbd-client-32 $RPM_BUILD_ROOT%{_sbindir}/nbd-client-32
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README simple_test nbd-tester-client.c cliserv.h
%{_mandir}/man*/nbd*
%{_bindir}/nbd-server
%{_sbindir}/nbd-client*

%changelog
* Wed Nov 07 2007 Warren Togami <wtogami@redhat.com> 2.9.7-4
- include nbd-client i386 in x86-64 RPM because initrd images need it

* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-3
- add buildrequires

* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-2
- package cleanups

* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-1
- update to 2.9.7

