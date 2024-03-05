import numpy,os
import matplotlib.pyplot as plt


SAVED_PATH = "/mnt/home/student/cranit/Work/RSGBank/TBSFR_Bank"

# PLOT
fig,ax=plt.subplots(1,1)
lines=[]
for offset in range(100):
    lbage,sfr = numpy.loadtxt(os.path.join(SAVED_PATH,"off_"+str(offset)+".txt")).T
    lbage /= 1e6
    hnd=ax.plot(lbage,sfr,'k.-',alpha=0.1,ms=1)
    lines.append(hnd[0])

# --- BEAUTIFY
# plt.xscale('log')
plt.yscale('log')
plt.xlabel("Age (Myr)")
plt.ylabel("SFR ($M_\odot yr^{-1}$)")

# Focus One
from matplotlib.widgets import Slider
axfreq = fig.add_axes([0.25, 0.9, 0.65, 0.03])
line_selector = Slider(ax=axfreq,label='Halo Offset',valmin=-1,valmax=99,valinit=-1,valstep=1)
def update(val):
    for i in range(100):
        reset_line = lines[i]
        reset_line.set_color('k')
        reset_line.set_alpha(0.1)
    selected_line_index = int(line_selector.val)
    if selected_line_index==-1:return
    selected_line = lines[selected_line_index]
    selected_line.set_color('r')
    selected_line.set_alpha(0.5)
    fig.canvas.draw_idle()
line_selector.on_changed(update)

# ---

# --- SAVE
plt.show()
# plt.savefig(SAVE_PATH,dpi=200)