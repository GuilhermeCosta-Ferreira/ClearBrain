# ================================================================
# 0. Section: IMPORTS
# ================================================================
import json
import os

import numpy as np
import plotly.graph_objects as go

from pathlib import Path



# ================================================================
# 1. Section: INPUTS
# ================================================================
DATA_FOLDER: Path = Path("data")
PLOT_FOLDER: Path = Path("out")

X_SCALE: float = 2.22
Y_SCALE: float = 1.0
Z_SCALE: float = 1.0

PLOT_SUBSAMPLE: int = 80            # clean & fast plotting
PRISM_HALF_WIDTH: int = 1000        # ← 2000×2000 square base (as requested)
PRISM_HALF_THICKNESS: int = 250     # ← 500 units thick
N_CUTS: int = 10                    # 10 axial cuts

JSON_FILES: list = ["32B_SC_sensitive.json"]



# ================================================================
# 2. Section: MAIN
# ================================================================
if __name__ == "__main__":
    print("Creating HTML with 10 larger axial cut prisms (2000×2000 × 500 thick)...\n")

    for filename in JSON_FILES:
        filepath = os.path.join(DATA_FOLDER, filename)
        if not os.path.exists(filepath):
            continue

        sample_name = os.path.splitext(filename)[0]
        print(f"Processing {sample_name}...")

        # === LOAD POINTS ===
        with open(filepath, "r") as f:
            points_full = np.array(json.load(f))
        points_full[:, 0] *= X_SCALE
        points_full[:, 1] *= Y_SCALE
        points_full[:, 2] *= Z_SCALE

        reduced_points = points_full[::PLOT_SUBSAMPLE]

        # === LOAD SPINAL CORD ORIENTATION LINE ===
        orientation_path = os.path.join(PLOT_FOLDER, f"{sample_name}_spinal_cord_orientation_line.npy")
        if not os.path.exists(orientation_path):
            print(f"❌ Orientation line .npy not found for {sample_name}. Run the previous script first!")
            continue

        orientation_line = np.load(orientation_path)
        print(f"   Loaded orientation line with {len(orientation_line)} points")

        # === SELECT 10 CUTS FURTHER FROM EXTREMITIES (5%–95%) ===
        start_idx = int(0.05 * len(orientation_line))
        end_idx   = int(0.95 * len(orientation_line))
        indices = np.linspace(start_idx, end_idx, N_CUTS, dtype=int)

        # === PLOT ===
        fig = go.Figure()

        # Grey cFos points
        fig.add_trace(go.Scatter3d(
            x=reduced_points[:, 0],
            y=reduced_points[:, 1],
            z=reduced_points[:, 2],
            mode='markers',
            marker=dict(size=2.3, color='#777777', opacity=0.35),
            name='High-density cFos cells'
        ))

        # Red Spinal Cord Orientation Line
        fig.add_trace(go.Scatter3d(
            x=orientation_line[:, 0],
            y=orientation_line[:, 1],
            z=orientation_line[:, 2],
            mode='lines',
            line=dict(color='#ff2d2d', width=9),
            name='Spinal Cord Orientation Line'
        ))

        # === ADD 10 LARGER 3D PRISMS ===
        print("   Adding 10 larger axial cut prisms (2000×2000 × 500)...")
        for i, idx in enumerate(indices):
            P = orientation_line[idx]

            # Tangent vector
            if idx < len(orientation_line) - 1:
                T = orientation_line[idx + 1] - P
            else:
                T = P - orientation_line[idx - 1]
            T /= np.linalg.norm(T)

            # Perpendicular basis vectors
            arbitrary = np.array([1., 0., 0.])
            if abs(np.dot(T, arbitrary)) > 0.99:
                arbitrary = np.array([0., 1., 0.])
            U = np.cross(T, arbitrary)
            U /= np.linalg.norm(U)
            V = np.cross(T, U)

            # 8 vertices of the prism
            half_w = PRISM_HALF_WIDTH
            half_t = PRISM_HALF_THICKNESS
            front = P - half_t * T
            back  = P + half_t * T

            v = [
                front + half_w*U + half_w*V,
                front + half_w*U - half_w*V,
                front - half_w*U + half_w*V,
                front - half_w*U - half_w*V,
                back  + half_w*U + half_w*V,
                back  + half_w*U - half_w*V,
                back  - half_w*U + half_w*V,
                back  - half_w*U - half_w*V
            ]

            verts_x = [v[j][0] for j in range(8)]
            verts_y = [v[j][1] for j in range(8)]
            verts_z = [v[j][2] for j in range(8)]

            # Mesh3d faces
            faces = [
                0,1,3, 0,3,2,
                4,5,7, 4,7,6,
                0,1,5, 0,5,4,
                1,3,7, 1,7,5,
                3,2,6, 3,6,7,
                2,0,4, 2,4,6
            ]

            fig.add_trace(go.Mesh3d(
                x=verts_x, y=verts_y, z=verts_z,
                i=faces[0::3], j=faces[1::3], k=faces[2::3],
                color='lightcyan',
                opacity=0.35,
                flatshading=True,
                name=f'Axial Cut {i+1}',
                showlegend=True
            ))

        fig.update_layout(
            title=f"{sample_name} — Spinal Cord Orientation Line with 10 Axial Cuts (2000×2000 × 500)",
            scene=dict(
                aspectmode='data',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                bgcolor='white'
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            legend=dict(x=0.02, y=0.98, title="Axial Cuts")
        )

        html_path = os.path.join(PLOT_FOLDER, f"{sample_name}_spinal_cord_orientation_line_with_10_axial_cuts_2000x2000.html")
        fig.write_html(html_path)
        print(f"   ✅ HTML with 2000×2000 × 500 prisms saved: {html_path}\n")

    print("🎉 DONE!")
    print("Open the new *_with_10_axial_cuts_2000x2000.html files in your browser.")
    print("The 10 axial cuts are now 2000×2000 squares, 500 units thick, and placed away from the extremities.")
    print("Each prism is clearly labeled 'Axial Cut 1', 'Axial Cut 2', ... in the legend.")
