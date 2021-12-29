#
# Copyright (C) 2019-2021 VMware, Inc. All Rights Reserved.
#
# Licensed under the GNU General Public License v2 (the "License");
# you may not use this file except in compliance with the License. The terms
# of the License are located in the COPYING file of this distribution.
#
# tdnf spec file
#
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%define _libdirorig %{_libdir}
%define _libdir /usr/lib
%define _tdnfpluginsdir %{_libdir}/%{name}-plugins


Summary:        dnf/yum equivalent using C libs
Name:           tdnf
Version:        3.2.3
Release:        1
Vendor:         VMware, Inc.
Distribution:   Photon
License:        LGPLv2.1,GPLv2
URL:            https://github.com/vmware/tdnf
Group:          Applications/RPM

Requires:       rpm-libs
Requires:       curl
Requires:       %{name}-cli-libs = %{version}-%{release}
Requires:       libsolv

BuildRequires:  popt-devel
BuildRequires:  rpm-devel
BuildRequires:  openssl-devel
BuildRequires:  libsolv-devel
BuildRequires:  curl-devel
BuildRequires:  libmetalink-devel

#plugin repogpgcheck
BuildRequires:  gpgme-devel
BuildRequires:  cmake
BuildRequires:  python3-devel
BuildRequires:  systemd

BuildRequires:  createrepo_c
BuildRequires:  glib
BuildRequires:  libxml2

Obsoletes:      yum
Provides:       yum

Source0:        %{name}-%{version}.tar.gz

%description
%{name} is a yum/dnf equivalent which uses libsolv and libcurl

%package    devel
Summary:    A Library providing C API for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   libsolv-devel

%description devel
Development files for %{name}

%package	cli-libs
Summary:	Library providing cli libs for %{name} like clients
Group:		Development/Libraries

%description cli-libs
Library providing cli libs for %{name} like clients.

%package	plugin-repogpgcheck
Summary:	%{name} plugin providing gpg verification for repository metadata
Group:		Development/Libraries
Requires:   gpgme

%description plugin-repogpgcheck
%{name} plugin providign gpg verification for repository metadata

%package	python
Summary:	python bindings for %{name}
Group:		Development/Libraries
Requires:   python3

%description python
python bindings for %{name}

%package automatic
Summary:        %{name} - automated upgrades
Requires:       %{name} = %{version}-%{release}
%{?systemd_requires}

%description automatic
Systemd units that can periodically download package upgrades and apply them.

%prep
%autosetup

%build
mkdir -p build && cd build
cmake \
-DCMAKE_BUILD_TYPE=Debug \
-DCMAKE_INSTALL_PREFIX=%{_prefix} \
-DCMAKE_INSTALL_LIBDIR:PATH=lib \
-DSYSTEMD_DIR=%{_unitdir} \
..
make %{?_smp_mflags} && make python


%install
cd build && make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.a' -delete
ls -R %{buildroot}/etc
mkdir -p %{buildroot}/var/cache/%{name}
ln -sf %{_bindir}/%{name} %{buildroot}%{_bindir}/yum
ln -sf %{_bindir}/%{name} %{buildroot}%{_bindir}/tyum
mv %{buildroot}/usr/lib/pkgconfig/tdnfcli.pc %{buildroot}/usr/lib/pkgconfig/%{name}-cli-libs.pc
mkdir -p %{buildroot}/%{_tdnfpluginsdir}/tdnfrepogpgcheck
mv %{buildroot}/%{_tdnfpluginsdir}/libtdnfrepogpgcheck.so %{buildroot}/%{_tdnfpluginsdir}/tdnfrepogpgcheck/libtdnfrepogpgcheck.so

pushd python
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
popd
find %{buildroot} -name '*.pyc' -delete

# Pre-install
%pre
# First argument is 1 => New Installation
# First argument is 2 => Upgrade

# Post-install
%post
# First argument is 1 => New Installation
# First argument is 2 => Upgrade
/sbin/ldconfig

