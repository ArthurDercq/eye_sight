from __future__ import annotations

import math

import matplotlib.pyplot as plt
import seaborn as sns
from eye_sight.strava.store_data import *
from eye_sight.strava.clean_data import *
from eye_sight.strava.fetch_strava import *


def plot_elevations(df, output_file="../plots/elevations.png"):
    # Create a new figure
    plt.figure()

    # Compute activity start times (for facet ordering)
    start_times = (
        df.groupby("name").agg({"moving_time": "min"}).reset_index().sort_values("moving_time")
    )
    ncol = math.ceil(math.sqrt(len(start_times)))

    # Create facets
    p = sns.FacetGrid(
        data=df,
        col="name",
        col_wrap=ncol,
        col_order=start_times["name"],
        sharex=False,
        sharey=True,
    )

    # Add activities
    p = p.map(plt.plot, "dist", "ele", color="black", linewidth=4)

    # Update plot aesthetics
    p.set(xlabel=None)
    p.set(ylabel=None)
    p.set(xticks=[])
    p.set(yticks=[])
    p.set(xticklabels=[])
    p.set(yticklabels=[])
    p.set_titles(col_template="", row_template="")
    sns.despine(left=True, bottom=True)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
    plt.savefig(output_file)


def filtrer_trail_runs(df):
    # Colonnes à garder
    colonnes = ["name", "moving_time", "distance", "total_elevation_gain", "sport_type"]

    # Filtrer les colonnes si elles existent dans le DataFrame
    df = df[[col for col in colonnes if col in df.columns]]

    # Garder uniquement les lignes où sport_type est "TrailRun"
    df_filtré = df[df["sport_type"] == "TrailRun"]

    # Supprimer la colonne "sport_type" si tu ne veux plus l’avoir ensuite
    df_filtré = df_filtré.drop(columns="sport_type")

    return df_filtré

if __name__ == '__main__':

    activities = fetch_strava_data()

    activities_clean = clean_data(activities)

    df_to_plot_elev = filtrer_trail_runs(activities_clean)

    plot_elevations(df_to_plot_elev)






### Le tracé n’est pas bon car total_elevation_gain est un nombre unique par activité → pas de courbe.

### Il faut un DataFrame avec plusieurs points par activité (dist, ele) pour tracer un vrai profil d’altitude.
