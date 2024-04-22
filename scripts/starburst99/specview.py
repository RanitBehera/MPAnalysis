# Ranit Behera
# ranit.behera@iucaa.in

"""
This script is a GUI base tool
to analyse spectrum outputs of Starburst99.
Currently supported files are
    spectrum, hires, ifaspec, ovi, uvlines
"""

import os,pathlib
import numpy
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from matplotlib.widgets import Slider
from enum import Enum
from scipy.optimize import curve_fit


# PATHS : --- Set paths to "go_galaxy" here for various models 
GO_DEFAULT      = "/home/ranitbehera/MyDrive/Repos/Starburst99/galaxy/myoutputs/sb99_default/go_galaxy"
GO_BURST        = "/home/ranitbehera/MyDrive/Repos/Starburst99/galaxy/myoutputs/burst/go_galaxy"
GO_CONTINUOUS   = "/home/ranitbehera/MyDrive/Repos/Starburst99/galaxy/myoutputs/continuous/go_galaxy"
GO_LOWERM       = "/home/ranitbehera/MyDrive/Repos/Starburst99/galaxy/myoutputs/out_lowerm/go_galaxy"
GO_CHAB_GAL     = "/home/ranitbehera/MyDrive/Repos/Starburst99/galaxy/myoutputs/out_imf/chab_galdisk/go_galaxy"
GO_CHAB_GLOB    = "/home/ranitbehera/MyDrive/Repos/Starburst99/galaxy/myoutputs/out_imf/chab_globular/go_galaxy"
GO_KROP_BIN    = "/home/ranitbehera/MyDrive/Repos/Starburst99/galaxy/myoutputs/out_imf/kroupa_binary/go_galaxy"
# -----------------------------------------------


# FILE MANAGEMENT : ---
class MODELDIR:
    def __init__(self,go_galaxy_dirpath,next=None) -> None:
        with open(go_galaxy_dirpath) as fp:
            lines = fp.readlines()
            header={}
            for line in lines:
                if line[0]=='#' : continue
                if not line[0:3]=="set" : continue
                line = (line.split("set")[-1]).strip()
                key,value = line.split("=")        
                header[key] = value
            del lines

        self.OUT_DIR     = header["drun"]
        self.FILE_NAME   = header["noutput"]
        if next==None : self.FILE_NEXT = header["next"]
        else : self.FILE_NEXT = str(next)

        del header
        
        self.spectrum   = os.path.join(self.OUT_DIR,self.FILE_NAME + ".spectrum"    + self.FILE_NEXT)
        self.uvline     = os.path.join(self.OUT_DIR,self.FILE_NAME + ".uvline"      + self.FILE_NEXT)
        self.ifaspec    = os.path.join(self.OUT_DIR,self.FILE_NAME + ".ifaspec"     + self.FILE_NEXT)
        self.hires      = os.path.join(self.OUT_DIR,self.FILE_NAME + ".hires"       + self.FILE_NEXT)
        self.ovi        = os.path.join(self.OUT_DIR,self.FILE_NAME + ".ovi"         + self.FILE_NEXT)

BURST           = MODELDIR(GO_BURST)
CONTINUOUS      = MODELDIR(GO_CONTINUOUS)

LOWERM_01       = MODELDIR(GO_LOWERM,1)
LOWERM_001      = MODELDIR(GO_LOWERM,2)

KROUPA_001      = MODELDIR(GO_LOWERM,2)
CHAB_GAL_001    = MODELDIR(GO_CHAB_GAL)
CHAB_GLOB_001   = MODELDIR(GO_CHAB_GLOB)
KRUP_BIN        = MODELDIR(GO_KROP_BIN)
# -----------------------------------------------


# USER FLAGS : --- Set user level flags here
MODELS_TO_PLOT  = [CONTINUOUS]#,BURST]
LEGEND_LABELS   = ["Continuous","Burst"]

# MODELS_TO_PLOT  = [LOWERM_01,LOWERM_001]
# LEGEND_LABELS   = ["Kroupa 0.1","Kroupa 0.01"]

# MODELS_TO_PLOT  = [LOWERM_001,CHAB_GAL_001,CHAB_GLOB_001,KRUP_BIN]
# LEGEND_LABELS   = ["Kroupa","Chabrier-Gal","Chabrier-Glob","Kroupa-Binary"]

MODEL_COLORS    = ["g","r","b","m"]
AVERAGING_SPAN  = 10
# -----------------------------------------------


