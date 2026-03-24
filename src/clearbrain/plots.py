# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import plotly.graph_objects as go



# ================================================================
# 1. Section: Functions
# ================================================================
def plot_3d_clearD(
    points: np.ndarray,
    centerline: np.ndarray,
    sample_name: str,
    plot_subsample: int,
) -> go.Figure:
    reduced_points = points[::plot_subsample]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=reduced_points[:, 0],
            y=reduced_points[:, 1],
            z=reduced_points[:, 2],
            mode="markers",
            marker=dict(size=2.3, color="#777777", opacity=0.35),
            name="High-density cFos cells",
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=centerline[:, 0],
            y=centerline[:, 1],
            z=centerline[:, 2],
            mode="lines",
            line=dict(color="#ff2d2d", width=9),
            name="Spinal Cord Orientation Line",
        )
    )

    fig.update_layout(
        title=f"{sample_name} - Spinal Cord Orientation Line",
        scene=dict(
            aspectmode="data",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor="white",
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(x=0.02, y=0.98),
    )

    return fig
