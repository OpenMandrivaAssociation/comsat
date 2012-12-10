%define release %mkrel 11
%define version 0.17
%define url ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/

Summary: A mail checker client and comsat mail checking server
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



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.17-11mdv2011.0
+ Revision: 617409
- the mass rebuild of 2010.0 packages

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 0.17-10mdv2010.0
+ Revision: 424938
- rebuild

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0.17-9mdv2009.0
+ Revision: 243621
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.17-7mdv2008.1
+ Revision: 136335
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix summary-ended-with-dot

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 0.17-7mdv2008.0
+ Revision: 70159
- use %%mkrel


* Fri Apr 02 2004 Daouda LO <daouda@mandrakesoft.com> 0.17-6mdk
- rebuild

* Thu Jan 16 2003 Daouda LO <daouda@mandrakesoft.com> 0.17-5mdk
- rebuild (glibc and/or unpackaged files)
- add URL

* Wed Jun 12 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.17-4mdk
- explicit compiler choice...

* Wed Oct 17 2001 Daouda LO <daouda@mandrakesoft.com> 0.17-3mdk
- s/Copyright/License
- right permissions on files.

* Thu Sep 06 2001 Daouda LO <daouda@mandrakesoft.com> 0.17-2mdk
- rebuild.

* Sat Sep 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.17-1mdk
- xinetd support.
- 0.17.

* Thu Jul 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.15-3mdk
- BM, macro, spechelper (daouda sucks)

* Sat Mar 25 2000 Daouda Lo	<daouda@mandrakesoft.com> 0.15-2mdk
- adjust group

* Wed Nov 03 1999 John Buswell <johnb@mandrakesoft.com>
- 0.15
- Build Release

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

