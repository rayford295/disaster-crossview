"""
Generate an interactive Folium map of labeled street view locations,
color-coded by damage class.

Usage:
    python scripts/visualization/map_damage_points.py --root .
    python scripts/visualization/map_damage_points.py --root . --out my_map.html

Opens outputs/damage_map.html in a browser (or pass --out to override).
"""

import argparse
import webbrowser
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from pathlib import Path

CLASS_COLORS = {
    "No_Damage":     "#2ecc71",
    "Affected_1-9_": "#f39c12",
    "Destroyed_50_": "#e74c3c",
}
CLASS_LABELS = {
    "No_Damage":     "No Damage",
    "Affected_1-9_": "Affected (1–9%)",
    "Destroyed_50_": "Destroyed (≥50%)",
}


def make_circle_marker(row) -> folium.CircleMarker:
    color = CLASS_COLORS.get(row["damage_class"], "#999")
    popup_html = (
        f"<b>{CLASS_LABELS.get(row['damage_class'], row['damage_class'])}</b><br>"
        f"OID: {row['object_id']}<br>"
        f"Lat: {row['latitude']:.6f}<br>"
        f"Lon: {row['longitude']:.6f}<br>"
        f"<small>{row['filename']}</small>"
    )
    return folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=CLASS_LABELS.get(row["damage_class"], row["damage_class"]),
    )


def add_legend(m: folium.Map):
    legend_html = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
                background: white; padding: 12px 16px; border-radius: 8px;
                border: 1px solid #ccc; font-family: Arial; font-size: 13px;">
      <b>Damage Class</b><br>
      <span style="color:#2ecc71;">&#9679;</span> No Damage (n={nd})<br>
      <span style="color:#f39c12;">&#9679;</span> Affected 1–9% (n={af})<br>
      <span style="color:#e74c3c;">&#9679;</span> Destroyed ≥50% (n={de})
    </div>
    """
    return legend_html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default=None)
    parser.add_argument("--cluster", action="store_true", help="Use marker clustering")
    args = parser.parse_args()

    root = Path(args.root)
    metadata_path = root / "data" / "eaton_fire_metadata.csv"
    if not metadata_path.exists():
        raise FileNotFoundError(
            f"{metadata_path} not found. Run scripts/data_prep/parse_metadata.py first."
        )

    df = pd.read_csv(metadata_path)
    center_lat = df["latitude"].mean()
    center_lon = df["longitude"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles="CartoDB positron",
    )

    if args.cluster:
        marker_group = MarkerCluster().add_to(m)
    else:
        marker_group = m

    for _, row in df.iterrows():
        make_circle_marker(row).add_to(marker_group)

    counts = df["damage_class"].value_counts()
    legend = add_legend(m).format(
        nd=counts.get("No_Damage", 0),
        af=counts.get("Affected_1-9_", 0),
        de=counts.get("Destroyed_50_", 0),
    )
    m.get_root().html.add_child(folium.Element(legend))

    out_path = args.out or str(root / "outputs" / "damage_map.html")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    m.save(out_path)
    print(f"Map saved → {out_path}")
    webbrowser.open(f"file://{Path(out_path).resolve()}")


if __name__ == "__main__":
    main()
