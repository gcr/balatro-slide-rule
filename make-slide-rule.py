import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def __(Path, np, plt):
    def prep_ax(plot_heights=[95]):
        ax = plt.subplot(111, polar=True)

        # Make the labels go clockwise
        ax.set_theta_direction(-1)
        # Place 0 at the top
        ax.set_theta_offset(np.pi/2.0)       

        # Polar plots don't have tick marks, 
        # cannot draw outside the max radius set by ylim
        # Remove the frame, and y-axis,
        # * draw our own axis circle
        # * draw our own tick marks (below)
        ax.set_ylim(0,130)
        #ax.grid(False)
        ax.set_frame_on(False)
        ax.axes.get_yaxis().set_visible(False)

        angles = np.linspace(0.0, 2.0*np.pi, 100)
        ax.plot( angles, 100*plot_heights, color='black', lw=0.2 )
        ax.set(xticks=[], yticks=[])
        return ax

    def annotate(ax, start_bases,
                 ranges,
                 line=None,
                 textformat=None,
                 xytext=(0.01, 120),
                 size=12,
                 lw=1.0, c='#000', scale=3):
        if not isinstance(start_bases, list):
            start_bases = [start_bases]
        for start in start_bases:
            label = [r*start for r in ranges]
            thetas=2.0*np.pi*np.log10(label)/scale
            if line is not None:
                ax.plot([thetas,thetas], line,lw=lw,c=c)
            if textformat is not None:
                for t,l in zip(thetas, label):
                    l = textformat%l
                    ax.annotate(l,
                        (t+xytext[0],xytext[1]),
                        rotation=-t*180/np.pi + 90,
                        ha='center',
                        va='center',
                        font=Path("/Users/kimmy/Downloads/"
                                  "m6x11plus.ttf"),
                        size=size,
                    )
    return annotate, prep_ax


@app.cell
def __(mo):
    out = mo.ui.switch(False, label="Out facing")
    out
    return (out,)


@app.cell
def __(out):
    start = 95
    prefix=""
    llength = 5 if out.value else -5
    path="scale-out.pdf" if out.value else "scale-in.pdf"
    return llength, path, prefix, start


@app.cell
def __(annotate, llength, np, path, plt, prefix, prep_ax, start):
    scales = [1, 10, 100]
    ax = prep_ax([start])
    ax.plot([0,np.pi], [10,10])
    ax.plot([np.pi*0.5,np.pi*1.5], [10,10])
    longnotches =    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    longline =       [start, start+llength]
    shortline =      [start+llength*0.5, start+llength]
    shortnotches =   [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
    shorternotches = [x+a for a in [1,2,3,4] for x in [.1, .2, .3, .4, .6, .7, .8, .9]]
    shorterline =    [start+llength*0.5, start+llength*0.4]
    xytext=(0.01, start+llength*2.5)
    size=10
    annotate(ax, scales, longnotches,
            line=longline,
            textformat=prefix+"%s", lw=1.7, xytext=xytext, size=size)
    annotate(ax, scales, shortnotches,
             line=shortline)
    annotate(ax, scales, shorternotches,
             line=shorterline)
    annotate(ax, 1,        [1.5, 2.5], textformat=prefix+"%.1f", xytext=xytext, size=size)
    annotate(ax, [10,100], [1.5, 2.5], textformat=prefix+"%d", xytext=xytext, size=size)
    plt.savefig(path)
    ax
    return (
        ax,
        longline,
        longnotches,
        scales,
        shorterline,
        shorternotches,
        shortline,
        shortnotches,
        size,
        xytext,
    )


@app.cell
def __():
    import marimo as mo
    from matplotlib import pyplot as plt
    import numpy as np
    from pathlib import Path

    # from https://stackoverflow.com/questions/69080109/matplotlib-making-polar-plot-with-logarithmic-angular-axis
    return Path, mo, np, plt


if __name__ == "__main__":
    app.run()
