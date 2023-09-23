import numpy as np
from matplotlib.colors import is_color_like

#Box
# ax            : handle of plot
# x,y,z         : position of points 
# L             : size of box
# s             : size of points

def PlotBox(ax,L,x,y,z,s,color='k',fids=None,fcolor='r'):
    # Validation
    if L==0:raise Exception("ERROR : Box Size=0.")

    try: # accepts [1] not 1. dirty fix 
        for si in s:
            if si==0: raise Exception("ERROR : Size zero point detected.")
    except:
        pass
    

    clr=np.array([color for i in range(0,len(x))],dtype=object)

    # Validate Fids Array
    

    # Validate Color

    def ValidateFidColorArray():
        # for each list in fids one correponding valid color in fcolors
        # so fids must be at max 2d array
        # fcolors must be at max 1d array

        fgid_1d=np.array([],dtype=int)
        fcid_1d=np.array([],dtype=object)       # change to rgb tuple append

        if fids==None:return

        if not type(fids) in [int,list,np.ndarray]:
            raise Exception("ERROR : fids must be of type between int,list or numpy array")
        
        if type(fids)==int:
            if not is_color_like(fcolor):
                raise Exception("ERROR : fcolor must be a valid color.")
            else:
                fgid_1d=np.append(fgid_1d,fids)
                fcid_1d=np.append(fcid_1d,fcolor)   # change to rgb tuple append
            return
        
        if type(fids) in [list,np.ndarray]:
            # print(len(fids),len(fcolor))
            if not len(fids)==len(fcolor): raise Exception("ERROR : Length of fids and fcolors must be same")
            for c in fcolor:
                if not is_color_like(c): raise Exception("ERROR : Elements of fcolors must be a valid color")

            for i in range(len(fids)):
                lv1_elm=fids[i] 
                if not type(lv1_elm) in [int,list,np.ndarray]:
                    raise Exception("ERROR : Level 1 Elements of fids must be int,list or numpy array")
                
                if type(lv1_elm)==int:
                        fgid_1d=np.append(fgid_1d,lv1_elm)
                        fcid_1d=np.append(fcid_1d,fcolor[i])# change to rgb tuple append
                        continue

                if type(lv1_elm) in [list,np.ndarray]:
                    for lv2_elm in lv1_elm:
                        if not type(lv2_elm)==int:
                            raise Exception("ERROR : Level 2 Elements of fids must be int")
                    
                carray=[fcolor[i] for e in lv1_elm]
                fgid_1d=np.append(fgid_1d,np.array(lv1_elm))
                fcid_1d=np.append(fcid_1d,np.array(carray)) # change to rgb tuple append

        return [fgid_1d,fcid_1d]
                

    try:
        if not fids==None: # Issue when no halo in the begginning
            fgid,fcid=ValidateFidColorArray()
            clr[fgid]=fcid    
            # for i in range(len(fgid)):
            #     clr[fgid[i]]=fcid[i] 
        #------------------------------------------------------------
        ax.scatter(x,y,z,s=s,color=clr,ec='none')
        #------------------------------------------------------------
    except:
        print("passed")
        pass
    # Limit Range
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)
    ax.set_zlim(0,L)
    #Hide axis ticks
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    # Hide BG Grid
    ax.grid(False)
    # BG plane transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # Draw Sim Cube
    alp=1
    ax_cx=np.array([0,1,1,0,0,0,0,1,1,0,0])*L
    ax_cy=np.array([0,0,1,1,0,0,0,0,1,1,0])*L
    ax_cz=np.array([0,0,0,0,0,1,1,1,1,1,1])*L
    ax.plot(ax_cx,ax_cy,ax_cz,'k-',alpha=alp,lw=1)
    ax.plot([L,L],[0,0],[0,L],'k-',alpha=alp,lw=1)
    ax.plot([L,L],[L,L],[0,L],'k-',alpha=alp,lw=1)
    ax.plot([0,0],[L,L],[0,L],'k-',alpha=alp,lw=1)
    # plt.tight_layout()
    #Rotate view(elev,azim)
    ax.view_init(20,40)
    ax.axis("equal")