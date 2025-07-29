from __future__ import annotations

import calmap
import matplotlib.pyplot as plt
import pandas as pd

ACTIVITY_FORMAT = "%b %d, %Y, %H:%M:%S %p"


def plot_calendar(
    df,
    year_min=None,
    year_max=None,
    max_dist=None,
    fig_height=15,
    fig_width=9,
    output_file="calendar.png",
):
    # Create a new figure
    plt.figure()

    # Process data
    df["start_date"] = pd.to_datetime(
        df["start_date"], format=ACTIVITY_FORMAT
    )
    df["date"] = df["start_date"].dt.date
    df = df.groupby(["date"])["distance"].sum()
    df.index = pd.to_datetime(df.index)
    df.clip(0, max_dist, inplace=True)

    if year_min:
        df = df[df.index.year >= year_min]

    if year_max:
        df = df[df.index.year <= year_max]

    # Create heatmap
    fig, ax = calmap.calendarplot(data=df)

    # Save plot
    fig.set_figheight(fig_height)
    fig.set_figwidth(fig_width)
    fig.savefig(output_file, dpi=600)
