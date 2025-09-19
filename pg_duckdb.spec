Name: pg_duckdb

%global pg_duckdb_version 1.0.0
%global duckdb_version 1.3.2
Version: %{pg_duckdb_version}
Release: 2%{?dist}

Summary: DuckDB-powered Postgres for high performance apps & analytics.
License: MIT
Url: https://github.com/duckdb/pg_duckdb

Patch1: duckdb_system.patch

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: git
BuildRequires: lz4-devel
BuildRequires: make
BuildRequires: postgresql-server-devel

BuildRequires: duckdb-devel = %{duckdb_version}

%description
pg_duckdb integrates DuckDB's columnar-vectorized analytics engine into PostgreSQL, enabling high-performance analytics and data-intensive applications.

%prep
git clone -q https://github.com/duckdb/pg_duckdb.git
pushd pg_duckdb
git -c advice.detachedHead=false checkout v%{pg_duckdb_version}
git rev-parse HEAD
%patch 1 -p1
popd

%build
export DUCKDB_BUILD=System
make -C pg_duckdb %{_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}/pgsql
mkdir -p %{buildroot}%{_datadir}/pgsql/extension
cp -p ./pg_duckdb/pg_duckdb.so %{buildroot}%{_libdir}/pgsql/
cp -p ./pg_duckdb/pg_duckdb.control %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./pg_duckdb/sql/pg_duckdb--1.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/

%files
%{_libdir}/pgsql/pg_duckdb.so
%{_datadir}/pgsql/extension/pg_duckdb--1.0.0.sql
%{_datadir}/pgsql/extension/pg_duckdb.control

%doc pg_duckdb/README.md
%license pg_duckdb/LICENSE

%changelog
* Fri Sep 19 2025 DuckDB Labs <alexkasko@duckdblabs.com> - 1.0.0-2
- Use system engine library

* Thu Sep 18 2025 DuckDB Labs <alexkasko@duckdblabs.com> - 1.0.0-1
- Initial package 
