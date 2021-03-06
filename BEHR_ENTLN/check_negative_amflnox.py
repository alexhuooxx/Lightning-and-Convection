import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.basemap import Basemap
from wrf import to_np, getvar, latlon_coords

# wrfout* filename
ncplace = '/home/xin/Desktop/BEHR_pics/1x200mol_2014/wrfout_d01_2014-06-01_19:30:00.nc'

# Range
Lat_min = 38.5; Lat_max = 43.5;
Lon_min = -102.5; Lon_max = -97.5;

# Read ncfile
ncfile = Dataset(ncplace)
lno2 = getvar(ncfile, "lno2")
lats, lons = latlon_coords(lno2)
lno2 = to_np(lno2)
lno = to_np(getvar(ncfile, "lno"))
no2 = to_np(getvar(ncfile, "no2"))
no = to_np(getvar(ncfile, "no_lnox"))
p = to_np(getvar(ncfile, "pressure"))

# Set map
def drawmap(ax,Lat_min,Lat_max,Lon_min,Lon_max):
    #define range of plot and plot provinces
    m=Basemap(llcrnrlat=Lat_min,urcrnrlat=Lat_max,llcrnrlon=Lon_min,urcrnrlon=Lon_max,resolution ='l',ax=ax)
    USAshp = '/home/xin/Research/python/shapefile/data/USA_adm_shp/USA_adm1'
    m.readshapefile(USAshp,'USA',drawbounds = True)

    parallels = np.arange(-90.,91.,1.)
    meridians = np.arange(-180.,181.,2.)
    m.drawparallels(parallels,labels=[1,0,0,1],linewidth=0.2,xoffset=0.2,fontsize=12,fontname='Arial')
    m.drawmeridians(meridians,labels=[1,0,0,1],linewidth=0.2,yoffset=0.2,fontsize=12,fontname='Arial')

    xminor_ticks = np.arange(Lon_min,Lon_max,1)
    yminor_ticks = np.arange(Lat_min,Lat_max, 1)
    ax.set_xticks(xminor_ticks, minor=True)
    ax.set_yticks(yminor_ticks, minor=True)

    return m

# Set colorbar
class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)
    def __call__(self, value, clip=None):
        # Note that I'm ignoring clipping and other edge cases here.
        result, is_scalar = self.process_value(value)
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.array(np.interp(value, x, y), mask=result.mask, copy=False)

# delta on one level(25)
def check_delta_one_level(no2,lno2,lons,lats,p,Lat_min,Lat_max,Lon_min,Lon_max):
    delta = no2 - lno2
    level = 24
    delta = delta[level,:,:]

    fig,ax = plt.subplots()
    m = drawmap(ax,Lat_min,Lat_max,Lon_min,Lon_max)
    x, y = m(to_np(lons), to_np(lats))

    p = ax.pcolormesh(x, y, delta,cmap='seismic',norm=MidpointNormalize(midpoint=0))
    clb = fig.colorbar(p,ax=ax,pad=0.02,shrink=0.95,extend='neither', orientation='vertical')
    ax.set_title('$\Delta$NO$_2$ (NO2-LNO2) \n level '+str(level+1),fontsize=15)

    plt.show()

# NO2 and LNO2 profile of one specific grid
def check_profile(lno2,no2,p):
    # get i_start and j_start
    # https://earthscience.stackexchange.com/questions/2732/how-to-get-cell-indices-from-latitude-and-longitude-in-wrf-model-grids?newreg=996285345387459ebe5a3039685f3795

    # # Target lon/lat
    # lon = -99.5
    # lat = 38.7

    # gep_file = '/public/home/njxdqx/xin/AutoWRFChem-R2SMH/WPS/geo_em.d01.nc'
    # ncfile = Dataset(gep_file)

    # xlat_m = to_np(getvar(ncfile, "XLAT_M"))
    # xlong_m = to_np(getvar(ncfile, "XLONG_M"))

    # j_parent_start,i_parent_start = np.unravel_index(\
    #     np.argmin((lon-xlong_m)**2+(lat-xlat_m)**2),xlong_m.shape)

    # i_parent_start += 1
    # j_parent_start += 1

    # print ('i_parent_start',i_parent_start,'\n','j_parent_start',j_parent_start)

    lno2 = lno2[:,181,170]*1E4
    no2 = no2[:,181,170]*1E4
    p = p[:,181,170]

    fig,ax = plt.subplots()
    l_no2 = plt.plot(no2,p,'-o',lno2,p,'-o')

    plt.xlabel('10$^{-4}$ ppmv')
    plt.ylabel('Pressure (hPa)')
    plt.legend(('NO$_2$','LNO$_2$'))

    plt.gca().invert_yaxis()
    ax.set_title('Original NO$_2$ profile of wrfout file')

    plt.show()

