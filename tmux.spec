Name:           tmux
Version:        1.0
Release:        2%{?dist}
Summary:        A terminal multiplexer

Group:          Applications/System
# Most of the source is ISC licensed; some of the files in compat/ are 2 and
# 3 clause BSD licensed.
License:        ISC and BSD
URL:            http://sourceforge.net/projects/tmux
Requires(pre):  shadow-utils
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# This first patch creates MANDIR in the GNUmakefile.  This has been sent
# upstream via email but upstream replied and said would not change.
Patch0:         tmux-1.0-02_fix_wrong_location.diff
Patch1:         tmux-1.0-03_proper_socket_handling.diff
Patch2:         tmux-1.0-04_dropping_unnecessary_privileges.diff
Patch3:         tmux-1.0-06_hardening_write_return.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

%prep
%setup -q
%patch0 -p1 -b .location
%patch1 -p1 -b .sockethandling
%patch2 -p1 -b .dropprivs
%patch3 -p1 -b .writehard

%build
%configure
make %{?_smp_mflags} LDFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLBIN="install -p -m 755" INSTALLMAN="install -p -m 644"

# Create the socket dir
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/%{name}

%clean
rm -rf %{buildroot}

%pre
getent group tmux >/dev/null || groupadd -r tmux

%files
%defattr(-,root,root,-)
%doc CHANGES FAQ NOTES TODO examples/
%attr(2755,root,tmux) %{_bindir}/tmux
%{_mandir}/man1/tmux.1.*
%attr(775,root,tmux) %{_localstatedir}/run/tmux

%changelog
* Sun Nov 01 2009 Sven Lankes <sven@lank.es> 1.0-2
- Add debian patches
- Add tmux group for improved socket handling

* Sat Oct 24 2009 Sven Lankes <sven@lank.es> 1.0-1
- New upstream release

* Mon Jul 13 2009 Chess Griffin <chess@chessgriffin.com> 0.9-1
- Update to version 0.9.
- Remove sed invocation as this was adopted upstream.
- Remove optflags patch since upstream source now uses ./configure and
  detects the flags when passed to make.

* Tue Jun 23 2009 Chess Griffin <chess@chessgriffin.com> 0.8-5
- Note that souce is mostly ISC licensed with some 2 and 3 clause BSD in
  compat/.
- Remove fixiquote.patch and instead use a sed invocation in setup.

* Mon Jun 22 2009 Chess Griffin <chess@chessgriffin.com> 0.8-4
- Add optimization flags by patching GNUmakefile and passing LDFLAGS
  to make command.
- Use consistent macro format.
- Change examples/* to examples/ and add TODO to docs.

* Sun Jun 21 2009 Chess Griffin <chess@chessgriffin.com> 0.8-3
- Remove fixperms.patch and instead pass them at make install stage.

* Sat Jun 20 2009 Chess Griffin <chess@chessgriffin.com> 0.8-2
- Fix Source0 URL to point to correct upstream source.
- Modify fixperms.patch to set 644 permissions on the tmux.1.gz man page.
- Remove wildcards from 'files' section and replace with specific paths and
  filenames.

* Mon Jun 15 2009 Chess Griffin <chess@chessgriffin.com> 0.8-1
- Initial RPM release.
