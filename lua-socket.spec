%{!?lua_version: %global lua_version %{lua: print(string.sub(_VERSION, 5))}}
%{!?lua_libdir: %global lua_libdir %{_libdir}/lua/%{lua_version}}
%{!?lua_pkgdir: %global lua_pkgdir %{_datadir}/lua/%{lua_version}}

%{!?lua_compat_version: %global lua_compat_version 5.1}
%{!?lua_compat_libdir: %global lua_compat_libdir %{_libdir}/lua/%{lua_compat_version}}
%{!?lua_compat_pkgdir: %global lua_compat_pkgdir %{_datadir}/lua/%{lua_compat_version}}
%{!?lua_compat_builddir: %global lua_compat_builddir %{_builddir}/compat-lua-%{name}-%{version}-%{release}}

Summary:        Network support for the Lua language
Name:           lua-socket
Version:        3.0
Release:        0.27.rc1%{?dist}
License:        MIT
URL:            http://www.tecgraf.puc-rio.br/~diego/professional/luasocket/
Source0:        https://github.com/diegonehab/luasocket/archive/v%{version}-rc1/luasocket-%{version}-rc1.tar.gz
Patch0:         luasocket-optflags.patch
Patch1:         luasocket-no-global-vars.patch
Patch2:         luasocket-3.0-settimeout.patch
Requires:       lua(abi) = %{lua_version}
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  lua >= %{lua_version}
BuildRequires:  lua-devel >= %{lua_version}

%description
LuaSocket is a Lua extension library that is composed by two parts: The C
core that provides support for the TCP and UDP transport layers, and the
set of Lua modules that add support for functionality commonly needed by
applications that deal with the Internet.

Among the support modules, the most commonly used implement the SMTP, HTTP
and FTP. In addition there are modules for MIME, URL handling and LTN12.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files necessary for developing and building an extension library
for Lua using lua-socket.

%if 0%{?fedora}
%package -n lua%{lua_compat_version}-socket
Summary:        Network support for the Lua %{lua_compat_version} language
Obsoletes:      lua-socket-compat < 3.0-0.28.rc1
Provides:       lua-socket-compat = %{version}-%{release}
Provides:       lua-socket-compat%{?_isa} = %{version}-%{release}
Requires:       lua(abi) = %{lua_compat_version}
BuildRequires:  compat-lua >= %{lua_compat_version}
BuildRequires:  compat-lua-devel >= %{lua_compat_version}

%description -n lua%{lua_compat_version}-socket
LuaSocket is a Lua %{lua_compat_version} extension library that is composed by two parts: The
C core that provides support for the TCP and UDP transport layers, and the
set of Lua %{lua_compat_version} modules that add support for functionality commonly needed by
applications that deal with the Internet.

Among the support modules, the most commonly used implement the SMTP, HTTP
and FTP. In addition there are modules for MIME, URL handling and LTN12.
%endif

%prep
%setup -q -n luasocket-%{version}-rc1
%patch0 -p1 -b .optflags
%patch1 -p1 -b .noglobal
%patch2 -p1 -b .settimeout

%if 0%{?fedora}
rm -rf %{lua_compat_builddir}
cp -a . %{lua_compat_builddir}
%endif

%build
%make_build linux \
  LUAV=%{lua_version} \
  LUAINC_linux=%{_includedir} \
  OPTFLAGS="$RPM_OPT_FLAGS -fPIC -DLUA_COMPAT_APIINTCASTS" \
  LDFLAGS="$RPM_LD_FLAGS -shared -o "

%if 0%{?fedora}
pushd %{lua_compat_builddir}
%make_build linux \
   LUAV=%{lua_compat_version} \
   LUAINC_linux=%{_includedir}/lua-%{lua_compat_version} \
   OPTFLAGS="$RPM_OPT_FLAGS -fPIC" \
   LDFLAGS="$RPM_LD_FLAGS -shared -o "
popd
%endif

