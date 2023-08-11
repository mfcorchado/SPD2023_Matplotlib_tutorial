from sunkit_instruments import iris      # used to open IRIS data into a sunpy.map object
import sunpy.map as smap                 # used to work with sunpy.map objects
import numpy as np                       # used to manipulate N-D arrays 
import matplotlib.pyplot as plt          # used to create and manipulate figures and axes
import matplotlib.animation as animation # used to create and manipulate animation

datadir  = '/Users/maco7096/Documents/CU/2022-2023/DS2_WORKSHOP/Presentation/data/'
outdir   = '/Users/maco7096/Documents/CU/2022-2023/DS2_WORKSHOP/Presentation/media/'
dataname = 'iris_l2_20170910_125947_3660109533_SJI_1330_t000.fits'

sjiMap = iris.SJI_to_sequence(datadir+dataname)
sjiMap_arr = sjiMap.as_array()

median_int = np.zeros(sjiMap_arr[0,0,:].shape,dtype = float)
intensity  = np.zeros(sjiMap_arr[0,0,:].shape,dtype = float)
obsr_time  = np.zeros(sjiMap_arr[0,0,:].shape,dtype = 'U23')

for i in range(len(sjiMap_arr[0,0,:])): 
    median_int[i] = np.median(sjiMap_arr[:,:,i][sjiMap_arr[:,:,i]>=0])
    intensity[i]  = sjiMap_arr[:,:,i][sjiMap_arr[:,:,i]>=0].sum()
    obsr_time[i]  = sjiMap[i].date.value

def updatefig(i,sjiMap_arr,median_int,obsr_time):
    plt.close('all')
    fig,axs = plt.subplots(1,2,figsize=(10,5),subplot_kw={"projection": sjiMap[i].wcs})

    sub1 = axs[0]
    sub2 = axs[1]

    sub1.set_xlabel('Solar-X [arcsec]')
    sub2.set_xlabel('Solar-X [arcsec]')

    sub1.set_ylabel('Solar-Y [arcsec]')
    sub2.set_ylabel('Solar-Y [arcsec]')

    sub1.set_title('IRIS 1330 Å SJI')
    sub2.set_title('IRIS 1330 Å SJI in Log-space')

    fig.suptitle(f'Obsevation time: {obsr_time[i]}',fontsize = 20)

    sub1.imshow(sjiMap_arr[:,:,i],origin='lower',vmin= 0,vmax =50,cmap = sjiMap[0].cmap)
    sub2.imshow(np.log10(sjiMap_arr[:,:,i]),origin='lower',vmin= 0,vmax =3,cmap = sjiMap[0].cmap)
    
    plt.savefig(outdir+'/flare_plots/20170910_flare_'+str(i).zfill(4)+'.png')
    plt.close('all')

imin = 0  

for i in range(imin,len(obsr_time)): 
    updatefig(i,sjiMap_arr,median_int,obsr_time)
