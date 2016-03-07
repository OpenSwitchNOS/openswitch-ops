# Show Version Detail Infrastructure

## Contents
- [Description](#description)
- [Use Cases](#use-cases)
- [Internal workings](#internal-workings)
- [Block Diagram](#block-diagram)
- [Version Detail Text File](#version-detail-text-file)
- [Source code debugging](#source-code-debugging)
- [Limitations](#limitations)

## Description
We will support a CLI "show version detail" that will list some key information for all packages included in the image.

## Use Cases
1. To provide a handy list of all packages in the image along with their versions to all users of this image.
2. To provide the source code location for every package to allow inspection/debugging of the relevant package.

## Internal workings
We use Yocto to build our images.
The runtime "package manager" functionality of Yocto uses the package*.bbclass to maintain per package metadata.
However we do not include this runtime "package manager" along with our image.
Due to this, the metadata maintained per package too is not present in the image.
Hence we have to rely on gathering this metadata during build time in order to display the desired information.
We leverage the functionality from the "package.bbclass" which is used by the package manager as well.
On the build machine, the metadata per package is gathered and stored in files (also called dictionaries) at - ${PKGDATA_DIR}.
During the packaging process, the "do_packagedata" task packages data for each recipe and installs it into this temporary, shared area. This directory defaults to the following: ${STAGING_DIR_HOST}/pkgdata
We tap into this resource to generate a "Version Detail" text file that contains the desired information per package.
This file is packaged along with the image.
When ops-sysd comes up, it reads this file and fills the information therein into the OVSDB "Package_Info" Table.
This OVSDB information is then accessed by management entities like CLI & REST to display the package information.
The implementation of "show version detail" CLI does just that.

## Block Diagram
```ditaa
+------------+         +-------+         +----------------+
|            |  init   |       |   CLI   |     ops-cli    |
|  ops-sysd  +-------->| OVSDB +-------->| (vtysh Daemon) |
|            |         |       |         |                |
+------------+         +-------+         +----------------+
          ^
          |
          |
          |
  +-------+--------+
  | version detail |
  | file ( TEXT )  |
  | /var/lib/      |
  +----------------+

```

##  Version Detail text file
This file is generated during build time after the rootfs is created and before the image is generated.
For every package present in the image, it lists the version number and the source-code path.
Based on the source-code path, the "source-type" for the package can be https, http, ftp, git, svn, cvs etc.
If the source-type is a git repository, the version will correspond to the git hash (SRCREV).
Otherwise, the version will correspond to a version string (PV).
On the build server, this file gets generated at - ${DEPLOY_DIR_IMAGE}/${IMAGE_NAME}.version_detail
It is then copied to the image at - /var/lib/version_detail

Sample contents of this file are shown below -

```ditaa
PKG=ops-openvswitch SRCREV=ac19ac49778adf6cf011a3ef6e0675025f1945b5 PV=gitAUTOINC+ac19ac4977 TYPE=git SRC_URL=https://git.openswitch.net/openswitch/ops-openvswitch

PKG=sed SRCREV=INVALID PV=4.2.2 TYPE=http SRC_URL=http://ftp.gnu.org/gnu/sed/sed-4.2.2.tar.gz
```
Note:
A few entries in this file will contain just the "PKG" & may or may not contain "PV"
For example:
```ditaa
PKG=packagegroup-base-ipv6 SRCREV=INVALID PV=1.0 TYPE=other SRC_URL=NA
```
These entries correspond to "metapackages": They exist as packages but do not actually install any files. They are used to pull in other packages through dependencies. Also the PKGSIZE for such metapackages is usually 0.

## Source code debugging
As the "show version detail" CLI output would display the source-code path (src_url), one will be able to fetch the exact codebase corresponding to the package. In case of git repositories, one would be able to fetch the exact codebase corresponding to the git-hash printed.
For example:
```ditaa
git clone <src_url>
cd <repo>/
git fetch origin <git-hash>
git reset --hard FETCH_HEAD
```

## Limitations
As the runtime "package manager" is not part of the image, we have to rely on static information gathered during build time.
Also this information is fed to the OVSDB by ops-sysd during init time.
Hence if there are hot patches or a new version of a package is installed on the running image, the OVSDB will still point to stale information present in the DB. We plan to address this when we start supporting the runtime package manager with our images.
