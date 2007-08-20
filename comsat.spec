%define release %mkrel 6
%define version 0.17
%define url ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/

Summary: A mail checker client and comsat mail checking server.
Name: comsat
Version: %{version}
Release: %{release}
License: BSD
Group: Networking/Mail
Source0:  %{url}/biff+comsat-%{version}.tar.bz2
Source1: %{name}-xinetd
Patch0: biff+comsat-0.10-nobr.patch
URL: http://freshmeat.net/projects/netkit/
Obsoletes: biff
Provides: biff
Requires: xinetd
BuildRoot: %{_tmppath}/%{name}-buildroot

%description
The biff client and comsat server are an antiquated method of
asynchronous mail notification.  Although they are still supported, most
users use their shell's MAIL variable (or csh shell's mail variable) to
check for mail, or a dedicated application like xbiff or xmailbox.  If
the comsat service is not enabled, biff won't work and you'll need to use
either the MAIL or mail variable.   

You may want to install biff if you'd like to be notified when mail
arrives. However, you should probably check out the more modern
methodologies of mail notification (xbiff or xmailbox) instead.

%prep
%setup -q -n biff+comsat-%{version}
%patch0 -p1

%build
sh configure --with-c-compiler=gcc

perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS),;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_bindir},%{_mandir}/man{1,8},usr/sbin}

make install INSTALLROOT=$RPM_BUILD_ROOT MANDIR=%{_mandir}

rm $RPM_BUILD_ROOT%{_mandir}/man8/comsat.8
ln -s in.comsat.8.bz2 $RPM_BUILD_ROOT%{_mandir}/man8/comsat.8.bz2

install -D -m644 %SOURCE1 ${RPM_BUILD_ROOT}/etc/xinetd.d/comsat

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/biff
%{_sbindir}/in.comsat
%config(noreplace) /etc/xinetd.d/comsat
%{_mandir}/man[18]/*

