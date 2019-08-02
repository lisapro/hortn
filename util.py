import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np


path_brom = r'E:\Users\EYA\Horten\_for_Paper\BROM_Horten_out_13c_6pl .nc'


start_time = 45300
stop_time =  -1 #46600

dist_time = 46390

baseline_col = 0
release_col = 6
cmap = plt.get_cmap('jet')
k_inj = 4 
nlev = 20

def get_levels_1_arr(arr1):

    vmin = np.min(arr1)
    vmax =  np.max(arr1)
    return np.linspace(vmin,vmax,nlev)


def get_levels(arr1,arr2):
    #nlev = utl200
    vmin = np.min((arr1,arr2))
    vmax =  np.max((arr1,arr2))
    return np.linspace(vmin,vmax,nlev)