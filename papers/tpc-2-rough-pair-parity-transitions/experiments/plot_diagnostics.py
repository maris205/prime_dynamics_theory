#!/usr/bin/env python3
"""Render dependency-free SVG diagnostics from rough_pair_diagnostics CSV files."""

import argparse
import csv
import html
import math
from pathlib import Path


SECTOR_COLORS = {
    "PP": "#1677b8",
    "PS": "#f29e2e",
    "SP": "#59a14f",
    "SS": "#d45087",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot four-sector shares and least-prime-factor heatmaps as SVG."
    )
    parser.add_argument("--summary", required=True, help="*_summary.csv file")
    parser.add_argument("--bins", required=True, help="*_factor_bins.csv file")
    parser.add_argument(
        "--theta",
        help="optional comma-separated theta values to retain in the figure",
    )
    parser.add_argument(
        "--output", default="rough_pair_diagnostics.svg", help="output SVG path"
    )
    return parser.parse_args()


def read_csv(path):
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def svg_text(x, y, text, size=13, anchor="start", weight="normal", fill="#222"):
    safe = html.escape(str(text))
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Arial, sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
        f'fill="{fill}">{safe}</text>'
    )


def heat_color(value):
    value = max(0.0, min(1.0, value))
    value = math.sqrt(value)
    start = (242, 247, 252)
    end = (8, 81, 156)
    rgb = tuple(round(a + value * (b - a)) for a, b in zip(start, end))
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def main():
    args = parse_args()
    summary = read_csv(args.summary)
    bins = read_csv(args.bins)
    if not summary:
        raise SystemExit("summary CSV has no data rows")
    if not bins:
        raise SystemExit("factor-bin CSV has no data rows")

    summary.sort(key=lambda row: float(row["theta"]))
    if args.theta:
        selected = [float(token) for token in args.theta.split(",")]
        summary = [
            row for row in summary
            if any(abs(float(row["theta"]) - theta) < 1e-12 for theta in selected)
        ]
        if len(summary) != len(selected):
            raise SystemExit("one or more requested theta values are absent")
    theta_labels = [float(row["theta"]) for row in summary]
    x_value = summary[0]["x"]
    h_value = summary[0]["h"]
    if any(row["x"] != x_value or row["h"] != h_value for row in summary):
        raise SystemExit("plot one X,h run at a time")

    bin_groups = {}
    for row in bins:
        key = (float(row["theta"]), row["series"])
        bin_groups.setdefault(key, []).append(row)
    for rows in bin_groups.values():
        rows.sort(key=lambda row: int(row["bin_index"]))

    series_order = ["PS_right", "SP_left", "SS_left", "SS_right"]
    heat_rows = []
    for theta in theta_labels:
        for series in series_order:
            rows = bin_groups.get((theta, series), [])
            if rows:
                heat_rows.append((theta, series, rows))

    global_heat_max = 0.0
    for _, _, rows in heat_rows:
        counts = [int(row["count"]) for row in rows]
        total = sum(counts)
        if total:
            global_heat_max = max(global_heat_max, max(counts) / total)

    width = 1220
    left = 145
    right = 45
    plot_width = width - left - right
    top = 72
    sector_height = 300
    heat_top = 475
    heat_row_height = 24
    heat_height = heat_row_height * len(heat_rows)
    height = max(760, int(heat_top + heat_height + 105))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        svg_text(width / 2, 30, "Rough-pair parity diagnostics", 22, "middle", "bold"),
        svg_text(
            width / 2,
            52,
            f"starts n in [{x_value}, {2 * int(x_value)}), h={h_value}",
            13,
            "middle",
            fill="#555",
        ),
    ]

    # Four-sector stacked bars.
    parts.append(svg_text(left, top - 12, "candidate-sector shares", 15, weight="bold"))
    for tick in range(6):
        share = tick / 5
        y = top + sector_height * (1 - share)
        parts.append(
            f'<line x1="{left}" y1="{y:.2f}" x2="{left + plot_width}" y2="{y:.2f}" '
            'stroke="#d9d9d9" stroke-width="1"/>'
        )
        parts.append(svg_text(left - 10, y + 4, f"{share:.1f}", 11, "end", fill="#555"))

    group_width = plot_width / len(summary)
    bar_width = min(95.0, group_width * 0.62)
    max_inversion_error = 0
    max_sector_error = 0
    for index, row in enumerate(summary):
        center = left + group_width * (index + 0.5)
        x0 = center - bar_width / 2
        total = int(row["A"])
        counts = {
            "PP": int(row["N_PP"]),
            "PS": int(row["N_PS"]),
            "SP": int(row["N_SP"]),
            "SS": int(row["N_SS"]),
        }
        bottom = top + sector_height
        for sector in ("PP", "PS", "SP", "SS"):
            share = counts[sector] / total if total else 0.0
            rect_height = share * sector_height
            bottom -= rect_height
            parts.append(
                f'<rect x="{x0:.2f}" y="{bottom:.2f}" width="{bar_width:.2f}" '
                f'height="{rect_height:.2f}" fill="{SECTOR_COLORS[sector]}">'
                f'<title>{sector}: {counts[sector]} ({share:.6%})</title></rect>'
            )
            if share >= 0.085:
                parts.append(
                    svg_text(
                        center,
                        bottom + rect_height / 2 + 4,
                        f"{share:.1%}",
                        12,
                        "middle",
                        weight="bold",
                        fill="white",
                    )
                )
        theta = float(row["theta"])
        parts.append(svg_text(center, top + sector_height + 23, f"{theta:.3f}", 13, "middle"))
        max_inversion_error = max(max_inversion_error, abs(int(row["inversion_error"])))
        max_sector_error = max(max_sector_error, abs(int(row["sector_sum_error"])))

    legend_x = left + plot_width - 300
    for index, sector in enumerate(("PP", "PS", "SP", "SS")):
        lx = legend_x + index * 75
        parts.append(f'<rect x="{lx}" y="{top - 24}" width="13" height="13" fill="{SECTOR_COLORS[sector]}"/>')
        parts.append(svg_text(lx + 18, top - 13, sector, 11))

    check_color = "#1b7f3a" if max_inversion_error == 0 and max_sector_error == 0 else "#b42318"
    parts.append(
        svg_text(
            left,
            top + sector_height + 47,
            f"max |inversion error|={max_inversion_error}; max |sector-sum error|={max_sector_error}",
            11,
            fill=check_color,
            weight="bold",
        )
    )

    # Least-prime-factor heatmap on one common row-share color scale.
    parts.append(
        svg_text(
            left,
            heat_top - 22,
            "least-prime-factor distribution within each contamination series",
            15,
            weight="bold",
        )
    )
    parts.append(
        svg_text(
            left,
            heat_top - 7,
            "common color scale: darkest = {:.1%} of a row; alpha = log(P^-(coordinate)) / log(2X+h)".format(global_heat_max),
            12,
            fill="#666",
        )
    )
    bin_count = len(heat_rows[0][2]) if heat_rows else 1
    cell_width = plot_width / bin_count
    for row_index, (theta, series, rows) in enumerate(heat_rows):
        y = heat_top + row_index * heat_row_height
        counts = [int(row["count"]) for row in rows]
        total = sum(counts)
        shares = [count / total if total else 0.0 for count in counts]
        label = f"{theta:.3f}  {series}"
        parts.append(svg_text(left - 8, y + heat_row_height * 0.72, label, 14, "end", fill="#444"))
        for bin_index, (source_row, count, share) in enumerate(zip(rows, counts, shares)):
            intensity = share / global_heat_max if global_heat_max else 0.0
            fill = heat_color(intensity)
            x = left + bin_index * cell_width
            parts.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell_width + 0.2:.2f}" '
                f'height="{heat_row_height - 1:.2f}" fill="{fill}">'
                f'<title>theta={theta:.6g}, {series}, '
                f'alpha=[{source_row["alpha_lo"]},{source_row["alpha_hi"]}), '
                f'count={count}, row share={share:.6%}</title></rect>'
            )

    axis_y = heat_top + heat_height + 5
    parts.append(
        f'<line x1="{left}" y1="{axis_y}" x2="{left + plot_width}" y2="{axis_y}" '
        'stroke="#444" stroke-width="1"/>'
    )
    for tick in range(6):
        alpha = tick / 10
        x = left + 2 * alpha * plot_width
        parts.append(f'<line x1="{x:.2f}" y1="{axis_y}" x2="{x:.2f}" y2="{axis_y + 5}" stroke="#444"/>')
        parts.append(svg_text(x, axis_y + 19, f"{alpha:.1f}", 10, "middle"))
    parts.append(svg_text(left + plot_width / 2, axis_y + 38, "least-factor exponent alpha", 12, "middle"))

    footer_y = height - 24
    parts.append(
        svg_text(
            width / 2,
            footer_y,
            "Diagnostic only: a finite-scale factor-size pattern is not a twin-prime lower bound.",
            11,
            "middle",
            fill="#666",
        )
    )
    parts.append("</svg>")

    output_path = Path(args.output)
    output_path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
