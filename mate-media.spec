#
# Conditional build:
%bcond_with	gst		# enable gstreamer mixer (breaks pulseaudio unmute)
%bcond_with	gtk3		# use GTK+ 3.x instead of 2.x

Summary:	MATE media programs
Summary(pl.UTF-8):	Programy multimedialne dla środowiska MATE
Name:		mate-media
Version:	1.8.0
Release:	3
License:	LGPL v2+ (gst-mixer parts), GPL v2+ (volume control, sound theme), FDL (documentation)
Group:		X11/Applications/Multimedia
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	829b4a8717511a086f8b30cb6d712ad6
Patch0:		uidir.patch
URL:		https://github.com/mate-desktop/mate-media
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gstreamer0.10-devel >= 0.10.23
BuildRequires:	gstreamer0.10-plugins-base-devel >= 0.10.23
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.24.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libcanberra-devel >= 0.13
%{!?with_gtk3:BuildRequires:	libcanberra-gtk-devel >= 0.13}
%{?with_gtk3:BuildRequires:	libcanberra-gtk3-devel >= 0.13}
BuildRequires:	libtool >= 1:1.4.3
%{!?with_gtk3:BuildRequires:	libunique-devel >= 1.0}
%{?with_gtk3:BuildRequires:	libunique3-devel >= 3.0}
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	mate-common >= 1.2.1
BuildRequires:	mate-desktop-devel >= 1.7.3
BuildRequires:	mate-panel-devel >= 1.7.0
BuildRequires:	pulseaudio-devel >= 0.9.16
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	desktop-file-utils
Requires:	glib2 >= 1:2.26.0
Requires:	gstreamer0.10 >= 0.10.23
Requires:	gstreamer0.10-audiosink-alsa
Requires:	gstreamer0.10-plugins-base >= 0.10.23
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.24.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Requires:	gtk-update-icon-cache
Requires:	libcanberra >= 0.13
%{!?with_gtk3:Requires:	libcanberra-gtk >= 0.13}
%{?with_gtk3:Requires:	libcanberra-gtk3 >= 0.13}
Requires:	mate-desktop-libs >= 1.7.3
Requires:	mate-icon-theme
Requires:	mate-panel >= 1.7.0
Requires:	pulseaudio-libs >= 0.9.16
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/mate-panel

%description
This package contains a few media utilities for the MATE desktop,
including a volume control.

%description -l pl.UTF-8
Ten pakiet zawiera kilka narzędzi multimedialnych dla środowiska MATE,
w tym do sterowania głośnością dźwięku.

%prep
%setup -q
%patch0 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable gst gst-mixer} \
	--enable-pulseaudio \
	--disable-schemas-compile \
	--disable-silent-rules \
	--disable-static \
	--with-gnu-ld \
	%{?with_gtk3:--with-gtk=3.0}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with gst}
# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-volume-control.convert
%endif

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/mate-volume-control.desktop

%find_lang %{name} --with-mate --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache mate
%glib_compile_schemas

%postun
%update_desktop_database
%update_icon_cache mate
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-volume-control
%attr(755,root,root) %{_bindir}/mate-volume-control-applet
/etc/xdg/autostart/mate-volume-control-applet.desktop
%{_datadir}/mate-media
%{_datadir}/sounds/mate
%{_desktopdir}/mate-volume-control.desktop
%{_mandir}/man1/mate-volume-control.1*
%{_mandir}/man1/mate-volume-control-applet.1*

%if %{with gst}
%attr(755,root,root) %{_libdir}/mate-panel/mixer_applet2
%{_datadir}/dbus-1/services/org.mate.panel.applet.MixerAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.mixer.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.volume-control.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.applets.MixerApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/mixer-applet-menu.xml
%{_iconsdir}/mate/16x16/devices/gvc-*.png
%{_iconsdir}/mate/16x16/status/audio-input-microphone-muted.png
%endif
