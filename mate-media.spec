Summary:	MATE media programs
Name:		mate-media
Version:	1.5.1
Release:	0.3
License:	GPLv2+ and LGPLv2+
Group:		X11/Applications/Multimedia
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	590e6b65c46266235271ac957694f844
URL:		http://mate-desktop.org/
BuildRequires:	clutter-gst-devel
BuildRequires:	desktop-file-utils
BuildRequires:	mate-common
BuildRequires:	mate-control-center-devel >= 1.5
BuildRequires:	mate-doc-utils
BuildRequires:	mate-panel-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libcanberra)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(unique-1.0)
BuildRequires:	pulseaudio-devel
BuildRequires:	rarian-compat
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

#find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} ';'
#find $RPM_BUILD_ROOT -name '*.a' -exec rm -rf {} ';'

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/mate-volume-control.desktop

%find_lang %{name} --all-name

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
%{_datadir}/mate/help/mate-volume-control
%{_datadir}/omf/mate-volume-control
%attr(755,root,root) %{_libdir}/mixer_applet2
%{_datadir}/dbus-1/services/org.mate.panel.applet.MixerAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.mixer.gschema.xml
%{_datadir}/mate-2.0/ui/mixer-applet-menu.xml
%{_datadir}/mate-panel/applets/org.mate.applets.MixerApplet.mate-panel-applet
%{_datadir}/mate/help/mate-mixer_applet2
%{_datadir}/omf/mate-mixer_applet2

# XXX proper dir
%dir %{_datadir}/mate-2.0
%dir %{_datadir}/mate-2.0/ui
