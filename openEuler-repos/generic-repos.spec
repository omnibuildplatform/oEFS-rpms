%global vendor %{?_vendor:%{_vendor}}%{!?_vendor:openEuler}

Name:           %{vendor}-repos
Version:        1.0
Release:        3.2
Summary:        %{vendor} package repositories
License:        Mulan PSL v2

Provides:       system-repos
Provides:       %{vendor}-repos
Requires:       %{vendor}-gpg-keys = %{version}-%{release}

Source2:        generic.repo
Source4:        RPM-GPG-KEY-generic
Source5:        LICENSE

%description
%{vendor} package repository files for yum and dnf along with gpg public keys

%package -n     %{vendor}-gpg-keys
Summary:        %{vendor} RPM keys

%description -n %{vendor}-gpg-keys
This package provides the RPM signature keys.


%prep

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{_sourcedir}/RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
mv $RPM_BUILD_ROOT/etc/pki/rpm-gpg/RPM-GPG-KEY-generic $RPM_BUILD_ROOT/etc/pki/rpm-gpg/RPM-GPG-KEY-%{vendor}

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d

install -m 644 %{_sourcedir}/generic.repo $RPM_BUILD_ROOT/etc/yum.repos.d/%{vendor}.repo

%files
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/%{vendor}.repo

%files -n %{vendor}-gpg-keys
/etc/pki/rpm-gpg/

%changelog
* Fri Oct 8 2021 wangchong <wangchong56@huawei.com> - 1.0-3.2
- Type:NA
- ID:NA
- SUG:NA
- DESC:fix EPOL repo error

* Thu Aug 12 2021 wangchong <wangchong56@huawei.com> - 1.0-3.1
- Type:NA
- ID:NA
- SUG:NA
- DESC:modify repo

* Thu Mar 4 2021 openEuler Buildteam <buildteam@openeuler.org> - 1.0-3.0
- Type:NA
- ID:NA
- SUG:NA
- DESC:delete unneeded GPG KEY and enable update repo

* Wed May 6 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.0-2.9
- Type:NA
- ID:NA
- SUG:NA
- DESC:modify license info in repos

* Wed Apr 29 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.0-2.8
- Type:NA
- ID:NA
- SUG:NA
- DESC:change license of mulan to v2

* Wed Apr 8 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.0-2.7
- Type:NA
- ID:NA
- SUG:NA
- DESC:modify repo

* Wed Apr 8 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.0-2.6
- Type:NA
- ID:NA
- SUG:NA
- DESC:add missing changelog

* Tue Mar 31 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.0-2.5
- Type:NA
- ID:NA
- SUG:NA
- DESC:add default repo for openEuler-20.03-LTS

* Mon Dec 23 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0-2.4
- Type:NA
- ID:NA
- SUG:NA
- DESC: delete unneeded provides

* Tue Oct 15 2019 fanghuiyu<fanghuiyu@huawei.com> - 1.0-2.3
- Type:NA
- ID:NA
- SUG:NA
- DESC: change to generic-repos

* Sun Sep 29 2019 wangcheng<wangcheng80@huawei.com> - 1.0-2.2
- Type:NA
- ID:NA
- SUG:NA
- DESC: add gpg key

* Mon Aug 26 2019 Zhuchengliang<zhuchengliang4@huawei.com> - 1.0-2.1
- Type:NA
- ID:NA
- SUG:NA
- DESC:remove sensetive info

* Thu Aug 22 2019 hexiaowen <hexiaowen@huawei.com> - 1.0-2
- add License

* Mon Aug 19 2019 shenyining<shenyining@huawei.com> - 1.0-1.6
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:correct release number

* Thu Aug 8 2019 shenyining<shenyining@huawei.com> - 1.0-1.5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:change to MIT licenses

* Fri Apr 12 2019 wangqing<wangqing54@huawei.com> - 1.0-1.4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:del post

* Fri Apr 12 2019 wangqing<wangqing54@huawei.com> - 1.0-1.3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update RPM-GPG-KEY-openEuler

* Fri Apr 12 2019 hexiaowen<hexiaowen@huawei.com> - 1.0-1.2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: delete unused key

* Mon Mar 4 2019 Shouping Wang<wangshouping@huawei.com> - 1.0-1.1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add openEuler-repo