# USER FLAGS VALIDATION : --- Validation for inputs
if not type(MODELS_TO_PLOT) is list: MODELS_TO_PLOT = [MODELS_TO_PLOT]
# -----------------------------------------------


# AUTO FLAGS : --- These flags are automatically set
# MODEL_LENGTH = len(MODELS_TO_PLOT)
# -----------------------------------------------


# HANDLES : --- Object Handles
# Figure
fig,ax = plt.subplots()
# Slider
fig.subplots_adjust(top=0.9, bottom=0.25)
ax_time = fig.add_axes([0.15, 0.1, 0.5, 0.02])
time_slider = Slider(ax=ax_time,label="Age",valmin=0,valmax=1,valinit=0,valstep=1,initcolor=None)
time_slider.label.set_size(12)
time_slider.valtext.set_fontsize(12)
# -----------------------------------------------


# GUI STATE FLAGS : --- Event callbacks change these
class PAGE(Enum):
    SPECTRUM    = 1
    UVLINE      = 2
    IFASPEC     = 3
    HIRES       = 4
    OVI         = 5

class SCALE(Enum):
    LINEAR      = 1
    LOGARITHMIC = 2

PAGE_ON_VIEW        = PAGE.UVLINE
XSCALE              = SCALE.LINEAR
YSCALE              = SCALE.LINEAR
TIME_OFFSET_INDEX   = 0
PLOT_CONTINUUM      = False
PLOT_UVFIT          = False

LINES = {
    # Lyman Series
    1216:False,
    1026:False,
    973:False,
    912:False,
    # Balmer Series
    6563:False,
    4861:False,
    4340:False,
    3646:False,
    # Paschen Series
    18750:False,
    12820:False,
    10940:False,
    8204:False,
    # Brackett Limit
    14580:False,
    # Pfund Limit
    22790:False,
    # Humphreys Limit
    32820:False
    }

# -----------------------------------------------



# PAGE VARIABELS : --- Changes only when page changes
class PageVar:
    def __init__(self) -> None:
        self.table              = None

        self.raw_time           = None
        self.raw_wave           = None

        self.raw_log_total      = None
        self.raw_log_stellar    = None
        self.raw_log_nebular    = None
        
        self.raw_log_lum        = None
        self.raw_log_norm       = None
        
        self.unq_time           = None
        self.unq_time_ind       = None
        self.time_in_Myr        = None

    def update_table(self,table):
        self.table=table
        self._extract_columns()

    def _extract_columns(self):
        if PAGE_ON_VIEW == PAGE.SPECTRUM:
            self.raw_time,self.raw_wave,self.raw_log_total,self.raw_log_stellar,self.raw_log_nebular = self.table.T
        else:        
            self.raw_time,self.raw_wave,self.raw_log_lum,self.raw_log_norm = self.table.T

        self.unq_time,self.unq_time_ind = numpy.unique(self.raw_time,return_index=True)
        self.unq_time_ind = numpy.append(self.unq_time_ind,len(self.raw_time))
        self.time_in_Myr = numpy.round(self.unq_time/10**6,2)
        
# data bank
all_view_model_vars = []
for model in MODELS_TO_PLOT:
    all_view_model_vars.append(PageVar())

def UpdateVariablesForPage(page):
    global all_view_model_vars

    model_vars : PageVar    # type hinting
    for i,model_vars in enumerate(all_view_model_vars):
        if   page == PAGE.SPECTRUM:
            model_vars.update_table(numpy.genfromtxt(MODELS_TO_PLOT[i].spectrum,skip_header=6))
        elif page == PAGE.UVLINE:
            model_vars.update_table(numpy.genfromtxt(MODELS_TO_PLOT[i].uvline,skip_header=6))
        elif page == PAGE.IFASPEC:
            model_vars.update_table(numpy.genfromtxt(MODELS_TO_PLOT[i].ifaspec,skip_header=6))
        elif page == PAGE.HIRES:
            model_vars.update_table(numpy.genfromtxt(MODELS_TO_PLOT[i].hires,skip_header=6))
        elif page == PAGE.OVI:
            model_vars.update_table(numpy.genfromtxt(MODELS_TO_PLOT[i].ovi,skip_header=6))

UpdateVariablesForPage(PAGE_ON_VIEW)
# -----------------------------------------------


