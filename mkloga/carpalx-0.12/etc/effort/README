
################################################################
#
# The typing effort model is based on calculating typing effort of
# triads (adjacent three-character combinations). 
#
# effort = k1*effort(x)*[1 + effort(y)*(k2 + k3*effort(z))] + k4*patheffort(x,y,z)
#
# For details, see http://mkweb.bcgsc.ca/carpalx/?typing_effort
#
# The following parameters are used
#
# k1..k3 - contribution (geometric) of each character in the triad
# 
#        - character 1 contributes k1
#        - character 2 contributes k1*k2
#        - character 3 contributes k1*k2*k3
#
# k4     - contribution of stroke path to total effort
#
# A variety of penalties (e.g. finger, row, hand) are found in
# effort/weight/*
#
# The efforts associated with each stroke path are found in effort/path/*
#
# The baseline effort for typing each key are found in base/*. These
# values are based on physical distance of finger travel on a stanard
# QWERTY keyboard.
#
