%define bname gstreamer1.0

%define api	1.0
%define major	0
%define gmajor	1.0

%define libname	%mklibname gstvalidate %{api} %{major}
%define girname	%mklibname gstvalidate-gir %{gmajor}
%define devname	%mklibname gstvalidate %{api} -d

%global __python %{__python3}

Name:		%{bname}-devtools
Summary:	Suite of tools to run GStreamer1.0 integration tests
Version:	1.26.2
Release:	1
License:	LGPLv2+
Group:		Video/Utilities
Url:		https://gstreamer.freedesktop.org/
Source0:	https://gstreamer.freedesktop.org/src/gst-devtools/gst-devtools-%{version}.tar.xz
# Rust sucks
Source1:	vendor.tar.xz
BuildRequires:	gettext-devel
BuildRequires:  meson
BuildRequires:	python
BuildRequires:	rust-packaging
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(libdw)
Requires:	%{name}-scenarios >= %{version}-%{release}
Obsoletes:	gstreamer1.0-validate < 1.18.0
Provides:	gstreamer1.0-validate = %{version}-%{release}

%description
The goal of GstValidate is to be able to detect when elements are not
behaving as expected and report it to the user so he knows how things
are supposed to work inside a GstPipeline. In the end, fixing issues
found by the tool will ensure that all elements behave all together in
the expected way.

%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the shared libraries for %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{_lib}%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description -n %{devname}
This package contains the shared libraries and development files
for %{name}.

%package scenarios
Summary:	Validate scenarios for %{name}
Group:		Video/Utilities
BuildArch:	noarch

%description scenarios
This package contains the scenario files for %{name}.

%prep
%autosetup -p1 -n gst-devtools-%{version}

# Rust SUCKS
cd dots-viewer
tar xf %{S:1}
mkdir .cargo
cat >>.cargo/config.toml <<EOF

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
%meson \
	-Ddoc=%{?with_docs:enabled}%{?!with_docs:disabled} \
	--buildtype=release
%meson_build

%install
%meson_install
#we don't want these
find %{buildroot} -name "*.la" -delete

%files
%{_bindir}/gst-validate-1.0
%{_bindir}/gst-validate-images-check-1.0
%{_bindir}/gst-validate-launcher
%{_bindir}/gst-validate-media-check-1.0
%{_bindir}/gst-dots-viewer
#{_bindir}/gst-validate-transcoding-1.0
%{_libdir}/gst-validate-launcher/
# should plugins be here or somewhere else?
%{_libdir}/gstreamer-1.0/validate/libgstvalidatefaultinjection.so
#{_libdir}/gstreamer-1.0/validate/libgstvalidateflow.so
%{_libdir}/gstreamer-1.0/validate/libgstvalidategapplication.so
%{_libdir}/gstreamer-1.0/validate/libgstvalidategtk.so
%{_libdir}/gstreamer-1.0/validate/libgstvalidatessim.so
%{_libdir}/gstreamer-1.0/libgstvalidatetracer.so

%files -n %{libname}
%{_libdir}/libgstvalidate-%{api}.so.%{major}
%{_libdir}/libgstvalidate-%{api}.so.%{major}.*
%{_libdir}/libgstvalidate-default-overrides-%{api}.so.%{major}
%{_libdir}/libgstvalidate-default-overrides-%{api}.so.%{major}.*
#{_libdir}/libgstvalidatevideo-%{api}.so.%{major}
#{_libdir}/libgstvalidatevideo-%{api}.so.%{major}.*

%files -n %{girname}
%{_libdir}/girepository-1.0/GstValidate-%{gmajor}.typelib

%files -n %{devname}
%{_includedir}/gstreamer-1.0/gst/validate/
%{_libdir}/pkgconfig/gstreamer-validate-%{api}.pc
%{_datadir}/gir-1.0/GstValidate-%{gmajor}.gir
%{_libdir}/libgstvalidate-%{api}.so
%{_libdir}/libgstvalidate-default-overrides-%{api}.so
#{_libdir}/libgstvalidatevideo-%{api}.so

%files scenarios
%{_datadir}/gstreamer-1.0/validate/
