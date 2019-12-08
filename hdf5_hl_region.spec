#
# Conditional build:
%bcond_without	fortran		# Fortran API
%bcond_with	tests		# perform "make tests" (reference dumps differ from current h5dump)
#
Summary:	High-Level Library for handling HDF5 object and region references
Summary(pl.UTF-8):	Wysokopoziomowa biblioteka do obsługi odniesień do obiektów i regionów HDF5
Name:		hdf5_hl_region
Version:	1.1.3
Release:	5
License:	BSD-like, changed sources must be marked
Group:		Libraries
Source0:	http://www.hdfgroup.uiuc.edu/ftp/pub/outgoing/NPOESS/source/hdf5_HL_REGION-%{version}.tar
# Source0-md5:	72b64bca020e8657f4e54ca7d9dfa57d
Patch0:		%{name}-shared.patch
Patch1:		%{name}-destdir.patch
Patch2:		hdf5-1.10.patch
URL:		http://www.hdfgroup.org/projects/npoess/HL_index.html
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	hdf5-devel
%{?with_fortran:BuildRequires:	hdf5-fortran-devel}
%{?with_tests:BuildRequires:	hdf5-progs}
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains C library to:
 - Get information and read data pointed to by region references
 - Create an array of region references using paths to datasets and
   corner coordinates of hyperslabs
 - Create a dataset and write data pointed to by region references
 - Copy data pointed to by region references
 - Retrieve data packed in an integer (quality flags)

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę C pozwalającą na:
 - uzyskanie informacji i odczyt danych wskazanych przez regionu
 - utworzenie tablicy wskazań regionu przy użyciu ścieżek do zbiorów
   danych i współrzędnych rogów obiektów hyperslab
 - utworzenie zbioru danych i zapis danych wskazanych przez region
 - skopiowanie danych wskazanych przez region
 - odtworzenie danych spakowanych w liczbie całkowitej (flag jakości)

%package devel
Summary:	Header files for HDF5 HL_REGION library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HDF5 HL_REGION
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	hdf5-devel

%description devel
Header files for HDF5 HL_REGION library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HDF5 HL_REGION.

%package static
Summary:	Static HDF5 HL_REGION library
Summary(pl.UTF-8):	Statyczna biblioteka HDF5 HL_REGION
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HDF5 HL_REGION library.

%description static -l pl.UTF-8
Statyczna biblioteka HDF5 HL_REGION.

%package fortran
Summary:	High-Level Fortran Library for handling HDF5 object and region references
Summary(pl.UTF-8):	Wysokopoziomowa biblioteka Fortranu do obsługi odniesień do obiektów i regionów HDF5
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description fortran
This package contains Fortran library to:
 - Get information and read data pointed to by region references
 - Create an array of region references using paths to datasets and
   corner coordinates of hyperslabs
 - Create a dataset and write data pointed to by region references
 - Copy data pointed to by region references
 - Retrieve data packed in an integer (quality flags)

%description fortran -l pl.UTF-8
Ten pakiet zawiera bibliotekę języka Fortran pozwalającą na:
 - uzyskanie informacji i odczyt danych wskazanych przez regionu
 - utworzenie tablicy wskazań regionu przy użyciu ścieżek do zbiorów
   danych i współrzędnych rogów obiektów hyperslab
 - utworzenie zbioru danych i zapis danych wskazanych przez region
 - skopiowanie danych wskazanych przez region
 - odtworzenie danych spakowanych w liczbie całkowitej (flag jakości)

%package fortran-devel
Summary:	Header files for HDF5 HL_REGION Fortran library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HDF5 HL_REGION dla Fortranu
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-fortran = %{version}-%{release}

%description fortran-devel
Header files for HDF5 HL_REGION library.

%description fortran-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HDF5 HL_REGION dla Foortranu.

%package fortran-static
Summary:	Static HDF5 HL_REGION Fortran library
Summary(pl.UTF-8):	Statyczna biblioteka HDF5 HL_REGION dla Fortranu
Group:		Development/Libraries
Requires:	%{name}-fortran-devel = %{version}-%{release}

%description fortran-static
Static HDF5 HL_REGION Fortran library.

%description fortran-static -l pl.UTF-8
Statyczna biblioteka HDF5 HL_REGION dla Fortranu.

%prep
%setup -q -n hdf5_HL_REGION-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} -j1 \
	CC="%{__cc}" \
	FC="%{_target_alias}-gfortran" \
	CCFLAGS="%{rpmcflags}" \
	FCFLAGS="%{rpmcflags}" \
	CHCK_H5FC2003="Fortran 2003 Compiler: yes" \
	HDF5_INSTALL_DIR=/usr \
	HDF5_USE_SHLIB=yes \
	LIBDIR=%{_libdir} \
	enable-fortran=yes

%if %{with tests}
%{__make} tests \
	HDF5_INSTALL_DIR=/usr
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	HDF5_INSTALL_DIR=/usr \
	enable-fortran=yes

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	fortran -p /sbin/ldconfig
%postun	fortran -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.txt doc/RELEASE.txt
%attr(755,root,root) %{_libdir}/libhdf5_hl_region.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhdf5_hl_region.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhdf5_hl_region.so
%{_libdir}/libhdf5_hl_region.la
%{_includedir}/h5hl_api.h
%{_includedir}/h5hl_region.h
%{_includedir}/hl_region_H5LRpublic.h
%{_includedir}/hl_region_H5LTpublic.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libhdf5_hl_region.a

%files fortran
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhdf5_hl_region_fortran.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhdf5_hl_region_fortran.so.0

%files fortran-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhdf5_hl_region_fortran.so
%{_libdir}/libhdf5_hl_region_fortran.la
%{_includedir}/h5hl_region.mod
%{_includedir}/hl_region_h5lr.mod
%{_includedir}/hl_region_h5lt.mod

%files fortran-static
%defattr(644,root,root,755)
%{_libdir}/libhdf5_hl_region_fortran.a
