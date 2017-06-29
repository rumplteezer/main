#     Python attempt at a simulator for a nuclear reactor

import serial as ser
import math
#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation

#     Data input from Arduino

PUP = 1100     #  Pulse Rod Position
SAP = 1100     #  Safety Rod Position
SHP = 1100         # Shim Rod Position
REP = 1100     # Reg Rod Position
#AIR = TRUE #  Air Applied to Pulse Rod
#     Variables for computation

PUR = 0.00     #  Pulse Rod Reactivity
SAR = 0.00     #  Safety Rod Reactivity
SHR = 0.00     #  Shim Rod Reactivity
RER = 0.00     #  Reg Rod Reactivity
RHO = 0.00     #  Total Reactivity

t = 0.00     #  Elapsed Time (s)..  t1-t0 from system date-time
temp = 300  #degrees K
Cp = (0.0075*temp)+17.58  #W/mK
rad = 0.1 #m
Beta = 0.0081 # Delayed neutron fraction
l = 0.000045 # seconds = prompt neutron lifetime
NU = 2.07
TU = 0.0973845
B2 = 0.0119 #  TRIGA MKII core
L2 = 2.5 # KSU core
T = 10.00    #  Reactor Period
keff = ((NU*TU)*math.exp(-B2*T))/(1+(L2*B2))
rho = ((keff)-1)/(keff)

kex = (keff - 1.0)

RP = 0.00     # Reactor Power (W)
g = 0.00     #  Blue Glow value
#SC = FALSE   #  Reactor SCRAM Setting

#     Reactivity Computations

PUR = ((2.89705e-12)*pow(PUP, 4))-((1.15066e-8)*pow(PUP, 3))+((1.25404e-5)*pow(PUP, 2))-((1.24401e-3)*(PUP))-(2.32494e-2)
SAR = ((1.12818e-12)*pow(SAP, 4))-((5.38600e-9)*pow(SAP, 3))+((5.95126e-6)*pow(SAP, 2))+((4.50633e-5)*(SAP))-(5.37668e-2)
SHR = ((1.01208e-12)*pow(SHP, 4))-((6.52850e-9)*pow(SHP, 3))+((8.94916e-6)*pow(SHP, 2))-((1.41568e-3)*(SHP))+(6.5447e-2)
RER = ((1.11050e-12)*pow(REP, 4))-((3.80753e-9)*pow(REP, 3))+((3.46334e-6)*pow(REP, 2))+((1.48608e-4)*(REP))-(4.41465e-2)
RHO = (PUR+SAR+SHR+RER)

net = ((rho) + (RHO))

power = (net / 0.00435)
if net <= 0.0000000000 :
    power = 0

#  Spot Check

print "RHO = ", RHO
print "rho = ", rho
print "net = ", net
print "keff = ", keff
print "kex = ", kex
print "power (kW) = ", power