# PAGE RENDER FUNCTIONS : ---
def PlotAtAge(offset):
    model_vars:PageVar
    for i,model_vars in enumerate(all_view_model_vars):
        row_mask    = numpy.arange(model_vars.unq_time_ind[offset],model_vars.unq_time_ind[offset+1])
        age_wave  = model_vars.raw_wave[row_mask]

        if PAGE_ON_VIEW==PAGE.SPECTRUM:
            age_flux  = model_vars.raw_log_total[row_mask]
        else:
            age_flux = model_vars.raw_log_lum[row_mask]
            # age_flux = (model_vars.raw_log_norm[row_mask])    # <--- For continuum

        c=MODEL_COLORS[i];a=1
        if PLOT_CONTINUUM and PAGE_ON_VIEW==PAGE.UVLINE:
            c='k';a=0.3

        ax.plot(age_wave,age_flux,color=c,alpha=a,lw=1,label= LEGEND_LABELS[i] + " : " + str(model_vars.time_in_Myr[offset])+" Myr")

    if XSCALE==SCALE.LOGARITHMIC: ax.set_xscale('log')
    if YSCALE==SCALE.LOGARITHMIC: ax.set_yscale('log')
    ax.set_xlabel("Wavelength $(\AA)$",fontsize=12)
    ax.set_ylabel("Log Flux $(\\text{ergs s}^{-1} \\text{ }\AA^{-1})$",fontsize=12)
    # ax.set_title("STARBURST99",fontsize=16,pad=30)
    leg=ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.1),ncol = len(MODELS_TO_PLOT),frameon=False,fontsize=12)
    for l in range(len(MODELS_TO_PLOT)):
        leg.legend_handles[l].set_color(MODEL_COLORS[l])
        leg.legend_handles[l].set_alpha(1)
        leg.legend_handles[l].set_linewidth(2)


    for k in LINES.keys():
        if LINES[k]: ax.axvline(k,color='k',ls='--',lw=1)


def PlotUVFit(wave_data,flux_data,line_offset=0):
    # Linear :
    #       f = f0*(lam/lam0)^beta
    # Logarithmic:
    #       log f = beta * log(lam/lam0) + log(f0)
    #       y = beta * log (x/x0) + y0 

    wave_lower = 1350
    wave_upper = 1800
    wave_refer = 1500

    index_refer = numpy.argmin(numpy.abs(wave_data-wave_refer))
    flux_refer = numpy.average(flux_data[index_refer-10:index_refer+10])

    ind_uv_start = numpy.argmin(numpy.abs(wave_data-wave_lower))
    ind_uv_end = numpy.argmin(numpy.abs(wave_data-wave_upper))
    wave_uv = wave_data[ind_uv_start:ind_uv_end]
    flux_uv = flux_data[ind_uv_start:ind_uv_end]

    if True: #Logarithimic
        def fitfun(wave,beta,y0):
            return beta * numpy.log10(wave/wave_refer) + y0 
        pvar,pcov = curve_fit(fitfun,wave_uv,flux_uv,[-2.5,flux_refer])
        
        wave_hr = numpy.linspace(wave_lower,wave_upper,1000)
        fitted_flux_hr = fitfun(wave_hr,pvar[0],pvar[1])
        ax.plot(wave_hr,fitted_flux_hr,'-k',lw=1)

        beta_uv= pvar[0]
        f_uv = fitted_flux_hr[numpy.argmin(numpy.abs(wave_hr-wave_refer))]

    if False: #Linear
        def fitfun(wave,beta,f0):
            return f0*numpy.power(wave/wave_refer,beta)
        pvar,pcov = curve_fit(fitfun,wave_uv,10**flux_uv,[-2.5,10**flux_refer])
            
        wave_hr = numpy.linspace(wave_lower,wave_upper,1000)
        fitted_flux_hr = fitfun(wave_hr,pvar[0],pvar[1])
        ax.plot(wave_hr,numpy.log10(fitted_flux_hr),'-b',lw=2)

        beta_uv= pvar[0]
        f_uv = fitted_flux_hr[numpy.argmin(numpy.abs(wave_hr-wave_refer))]
        f_uv = numpy.log10(f_uv)
    

    if True:
        ax.annotate("$\\beta_{\\text{UV}}$="+str(numpy.round(beta_uv,2)),
                        xy=(1,1),xytext=(+10,-10 - line_offset * 20),xycoords="axes fraction",textcoords="offset pixels",fontsize=12,
                        ha="left",va="top",color=MODEL_COLORS[line_offset])
        
        # plt.annotate("$\\tau$="+str(time_in_Myr[i])+" Myr",
        #         xy=(1,1),xytext=(-10,-45),xycoords="axes fraction",textcoords="offset pixels",fontsize=12,
        #         ha="right",va="top")



