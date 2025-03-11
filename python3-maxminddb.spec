#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_with	tests	# do not perform "make test"

%define 	module	maxminddb
Summary:	Python extension for reading the MaxMind DB format
Name:		python3-%{module}
Version:	2.5.2
Release:	3
License:	APL
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/m/maxminddb/maxminddb-%{version}.tar.gz
# Source0-md5:	b4c43becaffd76b9afa57beea19523c8
URL:		https://pypi.python.org/pypi/maxminddb
BuildRequires:	libmaxminddb-devel
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
Requires:	python-ipaddr
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python module for reading MaxMind DB files.

MaxMind DB is a binary file format that stores data indexed by IP
address subnets (IPv4 or IPv6).

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%py3_build %{?with_tests:test}

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HISTORY.rst README.rst
%{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
