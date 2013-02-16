Summary:	MATE media programs
Name:		mate-media
Version:	1.5.1
Release:	1
License:	GPL v2+ and LGPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	590e6b65c46266235271ac957694f844
URL:		https://github.com/mate-desktop/mate-media
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gstreamer0.10-devel
BuildRequires:	gstreamer0.10-plugins-base-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libcanberra-devel
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	libunique-devel
BuildRequires:	mate-common
BuildRequires:	mate-doc-utils
BuildRequires:	mate-panel-devel >= 1.5
BuildRequires:	pulseaudio-devel
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.26.0
Requires(post):	desktop-file-utils
Requires(postun):	desktop-file-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a few media utilities for the MATE desktop,
including a volume control.

%prep
%setup -q

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-static \
	--enable-gstmix \
	--disable-schemas-compile \
	--disable-scrollkeeper \
	--enable-gst-mixer-applet \
	--enable-pulseaudio \
	--with-gnu-ld

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/mate-volume-control.desktop

%find_lang %{name} --with-omf --with-mate --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database
%update_icon_cache mate
%glib_compile_schemas

%postun
/sbin/ldconfig
%update_desktop_database_postun
%update_icon_cache mate
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_bindir}/mate-volume-control
%attr(755,root,root) %{_bindir}/mate-volume-control-applet
%{_sysconfdir}/xdg/autostart/mate-volume-control-applet.desktop
%{_iconsdir}/mate/*/*/*.png
%{_datadir}/mate-media
%{_datadir}/sounds/mate
%{_datadir}/glib-2.0/schemas/org.mate.volume-control.gschema.xml
%{_desktopdir}/mate-volume-control.desktop
%attr(755,root,root) %{_libdir}/mixer_applet2
%{_datadir}/dbus-1/services/org.mate.panel.applet.MixerAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.mixer.gschema.xml
%{_datadir}/mate-2.0/ui/mixer-applet-menu.xml
%{_datadir}/mate-panel/applets/org.mate.applets.MixerApplet.mate-panel-applet

# XXX proper dir
%dir %{_datadir}/mate-2.0
%dir %{_datadir}/mate-2.0/ui
