import numpy as np
import matplotlib.pyplot as plt

class load_settlement:

    #Settlement Calculation
    ##Piling Properties
    def parameters(self):
        self.Us = 836      #Ultimate Shaft Capacity kN 836
        self.Ub = 112      #Ultimate Base Capacity kN 112
        self.Ds = 0.3      #Pile diameter m 0.3
        self.Eb = 76500    #Soil modulus below pile base kPa (Eu/Cu=450) 76500
        self.Ec = 31000000 #Concrete modulus kPa
        self.Ms = 0.001    #OC Clay, 0.001-0.002 (0.004-0.0005 in soft to firm clays)
        self.Pt = 445      #Load kN 445
        self.Lo = 2.5      #Length without friction m 2.5
        self.Lf = 12.5     #Length with friction m 12.5
        self.Ke = 0.45     #Effective Lf length factor (0.45 for London Clay)
        self.load_arr = np.linspace(0,self.Pt,11)
        
        ##Calculation Variables
        self.a = self.Us 
        self.b = self.Ds * self.Eb * self.Ub
        self.c = self.Ms * self.Ds
        self.d = 0.60 * self.Ub
        self.e = self.Ds * self.Eb
        self.f = self.e * self.load_arr - self.a * self.e - self.b
        self.g = self.d * self.load_arr + self.e * self.c * self.load_arr - self.a * self.d - self.b * self.c
        self.h = self.c * self.d * self.load_arr
    
    ##Rigid Settlement
    def rigid(self):
        self.del_t1 = ((-self.g+np.sqrt((self.g**2)-4*self.f*self.h))/(2*self.f))*1000
        self.del_t2 = ((-self.g-np.sqrt((self.g**2)-4*self.f*self.h))/(2*self.f))*1000
        self.del_t = []
        for i in np.arange(len(self.del_t1)):
            if self.del_t1[i] > self.del_t2[i]:
                self.del_t.append(self.del_t1[i])
            else:
                self.del_t.append(self.del_t2[i])
    
    ##Elastic Shortening
    def elastic(self):
        self.del_e = []
        for i in np.arange(len(self.load_arr)):
            if self.load_arr[i] <= self.Us:
                self.del_e.append(4/np.pi * (self.load_arr[i]*(self.Lo+self.Ke*self.Lf))/(self.Ds**2 * self.Ec)*1000)
            else:
                self.del_e.append(4/np.pi * 1/(self.Ds**2 * self.Ec) * (self.load_arr[i]*(self.Lo+self.Lf)-self.Lf*self.Us*(1-self.Ke))*1000)
    
    ##Total Settlement
    def total(self):    
        self.del_total = [x + y for x, y in zip(self.del_e, self.del_t)]
    
    ##Plot Formatting
    def plots(self):
        fig = plt.figure(1,figsize=(10,10))
        ax1 = plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=2)
        ax1.plot(self.load_arr,self.del_t,'g--',label='Rigid Settlement')
        ax1.plot(self.load_arr,self.del_e,'b--',label='Elastic Shortening')
        ax1.plot(self.load_arr,self.del_total,'r--',label='Total Settlement')
        ax1.set_xlim(0,np.max(self.Pt))
        ax1.set_ylim(np.max(self.del_total),0)
        ax1.set_ylabel('Settlement (mm)')
        ax1.set_xlabel('Load (kN)')
        ax1.legend()
        ax1.grid(b=True)
        
    def main(self):
        ls.rigid()
        ls.elastic()
        ls.total()
        ls.plots()

ls = load_settlement()
ls.main()