def PlotContinuumAndUVFit():
    if (not PLOT_CONTINUUM) and (not PLOT_UVFIT) : return

    for lo,line in enumerate(ax.lines):
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        cxdata=[]
        cydata=[]

        span= AVERAGING_SPAN
        for i in range(span,len(xdata)-span):
            if xdata[i]<1250 or xdata[i]>1900 : continue
            if True:
                if (xdata[i]>1520 and xdata[i]<1570) :continue

            chunk=ydata[i-span:i+span+1]
            chunk_avg=numpy.average(chunk)
            rel_offset = chunk-chunk_avg

            sumy = numpy.sum(chunk*numpy.exp(-rel_offset**2/0.01))
            sumy/= numpy.sum(numpy.exp(-rel_offset**2/0.01))

            # sumy = numpy.sum(chunk*numpy.exp(rel_offset/0.01))
            # sumy/= numpy.sum(numpy.exp(rel_offset/0.01))

            cydata.append(sumy)
            cxdata.append(xdata[i])
        
        cxdata = numpy.array(cxdata)
        cydata = numpy.array(cydata)

        if PLOT_CONTINUUM:ax.plot(cxdata,cydata,'-',color=MODEL_COLORS[lo])
        if PLOT_UVFIT : PlotUVFit(cxdata,cydata,lo)

        
    


# -----------------------------------------------


# VIEW MANAGEMENT : ---
def UpdateView(page):
    global PAGE_ON_VIEW
    if not PAGE_ON_VIEW == page : 
        PAGE_ON_VIEW = page
        UpdateVariablesForPage(PAGE_ON_VIEW)
    
    ax.clear()
    PlotAtAge(TIME_OFFSET_INDEX)

    time_slider.valmax = min([len(model_vars.unq_time)-1 for model_vars in all_view_model_vars])
    time_slider.ax.set_xlim(time_slider.valmin,time_slider.valmax)

    if PAGE_ON_VIEW==PAGE.UVLINE:PlotContinuumAndUVFit()


    canvas.draw()
# -----------------------------------------------


# GUI EVENT CALLBACKS : --- 
def OnChange_Slider(val): 
    global TIME_OFFSET_INDEX
    TIME_OFFSET_INDEX = val
    UpdateView(PAGE_ON_VIEW)
    time_slider.valtext.set_text(f"{val}")

def OnClick_Xscale():
    global XSCALE
    if XSCALE == SCALE.LINEAR : XSCALE = SCALE.LOGARITHMIC
    elif XSCALE == SCALE.LOGARITHMIC : XSCALE = SCALE.LINEAR
    UpdateView(PAGE_ON_VIEW)

def OnClick_Yscale():
    global YSCALE
    if YSCALE == SCALE.LINEAR : YSCALE = SCALE.LOGARITHMIC
    elif YSCALE == SCALE.LOGARITHMIC : YSCALE = SCALE.LINEAR
    UpdateView(PAGE_ON_VIEW)

def OnClick_Line(line):
    global LINES
    if not line in LINES.keys() : return
    LINES[line]=not LINES[line]
    UpdateView(PAGE_ON_VIEW)

def OnClick_LineClearAll():
    return
    global LINES
    for key in LINES.keys():LINES[key]=False
    UpdateView(PAGE_ON_VIEW)
    # also change gui tickbox state
    # need to change dict to bool-var

def OnClick_Continuum():
    global PLOT_CONTINUUM
    PLOT_CONTINUUM = not PLOT_CONTINUUM
    UpdateView(PAGE_ON_VIEW)

def OnClick_UVFit():
    global PLOT_UVFIT
    PLOT_UVFIT = not PLOT_UVFIT
    UpdateView(PAGE_ON_VIEW)

# Subscribe to events
time_slider.on_changed(OnChange_Slider)
# -----------------------------------------------




# TKINTER GUI : ---
# --- Window
root = tk.Tk()
root.title("Starburst99 Spectrum Viewer")
root.geometry("800x600")
def quit_me():
    root.destroy()
    root.quit()
root.protocol("WM_DELETE_WINDOW", quit_me)


# --- Embed in Matplotlib
canvas = FigureCanvasTkAgg(fig, master = root)   
canvas.draw() 
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root) 
toolbar.update() 
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1) 

# Initial Page
UpdateView(PAGE_ON_VIEW)



# --- Menubar
menubar                 = tk.Menu(root)
# Form menu-items
mi_file                 = tk.Menu(menubar,tearoff=0)

