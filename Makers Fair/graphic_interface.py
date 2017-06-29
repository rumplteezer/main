# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 00:33:57 2017

@author: Hewitt
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial as ser

#
# Serial communication information
#
port = 'COM7' # get from Arduino program
baud = 9600
s = ser.Serial(port=port,baudrate=baud,timeout=0)

fig = plt.figure()

ax1 = fig.add_subplot(1,5,4) # full power scale
ax1.set_ylim(0,110)
ax2 = fig.add_subplot(1,5,2) # Period
ax2.set_ylim(-0.5,0.5)
ax3 = fig.add_subplot(1,5,5) # Aux Info
ax3.set_ylim(0,100)
ax4 = fig.add_subplot(1,5,1) # log power scale
ax4.set_ylim(0,100)
ax5 = fig.add_subplot(1,5,3) # liner power scale
ax5.set_ylim(0,100)


def animate(i):
    ax4_yticks_names = np.array(['1E-4','1E-3','1E-2','1E-1','1','10','100'])
    ax4_yticks = np.array([-3,-2,-1,0,1,2,3])
    per_pre = np.array([0.33,0.25,0.20,0.143,0.1,0.0667,0.05,0.033,0,-0.033])
    markers = np.array(['3 S','4 S','5 S','7 S','10 S','15 S','20 S','30 S','INF','-30 S'])
    strings = ["Power","Period","Pulse","Safety","Shim","Reg"]
    line = s.readline()
    print(line)
    x = np.shape(line.split(','))
    if x==(7L,):
        pu,sa,sh,re,po,pe,ra = line.split(',')
        po = float(po)/100
        pe = float(pe)        
        values = [po,pe,pu,sa,sh,re]
        #
        # initial graphic construction
        #
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax5.clear()
        #
        # NPP-1000
        #
        ax1.set_ylim(0,110)
        ax1.set_xlim(0,1)
        ax1.hlines(po/10,0,0.5,color='r',linewidth=4)
        #
        # Period
        #
        ax2.set_ylim(-0.04,0.35)
        ax2.set_xlim(0,1)
        if pe!=0:
            ax2.hlines(1/pe,0,0.5,color='r', linewidth=4)
        for j in range(0,len(per_pre)):
            ax2.hlines(per_pre[j],0.5,1,color='k',linewidth=1)
            ax2.text(0.7,per_pre[j],'{0}'.format(markers[j]))
        #
        # Control Rod Position, alternate power and period indication
        #
        for j in range(0,6):
                ax3.text(0.1,90-10*j,"{0}:\n{1}".format(strings[j],values[j]))
        if ((po==0) and (pe==0)):
            ax3.text(0.05,20,'REACTOR\n SCRAM',color='r',fontsize=20)
        #
        # NLW-1000 power indication
        #
        ax4.set_ylim(-3.5,3.5)
        ax4.set_xlim(0,1)
        if po == 0:
            ax4.hlines(-3.5,0,0.5,color='r',linewidth=4)
        else:
            ax4.hlines(np.log10(po),0,0.5,color='r',linewidth=4)
        for j in range(0,len(ax4_yticks)):
            ax4.text(0,ax4_yticks[j],ax4_yticks_names[j],ha='right')
        #
        # NMP-1000 power indication
        #
        ax5.set_ylim(0,110)
        ax5.set_xlim(0,1)
        if po !=0:
            log_p = np.log10(po)
            if log_p<0:
                ax5.hlines((100*10**(log_p-int(log_p))),0,0.5,color='r',linewidth=4)
            elif log_p>0:
                ax5.hlines((10*10**(log_p-int(log_p))),0,0.5,color='r',linewidth=4)
        #
        # format axes and titles
        #
        ax1.set_xticks([])
        ax2.set_xticks([])
        ax2.set_yticks([])
        ax3.set_xticks([])
        ax3.set_yticks([])
        ax4.set_xticks([])
        ax4.set_yticks([])
        ax5.set_xticks([])
        ax1.set_title('NPP-1000')
        ax2.set_title('Period')
        ax4.set_title('NLW-1000')
        ax5.set_title('NMP-1000')
    
ani = animation.FuncAnimation(fig, animate, interval = 50)
plt.show()