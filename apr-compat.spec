%define	snap	20030913101709
Summary:	Apache Portable Runtime
Summary(pl):	Apache Portable Runtime - przeno�na biblioteka uruchomieniowa
Name:		apr
Version:	0.9.4
Release:	0.%{snap}.2
Epoch:		1
License:	GPL
Group:		Libraries
# http://www.apache.org/dist/apr/%{name}-%{version}.tar.gz
Source0:	http://cvs.apache.org/snapshots/apr/%{name}_%{snap}.tar.gz
# Source0-md5:	d14874964cd7f686594534d9e949eaee
Patch0:		%{name}-link.patch
URL:		http://apr.apache.org/
BuildRequires:	autoconf >= 2.13
BuildRequires:	libtool >= 1.3.3
BuildRequires:	perl-base
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
utrzymywanie bibliotek dostarcaj�cych przewidywalnego i sp�jnego
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
%setup -q -n %{name}
%patch -p1 -b .orig

%build
./buildconf
%configure \
	--enable-threads
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf %{_bindir}/libtool $RPM_BUILD_ROOT%{_datadir}/libtool

install build/{*apr*.m4,*.awk,*.sh,config.*} $RPM_BUILD_ROOT%{_datadir}/build

%{__perl} -pi -e "s#$RPM_BUILD_DIR/%{name}#%{_datadir}#g" $RPM_BUILD_ROOT%{_bindir}/*
%{__perl} -pi -e "s#$RPM_BUILD_DIR/%{name}.*#%{_datadir}/build#g" $RPM_BUILD_ROOT%{_datadir}/build/*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES STATUS docs/*.html
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

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
