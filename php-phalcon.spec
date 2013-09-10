# NOTE:
# - not in pecl because php devs are morons: https://github.com/phalcon/cphalcon/issues/194
#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname	phalcon
Summary:	Web framework delivered as a C-extension for PHP
Name:		%{php_name}-%{modname}
Version:	1.2.3
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	https://github.com/phalcon/cphalcon/archive/v%{version}/%{modname}-%{version}.tar.gz
# Source0-md5:	4f112e65c5ea101bd2924ac0d1549500
URL:		http://phalconphp.com/
BuildRequires:	%{php_name}-devel
BuildRequires:	rpmbuild(macros) >= 1.666
%{?requires_php_extension}
Suggests:	%{php_name}-mbstring
Suggests:	%{php_name}-mcrypt
Suggests:	%{php_name}-openssl
Suggests:	%{php_name}-pdo
Suggests:	%{php_name}-pdo-mysql
Suggests:	%{php_name}-pdo-oci
Suggests:	%{php_name}-pdo-pgsql
Suggests:	%{php_name}-pdo-sqlite
Suggests:	%{php_name}-pecl-mongo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86}
%define	barch 32bits
%endif
%ifarch %{x8664}
%define	barch 64bits
%endif

%description
Phalcon is a web framework implemented as a C extension offering high
performance and lower resource consumption.

%prep
%setup -qn cphalcon-%{version}

%build
cd build/%{barch}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build/%{barch} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc docs/DOCUMENTATION.txt docs/LICENSE.txt
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
