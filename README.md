mock-plugin-tsflags
===================

This plugin will append "--setopt=tsflags" to every yum call, the flags are specified using --plugin-option tsflags:flags=foo,bar.
This can be useful to skip %-scripts when (un-)installing packages.

Please note that this plugin conflicts with the selinux-plugin.

## Why?

redhat's glusterfs 3.4.0.57rhs-1 includes a %pretrans scriptlet written in lua. Unfortunately the return value of os.execute has changed between lua 5.1.4 (which is included in RHEL6) and 5.2.2 (provided by Fedora20), so mock won't install the glusterfs package. See:

```lua
ok, how, val = os.execute("/bin/date")
print(type(ok))
--[[
    lua 5.1.4 returns "number"
    lua 5.2.2 returns "boolean"
--]]
```

## Install

copy the tsflags.py to your mock-plugin directory, usually something like
/usr/lib/python2.7/site-packages/mockbuid/plugins/

## Usage

### command line

```
mock -r myroot --install --disable-plugin=selinux --enable-plugin=tsflags \
    --plugin-option tsflags:flags=nocontexts,noscripts
```

### mock config
```
config_opts['plugin_conf']['selinux_enable'] = False
config_opts['plugin_conf']['tsflags_enable'] = True
config_opts['plugin_conf']['tsflags_opts']['flags'] = "nocontexts,noscripts"
```

