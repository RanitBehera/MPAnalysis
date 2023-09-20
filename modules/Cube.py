import numpy as np

#Box
# ax            : handle of plot
# x,y,z         : position of points 
# L             : size of box
# s             : size of points
# f             : loc of size to focus, takes value from 0-1, mapped to min(size)-max(size)
# df            : span of size to focus
def PlotBox(ax,L,x,y,z,s,f=0.5,df=0,color='k',fcolor='r',ftype='focus'):
    # Validation
    if L==0:raise Exception("ERROR : Box Size=0.")
    for si in s:
        if si==0: raise Exception("ERROR : Size zero point detected.")
    if f<0:f=0
    if f>1:f=1

    # Points to focus maspping
    # if df>0:
    #     s_max=max(s)
    #     s_min=min(s)
    #     s_span=s_max-s_min
    #     s_loc=s_min   + ( f        *s_span)
    #     s_loc_l=s_min + ((f - df/2)*s_span)
    #     s_loc_u=s_min + ((f + df/2)*s_span)
    #     # Color assignment
    #     clr=['' for i in range(0,len(x))]
    #     for i in range(0,len(x)):
    #         if ((s[i]>s_loc_l) and (s[i]<s_loc_u)):
    #             clr[i]=fcolor
    #         else:
    #             clr[i]=color
    # else: clr=color

    clr=[color for i in range(0,len(x))]
    try:
        clr[0]=fcolor
    except:
        pass


    #------------------------------------------------------------
    ax.scatter(x,y,z,s=s,color=clr,ec='none')
    #------------------------------------------------------------
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