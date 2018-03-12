%if 0%{?_no_dist}
        %undefine dist
%endif

%if "%{dist}" == ".el7.centos"
	%define dist	.el7
%endif

%define debug_package	%{nil}
%global name		cw-openssl
%global version		1.0.2n
%global release		1_2%{?dist}.cachewall
%global _prefix		/opt/cachewall/%{name}
%global _opensslconfdir	%{_prefix}/etc

Summary:	Cryptography and SSL/TLS Toolkit
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	OpenSSL
Group:		System Environment/Libraries
URL:		https://www.openssl.org/
Vendor:		OpenSSL
Provides:	%{name}
%if "%{name}" != "cw-openssl"
Provides:	cw-openssl
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:	https://www.openssl.org/source/openssl-%{version}.tar.gz
Source1:	%{name}.conf
Patch1:		openssl-1.0.2a-enginesdir.patch

%description
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library. The project is managed by a worldwide community of volunteers that use the Internet to communicate, plan, and develop the OpenSSL toolkit and its related documentation.
OpenSSL is based on the excellent SSLeay library developed by Eric Young and Tim Hudson. The OpenSSL toolkit is licensed under an Apache-style license, which basically means that you are free to get and use it for commercial and non-commercial purposes subject to some simple license conditions.

%package devel
Summary:	Files for development of applications which will use OpenSSL
Group:		Development/Libraries
Requires:	krb5-devel%{?_isa}, zlib-devel%{?_isa}
Requires:	pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%prep
%setup -q -n openssl-%{version}
%patch1 -p1 -b .enginesdir

%build
./config \
	--prefix=%{_prefix} \
	--openssldir=%{_opensslconfdir}/pki/tls \
	no-ssl2 no-ssl3 shared -fPIC

make depend
make all
make rehash
make %{?_smp_mflags}

%install
%__rm -rf %{buildroot}

%__install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d
%__install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/ld.so.conf.d

%__make INSTALL_PREFIX=%{buildroot} install

%__rm -f %{buildroot}%{_prefix}/lib64
%__rm -rf %{buildroot}%{_opensslconfdir}/pki/tls/{cert.pem,certs,misc,private}

%__ln_s %{_prefix}/lib %{buildroot}%{_prefix}/lib64
%__ln_s %{_sysconfdir}/pki/tls/cert.pem %{buildroot}%{_opensslconfdir}/pki/tls/cert.pem
%__ln_s %{_sysconfdir}/pki/tls/certs %{buildroot}%{_opensslconfdir}/pki/tls/certs
%__ln_s %{_sysconfdir}/pki/tls/misc %{buildroot}%{_opensslconfdir}/pki/tls/misc
%__ln_s %{_sysconfdir}/pki/tls/private %{buildroot}%{_opensslconfdir}/pki/tls/private

%clean
%{__rm} -rf %{buildroot}

%pre

%files
%defattr(-,root,root,-)
%dir %{_prefix}/
%{_prefix}/bin
%{_prefix}/lib
%{_prefix}/lib64
%{_opensslconfdir}
%docdir %{_prefix}/man
%config(noreplace) %{_opensslconfdir}/pki/tls/openssl.cnf
%attr(0755,root,root) %{_prefix}/lib/libcrypto.so.1.0.0
%attr(0755,root,root) %{_prefix}/lib/libssl.so.1.0.0
%dir %{_sysconfdir}/ld.so.conf.d/
%attr(0644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}.conf

%files devel
%defattr(-,root,root)
%{_prefix}/include

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Sat Mar 10 2018 Bryon Elston <bryon@cachewall.com> - 1.0.2n-1.cachewall
- Derived cw-openssl from cPanel/ea-openssl.

* Mon Feb 19 2018 Cory McIntire <cory@cpanel.net> - 1.0.2n-2
- ZC-3456: Adjust ea-openssl to build shared.

* Tue Jan 09 2018 Cory McIntire <cory@cpanel.net> - 1.0.2n-1
- EA-7086: Update ea-openssl from 1.0.2m to 1.0.2n for CVE-2017-3737

* Tue Nov 07 2017 Dan Muey <dan@cpanel.net> - 1.0.2m-3
- EA-6812: add lib64 symlink so PHP can find what it needs

* Fri Nov 03 2017 Dan Muey <dan@cpanel.net> - 1.0.2m-2
- EA-6953: fix %files so only -devel owns includes

* Thu Nov 02 2017 Cory McIntire <cory@cpanel.net> - 1.0.2m-1
- EA-6951: Update ea-openssl from 1.0.2k to 1.0.2m

* Mon Aug 14 2017 Cory McIntire <cory@cpanel.net> - 1.0.2k-7
- EA-6671: add symlinks to system default certs

* Fri Jul 14 2017 Cory McIntire <cory@cpanel.net> - 1.0.2k-6
- EA-6544: remove CloudFlare patch to stop website breakage

* Thu Jun 08 2017 Jacob Perkins <jacob.perkins@cpanel.net> - 1.0.2k-5
- Move from experimental to production