# Convert charset of license file to UTF-8
iconv -f ISO-8859-1 -t UTF-8 -o LICENSE.UTF-8 LICENSE
touch -c -r LICENSE{,.UTF-8}
mv -f LICENSE{.UTF-8,}

%install
make install-unix INSTALL_DATA='install -p -m 644' \
  INSTALL_TOP=$RPM_BUILD_ROOT \
  INSTALL_TOP_CDIR=$RPM_BUILD_ROOT%{lua_libdir} \
  INSTALL_TOP_LDIR=$RPM_BUILD_ROOT%{lua_pkgdir}

%if 0%{?fedora}
pushd %{lua_compat_builddir}
make install-unix INSTALL_DATA='install -p -m 644' \
  INSTALL_TOP=$RPM_BUILD_ROOT \
  INSTALL_TOP_CDIR=$RPM_BUILD_ROOT%{lua_compat_libdir} \
  INSTALL_TOP_LDIR=$RPM_BUILD_ROOT%{lua_compat_pkgdir}
popd
%endif

# Install development headers
mkdir -p $RPM_BUILD_ROOT%{_includedir}/luasocket/
install -p -m 644 src/*.h $RPM_BUILD_ROOT%{_includedir}/luasocket/

%check
lua -e \
  'package.cpath="%{buildroot}%{lua_libdir}/?.so;"..package.cpath;
   package.path="%{buildroot}%{lua_pkgdir}/?.lua;"..package.path;
   dofile("test/hello.lua");'

%if 0%{?fedora}
lua-%{lua_compat_version} -e \
  'package.cpath="%{buildroot}%{lua_compat_libdir}/?.so;"..package.cpath;
   package.path="%{buildroot}%{lua_compat_pkgdir}/?.lua;"..package.path;
   dofile("test/hello.lua");'
%endif

%files
%license LICENSE
%doc NEW README doc/*
%{lua_libdir}/mime/
%{lua_libdir}/socket/
%{lua_pkgdir}/*.lua
%{lua_pkgdir}/socket/

%files devel
%{_includedir}/luasocket/

%if 0%{?fedora}
%files -n lua%{lua_compat_version}-socket
%license LICENSE
%doc NEW README doc/*
%{lua_compat_libdir}/mime/
%{lua_compat_libdir}/socket/
%{lua_compat_pkgdir}/*.lua
%{lua_compat_pkgdir}/socket/
%endif

%changelog
* Sun Jan 03 2021 Robert Scheck <robert@fedoraproject.org> 3.0-0.27.rc1
- Spec file modernization with basic %%check for Lua module
- Renamed subpackage lua-socket-compat to lua5.1-socket (for Fedora)

* Wed Sep 23 2020 Bastien Nocera <bnocera@redhat.com> - 3.0-0.26.rc1
- Fix for Lua >= 5.3 (#1873634)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.25.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 3.0-0.24.rc1
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jun 30 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0-0.23.rc1
- Rebuilt for Lua 5.4

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.22.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 29 2019 Kalev Lember <klember@redhat.com> - 3.0-0.21.rc1
- Require lua(abi) instead of just lua

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.20.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.19.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.18.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 16 2018 Rafael dos Santos <rdossant@redhat.com> - 3.0-0.17.rc1
- Use standard Fedora linker flags (bug #1548713)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.16.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.15.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.14.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.13.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-0.12.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.11.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Robert Scheck <robert@fedoraproject.org> 3.0-0.10.rc1
- Added upstream patch to fix settimeout() bug (#1220171)

* Mon May 04 2015 Robert Scheck <robert@fedoraproject.org> 3.0-0.9.rc1
- Fix broken release tag

* Fri Mar 20 2015 Bastien Nocera <bnocera@redhat.com> 3.0-0.8rc1.1
- Rebuild for new lua

* Fri Jan 16 2015 Tom Callaway <spot@fedoraproject.org> - 3.0-0.8rc1
- lua 5.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.7rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.6rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

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
