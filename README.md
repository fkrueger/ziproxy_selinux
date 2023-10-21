This git-repo contains the files needed to create accompanying RPM files for CentOS/RHEL8 (el8), but they should work for Fedora, Alma Linux, Rocky Linux, etc. also.


# INSTALLATION via repository
The compiled SElinux policy module should also work on Fedora, and maybe even earlier versions of CentOS.

A complete version of the resulting RPM file can be found in my technoholics-repo.
It can be found here: https://dev.techno.holics.at/technoholics-repo/

## Easy installation with technoholics-repo
* Download technoholics-repo-release RPM
* Install access to the techno.holics.at repository via
yum install https://dev.techno.holics.at/technoholics-repo/el8/technoholics-repo-release-20231002-2.el8.noarch.rpm
* If needed, the gpg key used for signing the RPM packages can be found here: https://dev.techno.holics.at/holics-repo/RPM-GPG-KEY-holicsrepo
* Now install the ziproxy_selinux and preferrably our ziproxy RPM as well.
yum install ziproxy_selinux ziproxy

# Cheers!


# NAME

ziproxy\_selinux - Security Enhanced Linux Policy for the ziproxy processes

# DESCRIPTION

Security-Enhanced Linux secures the ziproxy processes via flexible
mandatory access control.

The ziproxy processes execute with the ziproxy\_t SELinux type. You
can check if you have these processes running by executing the **ps**
command with the **-Z** qualifier.

For example:

**ps -eZ | grep ziproxy\_t**

# IMPORTANT

This selinux policy was created for the ziproxy RPM supplied in RHEL 8.
It might still work with older RHEL releases, too, though.

# TODO

Create better documentation (add managed files \<-\> context overview
automatically).

# ENTRYPOINTS

The ziproxy\_t SELinux type can be entered via the
**ziproxy\_exec\_t** file type.

The default entrypoint paths for the ziproxy\_t domain are the
following:

# PROCESS TYPES

SELinux defines process types (domains) for each process running on the
system

You can see the context of a process using the **-Z** option to **psP**

Policy governs the access confined processes have to files. SELinux
ziproxy policy is very flexible allowing users to setup their
ziproxy processes in as secure a method as possible.

The following process types are defined for ziproxy:

    ziproxy_t

Note: **semanage permissive -a ziproxy\_t** can be used to make the
process type ziproxy\_t permissive. SELinux does not deny access to
permissive process types, but the AVC (SELinux denials) messages are
still generated.

# BOOLEANS

SELinux policy is customizable based on least access required. ziproxy
policy is extremely flexible and has several booleans that allow you to
manipulate the policy and run ziproxy with the tightest access
possible.

No booleans have been defined as of yet.

# MANAGED FILES

The SELinux process type ziproxy\_t can manage files labeled with the
following file types. The paths listed are the default paths for these
file types. Note the processes UID still need to have DAC permissions.

  
**ziproxy\_\*\_t**

TODO add those later, in the meantime look in the source code in ziproxy.fc

# FILE CONTEXTS

SELinux requires files to have an extended attribute to define the file
type.

You can see the context of a file using the **-Z option to lsP**

Policy governs the access confined processes have to these files.
SELinux ziproxy policy is very flexible allowing users to setup their
ziproxy processes in as secure a method as possible.

*The following file types are defined for ziproxy:*

``` 

ziproxy_exec_t
```

\- Set files with the ziproxy\_exec\_t type, if you want to transition
an executable to the ziproxy\_t domain.

Note: File context can be temporarily modified with the chcon command.
If you want to permanently change the file context you need to use the
**semanage fcontext** command. This will modify the SELinux labeling
database. You will need to use **restorecon** to apply the labels.

# COMMANDS

**semanage fcontext** can also be used to manipulate default file
context mappings.

**semanage permissive** can also be used to manipulate whether or not a
process type is permissive.

**semanage module** can also be used to enable/disable/install/remove
policy modules.

**semanage boolean** can also be used to manipulate the booleans

**system-config-selinux** is a GUI tool available to customize SELinux
policy settings.

# AUTHOR

This manual page was auto-generated using **sepolicy manpage .**

# SEE ALSO

selinux(8), semanage(8), restorecon(8), chcon(1), sepolicy(8),
setsebool(8)