%triggerin -- motd
[ $2 -eq 1 ] || exit 0
if [ $1 -eq 1 ]; then
  echo "detected install of tdnf/motd, enabling tdnf-cache-updateinfo.timer" >&2
  systemctl enable %{name}-cache-updateinfo.timer >/dev/null 2>&1 || :
  systemctl start %{name}-cache-updateinfo.timer >/dev/null 2>&1 || :
elif [ $1 -eq 2 ]; then
  echo "detected upgrade of tdnf, daemon-reload" >&2
  systemctl daemon-reload >/dev/null 2>&1 || :
fi

# Pre-uninstall
%preun
# First argument is 0 => Uninstall
# First argument is 1 => Upgrade
%triggerun -- motd
[ $1 -eq 1 ] && [ $2 -eq 1 ] && exit 0
echo "detected uninstall of tdnf/motd, disabling tdnf-cache-updateinfo.timer" >&2
systemctl --no-reload disable %{name}-cache-updateinfo.timer >/dev/null 2>&1 || :
systemctl stop %{name}-cache-updateinfo.timer >/dev/null 2>&1 || :
rm -rf /var/cache/%{name}/cached-updateinfo.txt

# Post-uninstall
%postun
/sbin/ldconfig
# First argument is 0 => Uninstall
# First argument is 1 => Upgrade

%triggerpostun -- motd
[ $1 -eq 1 ] && [ $2 -eq 1 ] || exit 0
echo "detected upgrade of tdnf/motd, restarting tdnf-cache-updateinfo.timer" >&2
systemctl try-restart %{name}-cache-updateinfo.timer >/dev/null 2>&1 || :

%post cli-libs
# First argument is 1 => New Installation
# First argument is 2 => Upgrade
/sbin/ldconfig

%postun cli-libs
/sbin/ldconfig
# First argument is 0 => Uninstall
# First argument is 1 => Upgrade

%post automatic
%systemd_post %{name}-automatic.timer
%systemd_post %{name}-automatic-notifyonly.timer
%systemd_post %{name}-automatic-install.timer

%preun automatic
%systemd_preun %{name}-automatic.timer
%systemd_preun %{name}-automatic-notifyonly.timer
%systemd_preun %{name}-automatic-install.timer

%postun automatic
%systemd_postun_with_restart %{name}-automatic.timer
%systemd_postun_with_restart %{name}-automatic-notifyonly.timer
%systemd_postun_with_restart %{name}-automatic-install.timer

%files
%defattr(-,root,root,0755)
%{_bindir}/%{name}
%{_bindir}/tyum
%{_bindir}/yum
%{_bindir}/%{name}-cache-updateinfo
%{_libdir}/libtdnf.so.*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_unitdir}/%{name}-cache-updateinfo.service
%{_unitdir}/%{name}-cache-updateinfo.timer
%{_sysconfdir}/motdgen.d/02-%{name}-updateinfo.sh
%dir /var/cache/%{name}
%{_datadir}/bash-completion/completions/%{name}

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*.h
%{_libdir}/libtdnf.so
%{_libdir}/libtdnfcli.so
%exclude %{_libdir}/debug
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-cli-libs.pc

%files cli-libs
%defattr(-,root,root)
%{_libdir}/libtdnfcli.so.*

%files plugin-repogpgcheck
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}/pluginconf.d
%config(noreplace) %{_sysconfdir}/%{name}/pluginconf.d/tdnfrepogpgcheck.conf
%{_tdnfpluginsdir}/tdnfrepogpgcheck/libtdnfrepogpgcheck.so

%files python
%defattr(-,root,root)
%{_libdirorig}64/python3.8/site-packages*

%files automatic
%defattr(-,root,root,0755)
%{_bindir}/%{name}-automatic
%config(noreplace) %{_sysconfdir}/%{name}/automatic.conf
%{_unitdir}/%{name}-automatic.timer
%{_unitdir}/%{name}-automatic.service
%{_unitdir}/%{name}-automatic-install.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-notifyonly.service
