Summary:	MATE media programs
Summary(pl.UTF-8):	Programy multimedialne dla środowiska MATE
Name:		mate-media
Version:	1.26.2
Release:	1
License:	GPL v2+ (volume control, sound theme), FDL (documentation)
Group:		X11/Applications/Multimedia
Source0:	https://pub.mate-desktop.org/releases/1.26/%{name}-%{version}.tar.xz
# Source0-md5:	4202b5b5bf55f9069aff04701e19124f
URL:		https://github.com/mate-desktop/mate-media
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	libcanberra-devel >= 0.13
BuildRequires:	libcanberra-gtk3-devel >= 0.13
BuildRequires:	libmatemixer-devel >= 1.10.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	mate-common >= 1.2.1
BuildRequires:	mate-desktop-devel >= 1.17.0
BuildRequires:	mate-panel-devel >= 1.17.0
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.445
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	desktop-file-utils
Requires:	glib2 >= 1:2.50.0
Requires:	gtk+3 >= 3.22
Requires:	libcanberra >= 0.13
Requires:	libcanberra-gtk3 >= 0.13
Requires:	libmatemixer >= 1.10.0
Requires:	mate-desktop-libs >= 1.17.0
Requires:	mate-panel >= 1.17.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# use the same libexecdir as mate-panel
# (better solution: store mate-panel libexecdir in libmatepanelapplet-*.pc and read it here)
%define		matepanel_libexecdir	%{_libexecdir}/mate-panel

%description
This package contains a few media utilities for the MATE desktop,
including a volume control.

%description -l pl.UTF-8
Ten pakiet zawiera kilka narzędzi multimedialnych dla środowiska MATE,
w tym do sterowania głośnością dźwięku.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--libexecdir=%{matepanel_libexecdir} \
	--disable-schemas-compile \
	--disable-silent-rules \
	--disable-static \
	--with-gnu-ld

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{es_ES,frp,ie,jv,ku_IQ,pms}

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

%postun
%update_desktop_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-volume-control
%attr(755,root,root) %{_bindir}/mate-volume-control-status-icon
/etc/xdg/autostart/mate-volume-control-status-icon.desktop
%{_datadir}/mate-media
%{_datadir}/sounds/mate
%{_desktopdir}/mate-volume-control.desktop
%{_mandir}/man1/mate-volume-control.1*
%{_mandir}/man1/mate-volume-control-status-icon.1*
# panel applet
%attr(755,root,root) %{matepanel_libexecdir}/mate-volume-control-applet
%{_datadir}/dbus-1/services/org.mate.panel.applet.GvcAppletFactory.service
%{_datadir}/mate-panel/applets/org.mate.applets.GvcApplet.mate-panel-applet
