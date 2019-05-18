CLICOL PLUGIN EXTRAS
====================
Plugins for clicol which help troubleshooting
These plugins have external dependencies

### Example

# macvendor

     1    000a.b82d.10e0(Cisco Systems, Inc)    DYNAMIC     Fa0/16
     1    0012.80b6.4cd8(Cisco Systems, Inc)    DYNAMIC     Fa0/3
     1    0012.80b6.4cd9(Cisco Systems, Inc)    DYNAMIC     Fa0/16

### Configuration

In `~/.clicol/plugins.cfg` there must be a section for the plugin.

Example with defaults:

     # MAC vendor lookup
     [macvendor]
     # disable until not configured
     active=no
     # view (append|inline)
     #outtype=inline
     
