import numpy as np
import matplotlib.pyplot as plt

#Settlement Calculation
##Piling Properties
Us = 836      #Ultimate Shaft Capacity kN 836
Ub = 112      #Ultimate Base Capacity kN 112
Ds = 0.3      #Pile diameter m 0.3
Eb = 76500    #Soil modulus below pile base kPa (Eu/Cu=450) 76500
Ec = 31000000 #Concrete modulus kPa
Ms = 0.001    #OC Clay, 0.001-0.002 (0.004-0.0005 in soft to firm clays)
Pt = 445      #Load kN 445
Lo = 2.5      #Length without friction m 2.5
Lf = 12.5     #Length with friction m 12.5
Ke = 0.45     #Effective Lf length factor (0.45 for London Clay)
load_arr = np.linspace(0,Pt,11)

##Calculation Variables
a = Us 
b = Ds * Eb * Ub
c = Ms * Ds
d = 0.60 * Ub
e = Ds * Eb
f = e * load_arr - a * e - b
g = d * load_arr + e * c * load_arr - a * d - b * c
h = c * d * load_arr

##Rigid Settlement
del_t1 = ((-g+np.sqrt((g**2)-4*f*h))/(2*f))*1000
del_t2 = ((-g-np.sqrt((g**2)-4*f*h))/(2*f))*1000
del_t = []
for i in np.arange(len(del_t1)):
    if del_t1[i] > del_t2[i]:
        del_t.append(del_t1[i])
    else:
        del_t.append(del_t2[i])

##Elastic Shortening
del_e = []
for i in np.arange(len(load_arr)):
    if load_arr[i] <= Us:
        del_e.append(4/np.pi * (load_arr[i]*(Lo+Ke*Lf))/(Ds**2 * Ec)*1000)
    else:
        del_e.append(4/np.pi * 1/(Ds**2 * Ec) * (load_arr[i]*(Lo+Lf)-Lf*Us*(1-Ke))*1000)

##Total Settlement
del_total = [x + y for x, y in zip(del_e, del_t)]

#Plot Formatting
fig = plt.figure(1,figsize=(10,10))
ax1 = plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=2)
ax1.plot(load_arr,del_t,'g--',label='Rigid Settlement')
ax1.plot(load_arr,del_e,'b--',label='Elastic Shortening')
ax1.plot(load_arr,del_total,'r--',label='Total Settlement')
ax1.set_xlim(0,np.max(Pt))
ax1.set_ylim(np.max(del_total),0)
ax1.set_ylabel('Settlement (mm)')
ax1.set_xlabel('Load (kN)')
ax1.legend()
ax1.grid(b=True)