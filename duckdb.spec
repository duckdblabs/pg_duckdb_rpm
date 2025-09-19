Name: duckdb

%global duckdb_version 1.3.2
Version: %{duckdb_version}
Release: 1%{?dist}

Summary: high-performance analytical database system
License: MIT
Url: https://github.com/duckdb/pg_duckdb

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: git
BuildRequires: make

%description
DuckDB is a high-performance analytical database system.

%package devel
Summary: DuckDB developemnt files
Requires: duckdb%{?_isa} = %{version}-%{release}
%description devel
Development files.

%prep
git clone -q https://github.com/duckdb/pg_duckdb.git
git clone -q https://github.com/duckdb/duckdb.git
cd duckdb
git -c advice.detachedHead=false checkout v%{duckdb_version}

%build
#%global _lto_cflags %nil
cd duckdb
export CMAKE_BUILD_PARALLEL_LEVEL=%{_smp_mflags}
export ENABLE_EXTENSION_AUTOLOADING=1
export ENABLE_EXTENSION_AUTOINSTALL=1
export EXTENSION_CONFIGS=../pg_duckdb/third_party/pg_duckdb_extensions.cmake
make release

%install
cd duckdb
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
cp ./build/release/src/libduckdb.so %{buildroot}%{_libdir}/
cp -r ./src/include/* %{buildroot}%{_includedir}/

%files
%{_libdir}/libduckdb.so
%doc duckdb/README.md
%license duckdb/LICENSE

%files devel
%{_includedir}/*

%changelog
* Thu Sep 18 2025 DuckDB Labs <alexkasko@duckdblabs.com> - 1.3.2-1
- Initial package 
