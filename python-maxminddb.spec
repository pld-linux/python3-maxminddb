#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	maxminddb
Summary:	Python extension for reading the MaxMind DB format
Name:		python-%{module}
Version:	1.1.1
Release:	13
License:	APL
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/m/maxminddb/maxminddb-%{version}.tar.gz
# Source0-md5:	70a6d2a4b70f08e5b509fbb83f239795
URL:		https://pypi.python.org/pypi/maxminddb
BuildRequires:	libmaxminddb-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-modules
%endif
Requires:	python-ipaddr
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python module for reading MaxMind DB files.

MaxMind DB is a binary file format that stores data indexed by IP
address subnets (IPv4 or IPv6).

%package -n python3-%{module}
Summary:	Python extension for reading the MaxMind DB format
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
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
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%py_build %{?with_tests:test}
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc HISTORY.rst README.rst
%dir %{py_sitedir}/maxminddb
%{py_sitedir}/maxminddb/*.py[co]
%attr(755,root,root) %{py_sitedir}/maxminddb/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc HISTORY.rst README.rst
%{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/*
%endif
