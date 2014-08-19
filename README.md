mock-plugin-tsflags
===================

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

```
mock -r myroot --install --enable-plugin=tsflags \
    --plugin-option tsflags:flags=nocontexts,noscripts
```
