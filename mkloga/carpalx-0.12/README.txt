                             ___   __
                            | \ \ / /
   ___ __ _ _ __ _ __   __ _| |\ V /
  / __/ _` | '__| '_ \ / _` | | > <
 | (_| (_| | |  | |_) | (_| | |/ . \
  \___\__,_|_|  | .__/ \__,_|_/_/ \_\
                | |
                |_| v0.12

 carpalX - keyboard layout optimizer - save your carpals

 http://mkweb.bcgsc.ca/carpalx

 Martin Krzywinski <martink@bcgsc.ca>


ORIENTATION

Lots of typing for 10 years can leave your hands looking like cranky
twigs. Moving that pinky over and over again and rotating the
wrist. Ouch. Your fingers deserve better.

carpalx is a keyboard layout optimizer. Given a training corpus
(e.g. English text) and parameters that describe typing effort,
carpalx uses simulated annealing to find a keyboard layout to minimize
typing effort.

Typing effort is modeled using three contributions

 - base effort derived from finger travel distance
 - row, hand and finger penalties to limit use of weaker fingers/hands
      and distinguish harder-to-reach keys
 - stroke path effort, a complex figure of merit that rates the effort
      based on finger, row and hand alternation (e.g. asd is much easier to
      type than sad - this is captured by the stroke path effort)


INSTALLATION

To install, untar the distribution

  > tar xcvf carpalx-x.xx.tgz
  > cd carpax-x.xx

Binaries are in bin/ and the first line of each script should be
adjusted to reflect the location of your perl binary. For example, if
you are using /usr/bin/perl, then change

  #!/home/martink/bin/perl

to

  #!/usr/bin/perl

Each script has a manpage that can be accessed using -man. For example,

  bin/generatetriads -man

For brief usage, 

  bin/generatetriads -h


CONFIGURATION

Optimization is performed by the carpalx script and all others in bin/
are utility scripts that are not necessary for carpalx. However, they
are helpful in generated useful data files (e.g. triad lists).

carpalx uses an Apache-like configuration file which defines
variable-value pairs that control the script. Several configuration
files are found in etc/ and these are discussed in the online
tutorials (etc/tutorial-xx.conf).

Documentation for carpalx is available in the form of tutorials, e.g.

  http://mkweb.bcgsc.ca/carpalx/?keyboard_statistics


EXPERIMENTATION

carpalx is a sandbox keyboard simulator - experiment, have fun and
drop me a line if you find anything interesting!
