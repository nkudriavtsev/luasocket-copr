%if 0%{?fedora} >= 20 || 0%{?rhel} > 7
%define luaver 5.2
%else
%define luaver 5.1
%endif

%define luacompatver 5.1
%define luacompatlibdir %{_libdir}/lua/%{luacompatver}
%define luacompatpkgdir %{_datadir}/lua/%{luacompatver}
%define lua51dir %{_builddir}/lua51-%{name}-%{version}-%{release}

%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}
%global baseversion 3.0-rc1
%global upstreamname luasocket

Name:           lua-socket
Version:        3.0
Release:        0.5rc1%{?dist}
Summary:        Network support for the Lua language

Group:          Development/Libraries
License:        MIT
URL:            http://www.tecgraf.puc-rio.br/~diego/professional/luasocket/
#Source0:        http://luaforge.net/frs/download.php/2664/luasocket-%{baseversion}.tar.gz
Source0:        https://github.com/diegonehab/%{upstreamname}/archive/v%{baseversion}.tar.gz
Patch0:		    luasocket-optflags.patch
# All changes in the upstream repo from %{baseversion} tag to the
# current master. Seems to be harmless.
Patch1:         luasocket-no-global-vars.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  lua >= %{luaver}, lua-devel >= %{luaver}
BuildRequires:  /usr/bin/iconv
Requires:       lua >= %{luaver}

%if 0%{?fedora} >= 20
BuildRequires:  compat-lua >= %{luacompatver}, compat-lua-devel >= %{luacompatver}
%endif

%package devel
Summary:    Development files for %{name}
Group:      Development/Languages
Requires:   %{name}%{?_isa} = %{version}-%{release}


%description
LuaSocket is a Lua extension library that is composed by two parts: a C core
that provides support for the TCP and UDP transport layers, and a set of Lua
modules that add support for functionality commonly needed by applications
that deal with the Internet.

Among the support modules, the most commonly used implement the SMTP, HTTP
and FTP. In addition there are modules for MIME, URL handling and LTN12.

%description devel
Header files and libraries for building an extension library for the
Lua using %{name}

%if 0%{?fedora} >= 20
%package compat
Summary:        Network support for the Lua language 5.1
Group:          Development/Libraries

%description compat
LuaSocket is a Lua extension library that is composed by two parts: a C core
that provides support for the TCP and UDP transport layers, and a set of Lua
modules that add support for functionality commonly needed by applications
that deal with the Internet.

Among the support modules, the most commonly used implement the SMTP, HTTP
and FTP. In addition there are modules for MIME, URL handling and LTN12.
%endif

%prep
%setup -q -n %{upstreamname}-%{baseversion}
%patch0 -p1 -b .optflags
%patch1 -p1 -b .noglobal

%if 0%{?fedora} >= 20
rm -rf %{lua51dir}
cp -a . %{lua51dir}
%endif

%build
make %{?_smp_mflags} LUAV=%{luaver} OPTFLAGS="%{optflags} -fPIC" linux
/usr/bin/iconv -f ISO8859-1 -t UTF8 LICENSE >LICENSE.UTF8
mv -f LICENSE.UTF8 LICENSE

%if 0%{?fedora} >= 20
pushd %{lua51dir}
make %{?_smp_mflags} LUAV=%{luacompatver} LUAINC_linux=%{_includedir}/lua-%{luacompatver} OPTFLAGS="%{optflags} -fPIC" linux
/usr/bin/iconv -f ISO8859-1 -t UTF8 LICENSE >LICENSE.UTF8
mv -f LICENSE.UTF8 LICENSE
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
make install-unix OPTFLAGS="%{optflags}" INSTALL_TOP=$RPM_BUILD_ROOT \
    INSTALL_TOP_CDIR=$RPM_BUILD_ROOT%{lualibdir} \
    INSTALL_TOP_LDIR=$RPM_BUILD_ROOT%{luapkgdir}

# install development files
install -d $RPM_BUILD_ROOT%{_includedir}/%{upstreamname}
install -p src/*.h $RPM_BUILD_ROOT%{_includedir}/%{upstreamname}

%if 0%{?fedora} >= 20
pushd %{lua51dir}
make install-unix OPTFLAGS="%{optflags}" INSTALL_TOP=$RPM_BUILD_ROOT \
    INSTALL_TOP_CDIR=$RPM_BUILD_ROOT%{luacompatlibdir} \
    INSTALL_TOP_LDIR=$RPM_BUILD_ROOT%{luacompatpkgdir}
popd
%endif

%clean
#rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*
%doc README LICENSE
%{lualibdir}/*
%{luapkgdir}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{upstreamname}

%if 0%{?fedora} >= 20
%files compat
%defattr(-,root,root,-)
%doc doc/*
%doc README LICENSE
%{luacompatlibdir}/*
%{luacompatpkgdir}/*
%endif

%changelog
* Thu May 22 2014 Jan Kaluza <jkaluza@redhat.com> - 3.0-0.5rc1
- build -compat subpackage against compat-lua

* Mon Sep 09 2013 Matěj Cepl <mcepl@redhat.com> - 3.0-0.4rc1
- Add -devel package.

* Fri Aug 23 2013 Matěj Cepl <mcepl@redhat.com> - 3.0-0.3rc1
- update to the 3.0rc1 from git

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Tom Callaway <spot@fedoraproject.org> - 2.1-0.1.rc1
- update to 2.1rc1 from git

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Matthew Garrett <mjg@redhat.com> - 2.0.2-6
- Build support for Unix domain sockets (rhbz: #720692)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Apr 05 2008 Tim Niemueller <tim@niemueller.de> - 2.0.2-2
- Pass proper CFLAGS to produce valid debuginfo
- Pass LICENSE file through iconv to produce proper UTF8

* Fri Apr 04 2008 Tim Niemueller <tim@niemueller.de> - 2.0.2-1
- Initial package

