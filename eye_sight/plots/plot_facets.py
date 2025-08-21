from __future__ import annotations
import matplotlib.pyplot as plt
import seaborn as sns
import json
import polyline



def plot_mini_map(df, output_file="plot.png"):

    # Ton string JSON
    json_str = """{"id": "a15533644587", "summary_polyline": "qgotHkgn[[HKZEBMCMKY[k@cAa@k@U@aCl@}@^gDx@a@Ni@Lw@VeA`@uBj@a@Pi@LCALe@Jq@Lk@n@qB`ByDzBsFxAmCzAcCVy@FUDm@?o@FoCH_BJcAEEIB[Xc@j@g@t@c@Z[\\\\YXkBlCe@^]JIQFi@QQ]@MBg@oAa@k@c@HYCEBKIYCOBCFDNIvADj@DPCVi@r@OXUPS\\\\Ub@URCHQTSNW?UEg@]ACH_@TQVKBGPBPARORSB]@CN?TWP]H_@N}ABk@?aAHeADI@OIk@?KMWOQQi@Eq@GWBQ]y@YmAGe@o@}DMq@Og@U}AYgAxA{AlAaC\\\\]X]pAw@~@{@f@UFKh@QxBoAr@QbA@h@Gr@At@MXGPKl@@d@Dx@MXK`AG^I`@@~@W\\\\E`@@h@?\\\\BXJABKN_@PQ`@@x@Lv@JpAQlASp@@RL`@NNJT`Az@NbAH`AGZINo@h@MjACb@Ux@e@|@[x@CZBPAh@Lf@v@pANNV^Tb@Ab@CLDN@Z_@f@}@RWZQj@NtEC|@I`@Y^Ol@Fd@DLbAbBz@hAf@Rf@Dr@AN\\\\@LWl@q@p@MFgAVc@Re@Lu@XYRk@d@kAj@oEzAoA\\\\|B{@PINQf@QlA]`@EDNN\\\\bAbBLHHANGFI", "resource_state": 2}"""

    # Charger le JSON
    data = json.loads(json_str)
    polyline_str = data["summary_polyline"]

    # Décoder la polyline
    coords = polyline.decode(polyline_str)  # renvoie une liste de tuples (lat, lon)

    # Séparer latitude et longitude
    lats, lons = zip(*coords)

    # Tracer la trace
    plt.figure(figsize=(8, 8))
    plt.plot(lons, lats, color="blue", linewidth=2)
    plt.scatter(lons[0], lats[0], color="green", s=50, label="Départ")  # point départ
    plt.scatter(lons[-1], lats[-1], color="red", s=50, label="Arrivée")  # point arrivée
    plt.title("Trace de l'activité")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.axis("equal")  # pour garder les proportions réelles
    plt.legend()
    plt.show()
