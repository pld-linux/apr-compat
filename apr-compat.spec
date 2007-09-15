#
# Conditional build (Linux 2.4 compat, switch after Ac):
%bcond_with	epoll		# use epoll() syscall (requires Linux 2.6)
%bcond_with	sendfile64	# use sendfile64 on even if it requires Linux 2.6
%bcond_with	tcpnodelaycork	# use TCP_NODELAY|TCP_CORK flags (requires Linux 2.6)
#
# Linux 2.4.32 supports sendfile64 only on i386 and mips (only 32-bit archs matter)
%ifnarch ppc sparc sparc64
%define		with_sendfile64		1
%endif
Summary:	Apache Portable Runtime
Summary(pl):	Apache Portable Runtime - przeno�na biblioteka uruchomieniowa
Name:		apr
Version:	1.2.11
Release:	1
Epoch:		1
License:	Apache v2.0
Group:		Libraries
Source0:	http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
# Source0-md5:	22ede19520beb37dc17e62592b06a59c
Patch0:		%{name}-link.patch
Patch1:		%{name}-metuxmpm.patch
Patch2:		%{name}-libtool.patch
Patch3:		%{name}-no-epoll.patch
URL:		http://apr.apache.org/
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	libtool >= 1.3.3
BuildRequires:	libuuid-devel
BuildRequires:	sed >= 4.0
BuildRequires:	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	/usr/include/apr
%define		_datadir	/usr/share/apr

%description
The mission of the Apache Portable Runtime (APR) project is to create
and maintain software libraries that provide a predictable and
consistent interface to underlying platform-specific implementations.
The primary goal is to provide an API to which software developers may
code and be assured of predictable if not identical behaviour
regardless of the platform on which their software is built, relieving
them of the need to code special-case conditions to work around or
take advantage of platform-specific deficiencies or features.

%description -l pl
Celem projektu APR (Apache Portable Runtime) jest stworzenie i
utrzymywanie bibliotek dostarczaj�cych przewidywalnego i sp�jnego
interfejsu do le��cych u podstaw implementacji zale�nych od platformy.
G��wnym celem jest dostarczenie API, kt�rego mog� u�ywa� programi�ci
maj�c pewno��, �e zachowuje si� w spos�b przewidywalny, je�li nie
identyczny, niezale�nie od platformy na jakiej oprogramowanie jest
budowane oraz bez potrzeby kodowania specjalnych warunk�w do
obchodzenia lub wykorzystywania specyficznych dla platform r�nic lub
mo�liwo�ci.

%package devel
Summary:	Header files and development documentation for apr
Summary(pl):	Pliki nag��wkowe i dokumentacja programisty do apr
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libuuid-devel
Requires:	automake
Requires:	libtool

%description devel
Header files and development documentation for apr.

%description devel -l pl
Pliki nag��wkowe i dokumentacja programisty do apr.

%package static
Summary:	Static apr library
Summary(pl):	Statyczna biblioteka apr
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static apr library.

%description static -l pl
Statyczna biblioteka apr.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%{!?with_epoll:%patch3 -p1}

cat >> config.layout <<'EOF'
<Layout PLD>
sbindir:	%{_sbindir}
libexecdir:	%{_libdir}/apr
installbuilddir: ${datadir}/build-${APR_MAJOR_VERSION}
localstatedir:	/var/run
runtimedir:	/var/run
libsuffix:	-${APR_MAJOR_VERSION}
</Layout PLD>
EOF

%build
install /usr/share/automake/config.* build
./buildconf
%configure \
	%{!?with_tcpnodelaycork:apr_cv_tcp_nodelay_with_cork=no} \
	%{!?with_sendfile64:ac_cv_func_sendfile64=no} \
	--enable-layout=PLD \
%ifarch %{ix86} %{i8664}
%ifnarch i386
	--enable-nonportable-atomics \
%endif
%endif
	--enable-threads \
	--with-devrandom=/dev/urandom
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf %{_bindir}/libtool $RPM_BUILD_ROOT%{_datadir}/libtool

mv -f $RPM_BUILD_ROOT%{_datadir}/build-1 $RPM_BUILD_ROOT%{_datadir}/build
install build/{*apr*.m4,*.awk,*.sh,gen-build.py} $RPM_BUILD_ROOT%{_datadir}/build
ln -snf /usr/share/automake/config.{guess,sub} $RPM_BUILD_ROOT%{_datadir}/build
ln -snf /usr/share/libtool/ltmain.sh $RPM_BUILD_ROOT%{_datadir}/build
ln -snf /usr/bin/libtool $RPM_BUILD_ROOT%{_datadir}/build
ln -sf build $RPM_BUILD_ROOT%{_datadir}/build-1

sed -i -e 's@^\(APR_SOURCE_DIR=\).*@\1"%{_datadir}"@' \
	$RPM_BUILD_ROOT%{_bindir}/apr-1-config
sed -i -e 's@^\(apr_builddir\|apr_builders\)=.*@\1=%{_datadir}/build-1@' \
	$RPM_BUILD_ROOT%{_datadir}/build/apr_rules.mk
sed -i -e '1s@#!.*python@#!%{__python}@' $RPM_BUILD_ROOT%{_datadir}/build/gen-build.py

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES docs/*.html
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/apr.exp
%{_includedir}
%dir %{_datadir}
%dir %{_datadir}/build
%{_datadir}/build/*.mk
%{_datadir}/build/*.m4
%{_datadir}/build/*.awk
%attr(755,root,root) %{_datadir}/build/config.*
%attr(755,root,root) %{_datadir}/build/*.sh
%attr(755,root,root) %{_datadir}/build/libtool
%attr(755,root,root) %{_datadir}/build/gen-build.py
%{_datadir}/build-1
%{_pkgconfigdir}/apr-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
