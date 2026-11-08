Name:		doxia-sink-api
Version:	2.2.0
Release:	1
Summary:	Doxia sink API
Group:		Development/Java
License:	ASL 2.0
URL:		https://maven.apache.org/doxia/doxia/
Source0:	https://github.com/apache/maven-doxia/archive/refs/tags/doxia-%{version}.tar.gz#/doxia-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
Sink and SinkFactory interfaces used by Maven reporting and Doxia.
SinkEventAttributeSet lives in this jar. The classes import only the JDK.

%prep
%autosetup -n maven-doxia-doxia-%{version}
# The tag is the Doxia reactor. This package is only the sink API module.
# Its parent POM is that reactor, which is not packaged.
rm -rf src
mv doxia-sink-api/src src
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.doxia")
add(root, "artifactId", "doxia-sink-api")
add(root, "version", "%{version}")
add(root, "packaging", "jar")
add(root, "name", "Doxia :: Sink API")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
rm -rf doxia-core doxia-modules doxia-sink-api doxia-test-docs

%files -f .mfiles
%doc README.md
