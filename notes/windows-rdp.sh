#!/bin/bash
#set -x 

IP='192.168.122.7'

ping1() {
    ping -W1 -c1 $IP > /dev/null
}

if ! ping1
then
    sudo virsh start win-7
    echo -n Waiting for Windows to boot
    while ! ping1
    do
        echo -n .
    done
fi

for i in {1..10}
do
  sleep 1
  echo -n .
done


rdesktop -u jenia -p jeniapass -r sound:local -E -N -z -P -D -g 1920x1050 -a 32 -x b -r clipboard:PRIMARYCLIPBOARD $IP &


: <<EOF 

rdesktop: invalid option -- '-'
rdesktop: A Remote Desktop Protocol client.
Version 1.8.1. Copyright (C) 1999-2011 Matthew Chapman et al.
See http://www.rdesktop.org/ for more information.

Usage: rdesktop [options] server[:port]
   -u: user name
   -d: domain
   -s: shell / seamless application to start remotly
   -c: working directory
   -p: password (- to prompt)
   -n: client hostname
   -k: keyboard layout on server (en-us, de, sv, etc.)
   -g: desktop geometry (WxH)
   -i: enables smartcard authentication, password is used as pin
   -f: full-screen mode
   -b: force bitmap updates
   -L: local codepage
   -A: path to SeamlessRDP shell, this enables SeamlessRDP mode
   -B: use BackingStore of X-server (if available)
   -e: disable encryption (French TS)
   -E: disable encryption from client to server
   -m: do not send motion events
   -C: use private colour map
   -D: hide window manager decorations
   -K: keep window manager key bindings
   -S: caption button size (single application mode)
   -T: window title
   -t: disable use of remote ctrl
   -N: enable numlock syncronization
   -X: embed into another window with a given id.
   -a: connection colour depth
   -z: enable rdp compression
   -x: RDP5 experience (m[odem 28.8], b[roadband], l[an] or hex nr.)
   -P: use persistent bitmap caching
   -r: enable specified device redirection (this flag can be repeated)
         '-r comport:COM1=/dev/ttyS0': enable serial redirection of /dev/ttyS0 to COM1
             or      COM1=/dev/ttyS0,COM2=/dev/ttyS1
         '-r disk:floppy=/mnt/floppy': enable redirection of /mnt/floppy to 'floppy' share
             or   'floppy=/mnt/floppy,cdrom=/mnt/cdrom'
         '-r clientname=<client name>': Set the client name displayed
             for redirected disks
         '-r lptport:LPT1=/dev/lp0': enable parallel redirection of /dev/lp0 to LPT1
             or      LPT1=/dev/lp0,LPT2=/dev/lp1
         '-r printer:mydeskjet': enable printer redirection
             or      mydeskjet="HP LaserJet IIIP" to enter server driver as well
         '-r sound:[local[:driver[:device]]|off|remote]': enable sound redirection
                     remote would leave sound on server
                     available drivers for 'local':
                     libao:	libao output driver, default device: system dependent
         '-r clipboard:[off|PRIMARYCLIPBOARD|CLIPBOARD]': enable clipboard
                      redirection.
                      'PRIMARYCLIPBOARD' looks at both PRIMARY and CLIPBOARD
                      when sending data to server.
                      'CLIPBOARD' looks at only CLIPBOARD.
         '-r scard[:"Scard Name"="Alias Name[;Vendor Name]"[,...]]
          example: -r scard:"eToken PRO 00 00"="AKS ifdh 0"
                   "eToken PRO 00 00" -> Device in Linux/Unix enviroment
                   "AKS ifdh 0"       -> Device shown in Windows enviroment 
          example: -r scard:"eToken PRO 00 00"="AKS ifdh 0;AKS"
                   "eToken PRO 00 00" -> Device in Linux/Unix enviroment
                   "AKS ifdh 0"       -> Device shown in Windows enviroment 
                   "AKS"              -> Device vendor name                 
   -0: attach to console
   -4: use RDP version 4
   -5: use RDP version 5 (default)
   -o: name=value: Adds an additional option to rdesktop.
           sc-csp-name        Specifies the Crypto Service Provider name which
                              is used to authenticate the user by smartcard
           sc-container-name  Specifies the container name, this is usally the username
           sc-reader-name     Smartcard reader name to use
           sc-card-name       Specifies the card name of the smartcard to use

EOF
