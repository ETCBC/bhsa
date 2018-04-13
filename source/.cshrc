umask 022

set noclobber

if { tty -s } then

   stty erase  ^H
   stty kill   ^U
   stty werase ^W

   set fignore	= .o
   set filec
   set history	= 40
   set ignoreeof

   source ~/.alias

   cd

endif
