%define url ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/

Summary:	A mail checker client and comsat mail checking server
Name:		comsat
Version:	0.17
Release:	12
License:	BSD
Group:		Networking/Mail
Url:		http://freshmeat.net/projects/netkit/
Source0:	ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/biff+comsat-%{version}.tar.bz2
Source1:	%{name}-xinetd
Patch0:		biff+comsat-0.10-nobr.patch
Patch1:		biff+comsat-0.17-no-strip.patch
Requires:	xinetd
Provides:	biff = %{EVRD}

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

%files
%{_bindir}/biff
%{_sbindir}/in.comsat
%config(noreplace) %{_sysconfdir}/xinetd.d/comsat
%{_mandir}/man[18]/*

#----------------------------------------------------------------------------

%prep
%setup -q -n biff+comsat-%{version}
%patch1 -p1
%patch0 -p1

%build
sh configure --with-c-compiler=gcc

perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

sed s/"-O2"/"%{optflags}"/g -i MCONFIG

%make

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man8

make install INSTALLROOT=%{buildroot} MANDIR=%{_mandir}

rm %{buildroot}%{_mandir}/man8/comsat.8
ln -s in.comsat.8.bz2 %{buildroot}%{_mandir}/man8/comsat.8.bz2

install -D -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xinetd.d/comsat

