%define luaver 5.2
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}
%global baseversion 3.0-rc1
%global upstreamname luasocket

Name:           lua-socket
Version:        3.0
Release:        0.3rc1%{?dist}
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

%description
LuaSocket is a Lua extension library that is composed by two parts: a C core
that provides support for the TCP and UDP transport layers, and a set of Lua
modules that add support for functionality commonly needed by applications
that deal with the Internet.

Among the support modules, the most commonly used implement the SMTP, HTTP
and FTP. In addition there are modules for MIME, URL handling and LTN12.

%prep
%setup -q -n %{upstreamname}-%{baseversion}
%patch0 -p1 -b .optflags
%patch1 -p1 -b .noglobal

%build
make %{?_smp_mflags} OPTFLAGS="%{optflags} -fPIC" linux
/usr/bin/iconv -f ISO8859-1 -t UTF8 LICENSE >LICENSE.UTF8
mv -f LICENSE.UTF8 LICENSE


%install
rm -rf $RPM_BUILD_ROOT
make install-unix OPTFLAGS="%{optflags}" INSTALL_TOP=$RPM_BUILD_ROOT INSTALL_TOP_CDIR=$RPM_BUILD_ROOT%{lualibdir} INSTALL_TOP_LDIR=$RPM_BUILD_ROOT%{luapkgdir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*
%doc README LICENSE
%{lualibdir}/*
%{luapkgdir}/*


%changelog
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

