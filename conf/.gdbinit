set history save
set history expansion on

#unrecognized breakpoint will result in a pending breakpoint
set breakpoint pending on

#override security restriction which may prevent loading external files/libs by executable
set auto-load safe-path /


python 
import sys
#sys.path.insert(0, '/usr/share/gcc-4.8/python') #for Ubuntu 14
sys.path.insert(0, '/usr/share/gcc-5/python')    #for Ubuntu 16
from libstdcxx.v6.printers import register_libstdcxx_printers
register_libstdcxx_printers(None)
end

handle 2 stop print pass
