
%define plugin	azupdater

Name:		vuze-plugin-%plugin
Version:	1.8.10
Release:	3
Summary:	Vuze plugin: Automatic updates for external plugins
Group:		Networking/File transfer
License:	GPLv2+
URL:		http://azureus.sourceforge.net/
Source0:	http://azureus.sourceforge.net/plugins/%{plugin}_%{version}.zip
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	vuze
BuildRequires:	ant
BuildRequires:	java-rpmbuild
Requires:	vuze
BuildArch:      noarch

%description
This plugin provides automatic updates for user specific Vuze plugins
(i.e. those installed in ~/.azureus/plugins).

Note that if this package is not installed, the plugin will be
automatically downloaded from sourceforge servers on Vuze startup.

%prep
%setup -q -c
for file in *.jar; do
	unzip $file;
done
find -name '*.class' -delete

# This plugin does not have plugin.id in plugin.properties, so we provide it manually
# in the build section. Modify build.xml locally to make it work with that.
[ -e plugin.properties ] && ! grep -q plugin.id plugin.properties
sed 's,<target name="init" unless="plugin.id">,<target name="init">,' %{_datadir}/azureus/build.plugins.xml > build.xml

%build
CLASSPATH=%{_datadir}/azureus/Azureus2.jar %ant makejar -Dsource.dir=. -Dplugin.id=%plugin

%install
rm -rf %{buildroot}

install -d -m755 %{buildroot}%{_datadir}/azureus/plugins/%plugin
install -m644 %{plugin}_%{version}.jar %{buildroot}%{_datadir}/azureus/plugins/%plugin
install -m644 plugin.properties %{buildroot}%{_datadir}/azureus/plugins/%plugin

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_datadir}/azureus/plugins/%plugin
%{_datadir}/azureus/plugins/%plugin/%{plugin}_%{version}.jar
%{_datadir}/azureus/plugins/%plugin/plugin.properties


%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.8.10-2mdv2011.0
+ Revision: 615415
- the mass rebuild of 2010.1 packages

* Wed Dec 09 2009 Anssi Hannula <anssi@mandriva.org> 1.8.10-1mdv2010.1
+ Revision: 475275
- new version 1.8.10

* Sun Sep 20 2009 Anssi Hannula <anssi@mandriva.org> 1.8.8-1mdv2010.0
+ Revision: 445729
- initial Mandriva release