# profile of delta in one specific grid
def check_profiles():
    # Vaules (Unit: ppp) are generated by adding these in rProfile_WRF.m
        # if p == 11439 % this is the first negative grid in 2014-06-01, Swath52549
        #     disp('tmp_no2');
        #     disp(tmp_no2);
        #     disp('interp_no2');
        #     disp(interp_no2);
        #     disp('tmp_lno2');
        #     disp(tmp_lno2);
        #     disp('interp_lno2');
        #     disp(interp_lno2);
        # end
    #
    no2_wrf = 1E-10*np.array([0.0023,0.0034,0.0032,0.0017,0.0016,0.0003,0.0001,0.0002,0.0001,0.0001,0.0000,0.0000,0.0000,0.0000,0.0002,0.0450,0.0519,0.0402,0.0208,0.0087,0.0025,0.0007,0.0006,0.1506,0.0579,0.0049,0.0139,0.0729,0.1035,0.0392,0.0081,0.0008,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000])
    lno2_wrf = 1E-10*np.array([0.0023,0.0034,0.0032,0.0017,0.0016,0.0003,0.0001,0.0002,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0002,0.0159,0.0203,0.0354,0.0196,0.0080,0.0022,0.0006,0.0003,0.1409,0.0541,0.0046,0.0130,0.0667,0.0939,0.0339,0.0066,0.0007,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000])

    no2_interp = 1E-10*np.array([0.0014,0.0018,0.0023,0.0030,0.0034,0.0029,0.0019,0.0017,0.0014,0.0004,0.0002,0.0002,0.0002,0.0001,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0164,0.0502,0.0231,0.0053,0.0007,0.1495,0.0148,0.0037,0.0000,0.0000])
    lno2_interp = 1E-10*np.array([-0.0012,0.0009,0.0023,0.0032,0.0035,0.0030,0.0019,0.0016,0.0015,0.0006,0.0000,0.0002,0.0001,0.0000,0.0000,0.0000,0.0000,0.0001,0.0004,0.0015,0.0135,0.0220,0.0228,0.0043,0.0029,0.1408,0.0143,0.0038,0.0000,0.0003])

    wrf_level = np.array([896.2657470703125, 889.4143676757812, 880.17529296875, 868.5202026367188,\
     854.0614624023438, 835.9913940429688, 814.3046875, 791.3599853515625,\
     768.7667846679688, 746.1665649414062, 723.578125, 691.3536376953125,\
     650.5382080078125, 611.7963256835938, 575.01416015625, 540.0960693359375,\
     506.9690856933594, 475.5579528808594, 445.7876892089844, 417.5831298828125,\
     390.87445068359375, 365.5896911621094, 341.67059326171875,\
     319.05035400390625, 297.6748046875, 277.48541259765625, 258.427734375,\
     240.45138549804688, 223.506103515625, 207.5462646484375, 192.52401733398438,\
     178.39724731445312, 165.12167358398438, 152.70851135253906, 141.23046875,\
     130.68377685546875, 120.99507904052734, 112.09407043457031,\
     103.91685485839844])

    behr_level = np.array([1020, 1015, 1010, 1005, 1000, 990, 980, 970, 960, 945, 925, 900, 875, 850, 825, 800, 770, 740, 700, 660, 610, 560, 500, 450, 400, 350, 280, 200, 120, 60])

    delta_no2_wrf = no2_wrf - lno2_wrf
    delta_no2_interp  = no2_interp - lno2_interp

    fig,ax = plt.subplots()

    plt.plot(delta_no2_wrf*1E10,wrf_level,'-o',markersize=4)
    plt.plot(delta_no2_interp*1E10,behr_level,'-o',markersize=4)

    plt.xlabel('10$^{-4}$ ppmv')
    plt.ylabel('Pressure (hPa)')
    plt.legend(('WRF','Interp'))

    plt.gca().invert_yaxis()
    ax.set_title('$\Delta$ NO$_2$ (NO$_2$-LNO$_2$)')

    plt.show()
 
    plt.plot(no2_wrf*1E10,wrf_level,'-o',markersize=4,color='darkblue')
    plt.plot(no2_interp*1E10,behr_level,'--o',markersize=4,color='dodgerblue')
    plt.plot(lno2_wrf*1E10,wrf_level,'-o',markersize=4,color='darkred')
    plt.plot(lno2_interp*1E10,behr_level,'--o',markersize=4,color='darkorange')
    
    plt.xlabel('10$^{-4}$ ppmv')
    plt.ylabel('Pressure (hPa)')
    plt.legend(('NO$_2$','Interp_NO2','LNO$_2$','Interp_LNO$_2$'))

    plt.gca().invert_yaxis()
    ax.set_title('Profiles')
    plt.show()

check_delta_one_level(no2,lno2,lons,lats,p,Lat_min,Lat_max,Lon_min,Lon_max)
check_profile(lno2,no2,p)
check_profiles()