import numpy as np
import datetime
import matplotlib.pyplot as plt

def pw_pb(median25, median1020, noise_time, nbrdays, name) :
    pw25 = 20*np.log10(median25)
    pb1020 = 20*np.log10(median1020)
    pw25 -= np.min(pw25)
    pb1020 -= np.min(pb1020)

    noise_time = np.array(noise_time)

    surftime = [noise_time,noise_time]
    surfpw = [pw25,pw25+0.3]
    surfpb = [pb1020,pb1020+0.3]


    fig = plt.subplots(3, 1, figsize=(17, 15))
    ax1 = plt.subplot(3, 1, 1)

    color = list(range(len(pwhus25)))
    color = np.array(color)/nbrdays

    z_date = [color,color]

    ax1.scatter(pw25, pb1020,c=color)
    #ax1.colorbar()
    ax1.set_xlabel('Pw - Pw(min) (dB) \n Frequency between 2 and 5 Hz')
    ax1.set_ylabel('Pb - Pb(min) (dB) \n Frequency between 10 and 20 Hz')

    ax3 = plt.subplot(3, 1, 2)

    ax3.set_xlabel('Time') 
    ax3.set_ylabel('Pw - Pw(min) (dB) \n Frequency between 2 and 5 Hz') 
    ax3.contourf(surftime, surfpw,z_date)
    ax3.tick_params(axis ='y') 

    ax4 = ax3.twinx() 

    ax4.set_xlabel('Time') 
    ax4.set_ylabel('Débit (m$^3$/s)'+18*' ', color = 'blue')
    ax4.set_ylim((10,100))
    ax4.set_yticks([20,30,40,50,60,70])
    ax4.plot(gauging_time, gauging_velos, label = 'Discharge', c='blue')
    ax4.tick_params(axis ='y', labelcolor = 'blue')

    ax5 = plt.subplot(3, 1, 3)

    ax5.set_xlabel('Time') 
    ax5.set_ylabel('Pb - Pb(min) (dB) \n Frequency between 10 and 20 Hz') 
    ax5.contourf(surftime, surfpb,z_date)
    ax5.tick_params(axis ='y') 

    ax6 = ax5.twinx() 

    ax6.set_xlabel('Time') 
    ax6.set_ylabel('Débit (m$^3$/s)'+18*' ', color = 'blue')
    ax6.set_ylim((10,100))
    ax6.set_yticks([20,30,40,50,60,70])
    ax6.plot(gauging_time, gauging_velos, label = 'Discharge', c='blue')
    ax6.tick_params(axis ='y', labelcolor = 'blue')


    plt.savefig('plot_hydro\\compar_pw_pb_'+str(name)+'.png')


    plt.show()