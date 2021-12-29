%global vendor %{?_vendor:%{_vendor}}%{!?_vendor:openEuler}
%global rpmvdir /usr/lib/rpm/%{vendor}

Name:		%{vendor}-rpm-config
Version:	30
Release:	22
License:	GPL+
Summary:	specific rpm configuration files
URL:		https://gitee.com/openeuler/openEuler-rpm-config

Source0:        https://gitee.com/openeuler/openEuler-rpm-config/repository/archive/%{version}.tar.gz

Provides: python-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: python2-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: python3-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: python-srpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: fpc-srpm-macros = 1.1-6
Provides: ghc-srpm-macros = 1.4.2-8
Provides: gnat-srpm-macros = 4-6
Provides: nim-srpm-macros = 1-3
Provides: ocaml-srpm-macros = 5-4
Provides: openblas-srpm-macros = 2-4
Provides: perl-srpm-macros = 1-28
Provides: rust-srpm-macros = 10-1
Provides: go-srpm-macros = 2-18
Provides: perl-macros = 4:5.32.0-1
Obsoletes: perl-macros <= 4:5.32.0-1
Obsoletes: python-rpm-macros <= %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: python2-rpm-macros <= %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: python3-rpm-macros <= %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: python-srpm-macros <= %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: fpc-srpm-macros <= 1.1-6
Obsoletes: ghc-srpm-macros <= 1.4.2-8
Obsoletes: gnat-srpm-macros <= 4-6
Obsoletes: nim-srpm-macros <= 1-3
Obsoletes: ocaml-srpm-macros <= 5-4
Obsoletes: openblas-srpm-macros <= 2-4
Obsoletes: perl-srpm-macros <= 1-28
Obsoletes: rust-srpm-macros <= 10-1
Obsoletes: go-srpm-macros <= 2-18

%if %{vendor} != openEuler
Provides: openEuler-rpm-config = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: openEuler-rpm-config <= %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Requires: efi-srpm-macros
Requires: qt5-srpm-macros

Requires: rpm >= 4.11.0
Requires: zip
#Requires: (annobin if gcc)

# for brp-mangle-shebangs
Requires: %{_bindir}/find
Requires: %{_bindir}/file
Requires: %{_bindir}/grep
Requires: %{_bindir}/sed
Requires: %{_bindir}/xargs

# -fstack-clash-protection and -fcf-protection require GCC 8.
Conflicts: gcc < 7

Provides: system-rpm-config = %{version}-%{release}

%description
specific rpm configuration files for %{vendor}.

%package -n kernel-rpm-macros
Summary: Macros and scripts for building kernel module packages

%description -n kernel-rpm-macros
Macros and scripts for building kernel module packages.

%prep
%autosetup -n openEuler-rpm-config -p1

%install
mkdir -p %{buildroot}%{rpmvdir}
install -p -m 644 -t %{buildroot}%{rpmvdir} macros rpmrc
install -p -m 755 -t %{buildroot}%{rpmvdir} config.*
install -p -m 755 -t %{buildroot}%{_rpmconfigdir}/openEuler brp-*
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/openEuler openEuler-*
install -p -m 755 -t %{buildroot}%{rpmvdir} kmodtool.py

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d/ macros.perl macros.python macros.go macros.forge macros.kmp

mkdir -p %{buildroot}%{_fileattrsdir}

%files
%dir %{rpmvdir}
%{rpmvdir}/macros
%{rpmvdir}/rpmrc
%{_rpmconfigdir}/openEuler/brp-*
%{_rpmconfigdir}/openEuler/openEuler-*
%{rpmvdir}/config.*
%{_fileattrsdir}/
%{_rpmconfigdir}/macros.d/
%exclude %{_rpmconfigdir}/macros.d/macros.kmp

%files -n kernel-rpm-macros
%exclude %{_prefix}/lib/rpm/*/__pycache__/*
%{rpmvdir}/kmodtool.py
%{_rpmconfigdir}/macros.d/macros.kmp

%changelog
* Sat Sep 4 2021 yangmingtai <yangmingtai@huawei.com> - 30-22
- add brp scripts to delete rpath

* Thu Apr 8 2021 Anakin Zhang <benjamin93@163.com> - 30-21
- exclude kernel source and EFI files in digest list building

* Mon Mar 29 2021 shenyangyang <shenyangyang4@huawei.com> - 30-20
- Patched missing patch that remove fexceptions

* Thu Mar 25 2021 shenyangyang <shenyangyang4@huawei.com> - 30-19
- Modify support for change vendor with better method

* Thu Mar 18 2021 shenyangyang <shenyangyang4@huawei.com> - 30-18
- Change the name of spec to openEuler-rpm-spec and fix few bugs

* Thu Mar 11 2021 shenyangyang <shenyangyang4@huawei.com> - 30-17
- Add for support for change vendor

* Tue Dec 1 2020 whoisxxx <zhangxuzhou4@huawei.com> - 30-16
- Add riscv64 in macros.go

* Wed Sep 30 2020 shenyangyang <shenyangyang4@huawei.com> - 30-15
- Change the source code to tar

* Fri Aug 21 2020 Wang Shuo <wangshuo_1994@foxmail.com> - 30-14
- fix error message for kmodtool

* Thu Aug 13 2020 shenyangyang <shenyangyang4@huawei.com> - 30-13
- Add provides of perl-macros

* Thu Aug 6 2020 tianwei <tianwei12@huawei.com> - 30-12
- delete strip-file-prefix

* Mon Aug 3 2020 Anakin Zhang <benjamin93@163.com> - 30-12
- add brp-digest-list

* Wed May 6 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-10
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: disable buildid link macro

* Tue Feb 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-9
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify python_provide macro from python2 to python3

* Sun Jan 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-8
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:revise vendor in macro

* Sun Jan 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-7
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:revise macro file

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-6
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update macros file

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add macros to macros.python

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update macros.python

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:change type of files

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add source10 to package

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 30-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:rebuild

* Thu Dec 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 29-20
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:delete unneeded provides

* Wed Nov 27 2019 fanghuiyu<fanghuiyu@huwei.com> - 29-19
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:change to generic-rpm-config

* Fri Nov 15 2019 jiangchuangang<jiangchuangang@huwei.com> - 29-18
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: remove fcf-protection for x86_64 from rpmrc

* Wed Oct 30 2019 hexiaowen <hexiaowen@huawei.com> - 29-17
- add custom macros

* Wed Sep 25 2019 hexiaowen <hexiaowen@huawei.com> - 29-16
- add rust-srpm-macros and go-srpm-macros

* Fri Sep 20 2019 hexiaowen <hexiaowen@huawei.com> - 29-15
- add version-release for python-rpm-macros

* Fri Sep 20 2019 hexiaowen <hexiaowen@huawei.com> - 29-14
- add python-rpm-macros fpc-srpm-macros ghc-srpm-macros gnat-srpm-macros
- nim-srpm-macros ocaml-srpm-macros openblas-srpm-macros perl-srpm-macros

* Thu Aug 29 2019 hexiaowen <hexiaowen@huawei.com> - 29-13
- fix typo

* Tue Aug 27 2019 hexiaowen <hexiaowen@huawei.com> - 29-2
- delete annobin

* Wed Jul 18 2018 openEuler Buildteam <buildteam@openeuler.org> - 29-1
- Package init
