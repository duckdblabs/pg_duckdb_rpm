Name: pg_duckdb

%global version 1.0.0
Version: %{version}
Release: 1%{?dist}

Summary: DuckDB-powered Postgres for high performance apps & analytics.
License: MIT
Url: https://github.com/duckdb/pg_duckdb

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: git
BuildRequires: make
BuildRequires: ninja-build
BuildRequires: postgresql-server-devel

%description
pg_duckdb integrates DuckDB's columnar-vectorized analytics engine into PostgreSQL, enabling high-performance analytics and data-intensive applications.

%prep
git clone -q https://github.com/duckdb/pg_duckdb.git
cd pg_duckdb
git checkout v%{version}
git submodule update -q --init

%build
cd pg_duckdb
export PG_CFLAGS=-D_GNU_SOURCE
export DUCKDB_BUILD=ReleaseStatic
make %{_smp_mflags}

%install
cd pg_duckdb
mkdir -p %{buildroot}%{_libdir}/pgsql
mkdir -p %{buildroot}%{_datadir}/pgsql/extension
cp -p ./pg_duckdb.so %{buildroot}%{_libdir}/pgsql/
cp -p ./pg_duckdb.control %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./sql/pg_duckdb--1.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/

%files
%{_libdir}/pgsql/pg_duckdb.so
%{_datadir}/pgsql/extension/pg_duckdb--1.0.0.sql
%{_datadir}/pgsql/extension/pg_duckdb.control

%doc pg_duckdb/README.md
%license pg_duckdb/LICENSE

%changelog
* Thu Sep 18 2025 DuckDB Labs <alexkasko@duckdblabs.com> - 1.0.0-1
- Initial package 
