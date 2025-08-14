import matplotlib.pyplot as plt
import pandas as pd



def _prepare_weekly_data(df, value_col, weeks, sport_types=None):
    """
    Prépare les données agrégées par semaine.

    :param df: DataFrame contenant au minimum 'start_date', 'sport_type', 'distance', 'moving_time', 'total_elevation_gain'
    :param value_col: colonne à agréger ('duration_h', 'distance_km')
    :param weeks: nombre de semaines à afficher
    :param sport_types: liste des sports à filtrer ou None pour tous
    """
    df = df.copy()
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["week"] = df["start_date"].dt.to_period("W").apply(lambda r: r.start_time)

    if sport_types:
        df = df[df["sport_type"].isin(sport_types)]

    weekly = (
        df.groupby("week")
        .agg({
            value_col: "sum",
            "total_elevation_gain": "sum"
        })
        .reset_index()
        .sort_values("week", ascending=False)
        .head(weeks)
        .sort_values("week")  # on remet en ordre chronologique
    )
    return weekly


def _plot_bar_with_dplus(weekly_df, value_label, color="skyblue"):
    """
    Trace un graphique barres + courbe D+.
    """
    fig, ax1 = plt.subplots(figsize=(8, 4))

    # Barres
    ax1.bar(weekly_df["week"], weekly_df.iloc[:, 1], color=color, label=value_label)
    ax1.set_ylabel(value_label, color=color)
    ax1.tick_params(axis="y", labelcolor=color)

    # Courbe D+ sur axe secondaire
    ax2 = ax1.twinx()
    ax2.plot(weekly_df["week"], weekly_df["total_elevation_gain"], color="darkred", marker="o", label="D+ (m)")
    ax2.set_ylabel("D+ (m)", color="darkred")
    ax2.tick_params(axis="y", labelcolor="darkred")

    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def plot_hours_per_week(df, weeks=10):
    weekly_df = _prepare_weekly_data(df, "moving_time", weeks)
    return _plot_bar_with_dplus(weekly_df, "Heures de sport", color="cornflowerblue")


def plot_run_trail_km_per_week(df, weeks=10):
    weekly_df = _prepare_weekly_data(df, "distance", weeks, sport_types=["Run", "TrailRun"])
    return _plot_bar_with_dplus(weekly_df, "Km Run & TrailRun", color="seagreen")


def plot_bike_km_per_week(df, weeks=10):
    weekly_df = _prepare_weekly_data(df, "distance", weeks, sport_types=["Ride"])
    return _plot_bar_with_dplus(weekly_df, "Km Vélo", color="orange")
