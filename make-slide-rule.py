import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        r"""
        # Rotary slide rule

        ## [Usage video](https://www.youtube.com/watch?v=85sJeg3v7Jg), [Github](https://github.com/gcr/balatro-slide-rule)

        - Rotary logarithmic scale with three octaves for multiplying numbers between 001 and 999. 
          - I really like the 3-octave design because you can think in terms of "ones," "thousands," or "millions" depending on situation
          - Calculation wraps around, eliminating "off-scale" calculation problems of linear slide rules
        - This notebook saves inner.pdf and outer.pdf
        - Open in Affinity Designer, expand strokes, make sure there's no self-intersecting geometry, and export to SVG
        - Open the resulting files in Fusion 360. Use the center "X" to align.
        """
    )
    return


@app.cell
def __(annotate, mo, np, out, plt, prep_ax, start):
    # Polar coordinates: (theta, r)
    ax = prep_ax([start])


    # X in center, useful for aligning inner and outer in Fusion 360
    ax.plot([0,np.pi], [10,10])
    ax.plot([np.pi*0.5,np.pi*1.5], [10,10])

    # Plot has three octaves
    scales = [1, 10, 100]

    # Where to place notches? (theta)
    longnotches =    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    shortnotches =   [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
    shorternotches = [x+a for a in [1,2,3,4] for x in [.1, .2, .3, .4, .6, .7, .8, .9]]

    # Line lengths (r)
    llength = 5 if out.value else -5
    longline =       [start, start+llength]
    shortline =      [start+llength*0.5, start+llength]
    shorterline =    [start+llength*0.5, start+llength*0.4]

    # Text
    fontsize = 10
    prefix="" # change to "x " to add multiplier in front of all digits
    xytext=(0.01, start+llength*3.5)

    path="scale-out.pdf" if out.value else "scale-in.pdf"

    annotate(ax, scales, longnotches,
            line=longline,
            textformat=prefix+"%s", lw=1.7, xytext=xytext, size=fontsize)
    annotate(ax, scales, shortnotches,
             line=shortline)
    annotate(ax, scales, shorternotches,
             line=shorterline)
    annotate(ax, 1,        [1.5, 2.5], textformat=prefix+"%.1f", xytext=xytext, size=fontsize)
    annotate(ax, [10,100], [1.5, 2.5], textformat=prefix+"%d", xytext=xytext, size=fontsize)
    plt.savefig(path)
    mo.vstack([mo.md("# Slide rule preview"), out, ax])
    return (
        ax,
        fontsize,
        llength,
        longline,
        longnotches,
        path,
        prefix,
        scales,
        shorterline,
        shorternotches,
        shortline,
        shortnotches,
        xytext,
    )


@app.cell
def __(np, plt):
    start = 95
    def prep_ax(ring_heights=[95]):
        """Start making a new plot, in polar coordinates"""
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
        ax.grid(False)
        ax.set_frame_on(False)
        ax.axes.get_yaxis().set_visible(False)

        angles = np.linspace(0.0, 2.0*np.pi, 100)
        # plot a single ring
        if ring_heights is not None:
            ax.plot( angles, 100*ring_heights, color='black', lw=0.2 )
        # all ticks are made manually via plt.annotate()
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
    #                    font=Path("/Users/kimmy/Downloads/
    #                              "m6x11plus.ttf"),
                        size=size,
                    )
    return annotate, prep_ax, start


@app.cell
def __():
    import marimo as mo
    from matplotlib import pyplot as plt
    import numpy as np
    from pathlib import Path

    # adapted from https://stackoverflow.com/questions/69080109/matplotlib-making-polar-plot-with-logarithmic-angular-axis
    return Path, mo, np, plt


@app.cell
def __(mo):
    # UI switches
    out = mo.ui.switch(True, label="Text is outside ring")
    return (out,)


if __name__ == "__main__":
    app.run()
