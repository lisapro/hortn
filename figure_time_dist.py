'''
Script to plot Figure 
Distance Profle

'''


import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import palettable
from palettable.colorbrewer.sequential import Blues_8
from palettable import cubehelix



import numpy as np 
import xarray as xr 
import util
import numpy.ma as ma
from matplotlib import ticker
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
import seaborn as sns
sns.set_style("whitegrid")
register_matplotlib_converters()

h = 0.06
w = 0.05
sed2 = 6

def make_fig_gs(nrows,ncols):
    global fig
    fig = plt.figure(figsize=(8.27,11*nrows/5), dpi=100) 

    gs = gridspec.GridSpec(nrows, ncols) 
    gs.update(left = 0.07,right = 0.93, 
            bottom = 0.08, top = 0.95,
            wspace = 0.3, hspace= 0.35)
    return gs

def create_gs(pos):
    return gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs[pos],
                                            hspace=h,wspace=w,
                                            width_ratios = [15,1]) 
def call_create_gs(poss):
    return [create_gs(n) for n in poss]

def sbplt_cb(to_gs): 
    return [fig.add_subplot(a) for a in [to_gs[0,0],to_gs[0,1]]]

def get_df(my_path):
    return xr.open_dataset(my_path)

def get_z(df_brom,param):
    return df_brom[param][util.start_time:util.stop_time,util.k_inj,:].values #

def get_levels(z):
    levels = util.get_levels_1_arr(z[:,:])
    return levels

def plot_param_dist(param,z,axis,axis_cb):
    
    levels = get_levels(z)
    X,Y = np.meshgrid(x,y[:])  


    cmap =  plt.get_cmap('cubehelix') 

    CS_1 = axis.contourf(X,Y, z.T,cmap = cmap, levels = levels, extend="both")
    #CS_1 = axis.pcolormesh(X,Y, z[:,:].T,cmap = cmap) #levels = levels,extend="both",

    tick_locator = ticker.MaxNLocator(nbins= 'auto')
    cb = plt.colorbar(CS_1,cax = axis_cb)
    cb.locator = tick_locator
    cb.update_ticks()

    axis.set_ylim(-16,16)
    axis.set_yticks([-15,-10,-5,0,5,10,15])
    axis.tick_params(axis='y', pad = 0.01)


    myFmt = mdates.DateFormatter("%b %d ") #%H:%M
    #myFmt = mdates.DateFormatter("%d %H:%M ") #  
    axis.xaxis.set_major_formatter(myFmt)

def fig7(): #'Figure_Horten_Time_7col.png'
    global gs,x,y,y_sed,df_brom

    gs = make_fig_gs(5,1)
    df_brom = get_df(util.path_brom)
    
    gs00,gs01,gs02,gs03,gs04 = call_create_gs([0,1,2,3,4])
 
    ax00,ax00_cb = sbplt_cb(gs00)  
    ax01,ax01_cb = sbplt_cb(gs01)  
    ax02,ax02_cb = sbplt_cb(gs02)  
    ax03,ax03_cb = sbplt_cb(gs03)  
    ax04,ax04_cb = sbplt_cb(gs04)  
    import datetime 
    dt =   np.timedelta64(19,'D') + np.timedelta64(21, 'h') + np.timedelta64(43 , 'm') + np.timedelta64(11,'s')

    x = df_brom.time.values - dt   
    x = x[util.start_time:util.stop_time] #

    y = df_brom.i.values    
    y = y - y[util.release_col]


    plot_param_dist('CO2g',get_z(df_brom,'CO2g'),ax00,ax00_cb) 
    ax00.set_title(r'$CO_2 \ gas$')   

    plot_param_dist('pCO2',get_z(df_brom,'pCO2'),ax01,ax01_cb) 
    ax01.set_title(r'$pCO2\  ppm$')

    plot_param_dist('pH',get_z(df_brom,'pH'),ax02,ax02_cb) 
    ax02.set_title(r'$pH\  $')
 
    plot_param_dist('DIC',get_z(df_brom,'DIC'),ax03,ax03_cb) 
    ax03.set_title(r'$DIC\  $')

    plot_param_dist('Alk',get_z(df_brom,'Alk'),ax04,ax04_cb) 
    ax04.set_title(r'$Alk\  $')

    [axis.set_ylabel('Distance,m') for axis in [ax00,ax01,ax02,ax03,ax04]]
    ax04.set_xlabel('Month,Day')
    
    plt.savefig('Figure_Horten_Dist_Time.png')
    #plt.show()


if __name__ == '__main__':
    fig7()  
    #   
    #   #fig8()

    # To Slice:   
    #df_brom = get_df(util.path_brom)
    #df_brom = df_brom[['pCO2','DIC','Alk','pH','CO2g']]
    #df_brom = df_brom.sel(time=slice('2012-07-01', '2012-12-01'))   
    #df_brom.to_netcdf('slice_horten.nc')



    