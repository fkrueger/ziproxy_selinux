%global username ziproxy

Name:           ziproxy
Version:        3.3.2
Release:        1%{?dist}
Summary:        Compressing (non-caching) web proxy
License:        GPLv2
URL:            https://github.com/%{name}/%{name}

Source0:	https://sourceforge.net/projects/%{name}/files/%{name}/%{name}-%{version}/%{name}-%{version}.tar.bz2
Source1:        ziproxy.env
Source2:        ziproxy.service
Source3:        ziproxy.firewalld.xml
Source4:        ziproxy.logrotate

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  zlib-devel
BuildRequires:	giflib-devel, libjpeg-turbo-devel, libpng-devel
BuildRequires:	jasper-devel, cyrus-sasl-devel


Requires(pre):  shadow-utils

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
#Requires:	openssl, openssl-libs, pam, ziproxy_selinux
Requires:	pam, jasper, cyrus-sasl-lib, zlib, giflib, libjpeg-turbo, libpng
%endif

%description
ziproxy is a non-caching, compressing proxy. It compresses on-the-fly images (lower qualities!), text (gz!), etc.

%prep
%setup -q

%build
autoreconf -vif
%configure --disable-runtime-loading
make %{?_smp_mflags}

sed -i 's/\/var\/ziproxy\/error/\/usr\/share\/%{name}\/error/g' etc/ziproxy/ziproxy.conf


%install
mkdir -p %{buildroot}/usr/lib/firewalld/services
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/ziproxy/sasl
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}/usr/lib/firewalld/services
mkdir -p %{buildroot}/usr/share/doc/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}/error
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}/var/log/ziproxy

install -p -m 755 -D src/ziproxy %{buildroot}%{_sbindir}/ziproxy
install -p -m 755 -D src/tools/ziproxylogtool %{buildroot}%{_bindir}/
install -p -m 755 -D src/tools/ziproxy_genhtml_stats.sh %{buildroot}%{_bindir}/

install -p -m 644 -D etc/ziproxy/bo_exception.list %{buildroot}%{_sysconfdir}/ziproxy/
install -p -m 644 -D etc/ziproxy/change_tos.list %{buildroot}%{_sysconfdir}/ziproxy/
install -p -m 644 -D etc/ziproxy/deny.list %{buildroot}%{_sysconfdir}/ziproxy/
install -p -m 644 -D etc/ziproxy/noprocess.list %{buildroot}%{_sysconfdir}/ziproxy/
install -p -m 644 -D etc/ziproxy/replace.list %{buildroot}%{_sysconfdir}/ziproxy/
install -p -m 644 -D etc/ziproxy/replace_ct.list %{buildroot}%{_sysconfdir}/ziproxy/
install -p -m 644 -D etc/ziproxy/ziproxy.conf %{buildroot}%{_sysconfdir}/ziproxy/
install -p -m 644 -D etc/ziproxy/sasl/ziproxy.conf %{buildroot}%{_sysconfdir}/ziproxy/sasl/

install -p -m 644 -D var/ziproxy/error/400.html %{buildroot}/usr/share/%{name}/error/
install -p -m 644 -D var/ziproxy/error/403.html %{buildroot}/usr/share/%{name}/error/
install -p -m 644 -D var/ziproxy/error/404.html %{buildroot}/usr/share/%{name}/error/
install -p -m 644 -D var/ziproxy/error/407.html %{buildroot}/usr/share/%{name}/error/
install -p -m 644 -D var/ziproxy/error/408.html %{buildroot}/usr/share/%{name}/error/
install -p -m 644 -D var/ziproxy/error/409.html %{buildroot}/usr/share/%{name}/error/
install -p -m 644 -D var/ziproxy/error/500.html %{buildroot}/usr/share/%{name}/error/
install -p -m 644 -D var/ziproxy/error/503.html %{buildroot}/usr/share/%{name}/error/

install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_unitdir}
install -p -m 644 -D %{SOURCE3} %{buildroot}/usr/lib/firewalld/services/%{name}.xml
install -p -m 644 -D %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/ziproxy

install -p -m 644 -D man/ziproxy.1 %{buildroot}%{_mandir}/man1/ziproxy.1
install -p -m 644 -D man/ziproxylogtool.1 %{buildroot}%{_mandir}/man1/ziproxylogtool.1

install -p -m 644 -D ChangeLog %{buildroot}/usr/share/doc/%{name}/
install -p -m 644 -D COPYING %{buildroot}/usr/share/doc/%{name}/
install -p -m 644 -D CREDITS %{buildroot}/usr/share/doc/%{name}/
install -p -m 644 -D README %{buildroot}/usr/share/doc/%{name}/
install -p -m 644 -D README.tools %{buildroot}/usr/share/doc/%{name}/
install -p -m 644 -D JPEG2000.txt %{buildroot}/usr/share/doc/%{name}/
install -p -m 644 -D THANKS %{buildroot}/usr/share/doc/%{name}/

#install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/ziproxyd
#install -p -m 644 ziproxy/white-on-black.css %{buildroot}%{_datadir}/%{name}
#install -p -m 644 ziproxy/color.css %{buildroot}%{_datadir}/%{name}
#install -p -m 644 ziproxy/monochrome.css %{buildroot}%{_datadir}/%{name}

%if 0%{?fedora} || 0%{?rhel} >= 7

# Systemd unit files
#install -p -m 644 -D %{SOURCE2} %{buildroot}%{_unitdir}/ziproxyd.service

# SystemD firewalld service file
#install -p -m 644 -D %{SOURCE4} %{buildroot}/usr/lib/firewalld/services/ziproxyd.xml


%else

# Initscripts
#install -p -m 755 -D %{SOURCE3} %{buildroot}%{_initrddir}/ziproxyd

%endif

%pre
getent group %username >/dev/null || groupadd -r %username &>/dev/null || :
getent passwd %username >/dev/null || useradd -r -s /sbin/nologin \
    -d %{_sharedstatedir}/ziproxy -M -c 'ziproxy' -g %username %username &>/dev/null || :
exit 0

%if 0%{?fedora} || 0%{?rhel} >= 7

%post
%systemd_post ziproxy.service
/usr/bin/firewall-cmd --reload >/dev/null 2>&1 || :

%preun
%systemd_preun ziproxy.service
/usr/bin/firewall-cmd --reload >/dev/null 2>&1 || :

%postun
%systemd_postun_with_restart ziproxy.service
/usr/bin/firewall-cmd --reload >/dev/null 2>&1 || :

%endif

%files
%{!?_licensedir:%global license %%doc}
%doc ChangeLog COPYING CREDITS JPEG2000.txt README README.tools THANKS
%config(noreplace) %{_sysconfdir}/sysconfig/ziproxy
%config(noreplace) %{_sysconfdir}/ziproxy/*
%{_sysconfdir}/logrotate.d/ziproxy
%{_mandir}/man1/ziproxy*.1*
%{_datadir}/%{name}
%{_datadir}/%{name}/error
%{_datadir}/%{name}/error/*
%{_bindir}/ziproxy_genhtml_stats.sh
%{_bindir}/ziproxylogtool
%{_sbindir}/ziproxy
%{_unitdir}/ziproxy.service
/usr/lib/firewalld/services/ziproxy.xml
%dir %attr(0660,ziproxy,ziproxy) /var/log/ziproxy


%changelog
* Fri Oct 20 2023 Frederic Krueger <fkrueger-dev-el8_ziproxy@holics.at> - 3.3.2-1
- Initial spec file release