mi_lines                = tk.Menu(menubar,tearoff=0)
if True:
    mi_line_H           = tk.Menu(mi_lines,tearoff=0)
    if True:
        mi_lyman        = tk.Menu(mi_line_H,tearoff=0)
        mi_balmer       = tk.Menu(mi_line_H,tearoff=0)
        mi_paschen      = tk.Menu(mi_line_H,tearoff=0)
        mi_brackett     = tk.Menu(mi_line_H,tearoff=0)
        mi_pfund        = tk.Menu(mi_line_H,tearoff=0)
        mi_humphreys    = tk.Menu(mi_line_H,tearoff=0)
    mi_line_He          = tk.Menu(mi_lines,tearoff=0)
mi_utils                = tk.Menu(menubar,tearoff=0)

# Add cascades
menubar.add_cascade(label ='File', menu = mi_file) 
menubar.add_cascade(label ='Lines', menu = mi_lines) 
menubar.add_cascade(label ='Utility', menu = mi_utils)
# ---
mi_lines.add_cascade(label ='Hydrogen', menu = mi_line_H)
mi_lines.add_cascade(label ='Helium', menu = mi_line_He)
mi_lines.add_separator()
mi_lines.add_command(label="Clear All",command=OnClick_LineClearAll)
# ---
mi_line_H.add_cascade(label="Lyman",menu=mi_lyman)
mi_line_H.add_cascade(label="Balmer",menu=mi_balmer)
mi_line_H.add_cascade(label="Paschen",menu=mi_paschen)
mi_line_H.add_cascade(label="Brackett",menu=mi_brackett)
mi_line_H.add_cascade(label="Pfund",menu=mi_pfund)
mi_line_H.add_cascade(label="Humphreys",menu=mi_humphreys)
# ---
menubar.add_checkbutton(label="Log X",command=OnClick_Xscale)
menubar.add_checkbutton(label="Log Y",command=OnClick_Yscale)

# Add Commands
mi_file.add_radiobutton(label ='spectrum', command = lambda:UpdateView(PAGE.SPECTRUM)) 
mi_file.add_radiobutton(label ='uvline', command = lambda:UpdateView(PAGE.UVLINE))
mi_file.add_radiobutton(label ='ifaspec', command = lambda:UpdateView(PAGE.IFASPEC))
mi_file.add_radiobutton(label ='hires', command = lambda:UpdateView(PAGE.HIRES))
mi_file.add_radiobutton(label ='ovi', command = lambda:UpdateView(PAGE.OVI))
#---
mi_utils.add_checkbutton(label="Continuum",command=OnClick_Continuum)
mi_utils.add_checkbutton(label="UV Fit",command=OnClick_UVFit)
#--- Lines
mi_lyman.add_checkbutton(label="Alpha (1216A)",command=lambda:OnClick_Line(1216))
mi_lyman.add_checkbutton(label="Beta (1026A)",command=lambda:OnClick_Line(1026))
mi_lyman.add_checkbutton(label="Gamma (973A)",command=lambda:OnClick_Line(973))
mi_lyman.add_separator()
mi_lyman.add_checkbutton(label="Limit (912A)",command=lambda:OnClick_Line(912))
# ---
mi_balmer.add_checkbutton(label="Alpha (6563A)",command=lambda:OnClick_Line(6563))
mi_balmer.add_checkbutton(label="Beta (4861A)",command=lambda:OnClick_Line(4861))
mi_balmer.add_checkbutton(label="Gamma (4340A)",command=lambda:OnClick_Line(4340))
mi_balmer.add_separator()
mi_balmer.add_checkbutton(label="Limit (3646A)",command=lambda:OnClick_Line(3646))
# ---
mi_paschen.add_checkbutton(label="Alpha (18750A)",command=lambda:OnClick_Line(18750))
mi_paschen.add_checkbutton(label="Beta (12820A)",command=lambda:OnClick_Line(12820))
mi_paschen.add_checkbutton(label="Gamma (10940A)",command=lambda:OnClick_Line(10940))
mi_paschen.add_separator()
mi_paschen.add_checkbutton(label="Limit (8204A)",command=lambda:OnClick_Line(8204))
# ---
mi_brackett.add_checkbutton(label="Limit (14580A)",command=lambda:OnClick_Line(14580))
mi_pfund.add_checkbutton(label="Limit (22790A)",command=lambda:OnClick_Line(22790))
mi_humphreys.add_checkbutton(label="Limit (32820A)",command=lambda:OnClick_Line(32820))


# ---
root.config(menu=menubar)


# Run window mainloop
tk.mainloop()