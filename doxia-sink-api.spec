Name:		doxia-sink-api
Version:	2.0.0
Release:	1
Summary:	Doxia sink API
Group:		Development/Java
License:	ASL 2.0
URL:		https://maven.apache.org/doxia/doxia/
Source0:	https://github.com/apache/maven-doxia/archive/refs/tags/doxia-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
Sink and SinkFactory interfaces used by Maven reporting and Doxia.
The classes import only the JDK.

%prep
%autosetup -n maven-doxia-doxia-%{version}
# The tag is the Doxia reactor. This package is only the sink API module.
# Its parent POM is that reactor, which is not packaged.
rm -rf src
mv doxia-sink-api/src src
python - <<PY
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)
root = ET.Element("{%s}project" % NS)
ET.SubElement(root, "{%s}modelVersion" % NS).text = "4.0.0"
ET.SubElement(root, "{%s}groupId" % NS).text = "org.apache.maven.doxia"
ET.SubElement(root, "{%s}artifactId" % NS).text = "doxia-sink-api"
ET.SubElement(root, "{%s}version" % NS).text = "%{version}"
ET.SubElement(root, "{%s}packaging" % NS).text = "jar"
ET.SubElement(root, "{%s}name" % NS).text = "Doxia :: Sink API"
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
rm -rf doxia-core doxia-modules doxia-sink-api doxia-test-docs

%files -f .mfiles
%doc README.md
