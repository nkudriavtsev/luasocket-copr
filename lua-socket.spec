%define luaver 5.1
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}

Name:           lua-socket
Version:        2.0.2
Release:        9%{?dist}
Summary:        Network support for the Lua language

Group:          Development/Libraries
License:        MIT
URL:            http://www.tecgraf.puc-rio.br/~diego/professional/luasocket/
Source0:        http://luaforge.net/frs/download.php/2664/luasocket-2.0.2.tar.gz
Patch0:		lua-socket-unix-sockets.patch
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
%setup -q -n luasocket-%{version}
%patch0 -p1 -b .unix

%build
make %{?_smp_mflags} CFLAGS="%{optflags} -fPIC"
/usr/bin/iconv -f ISO8859-1 -t UTF8 LICENSE >LICENSE.UTF8
mv -f LICENSE.UTF8 LICENSE


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_TOP_LIB=$RPM_BUILD_ROOT%{lualibdir} INSTALL_TOP_SHARE=$RPM_BUILD_ROOT%{luapkgdir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*
%doc README LICENSE
%{lualibdir}/*
%{luapkgdir}/*


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 10 2011 Matthew Garrett <mjg@redhat.com> - 2.0.2-6
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

