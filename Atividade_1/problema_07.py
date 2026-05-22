"""
Problema 7 da Lista 2
Força resultante sobre Q3 devido a Q1 e Q2.

Q1 = +2 µC em P1(1, 2, 1) m
Q2 = −4 µC em P2(−1, 0, 2) m
Q3 = −3 µC em P3(2, 1, 3) m 
"""

import numpy as np
import plotly.graph_objects as go
from utils import K, calculate_force_on_charge, normalize_vector, add_vector_arrow


def main():
    # Dados
    charges     = [2e-6, -4e-6]
    coordinates = [(1., 2., 1.), (-1., 0., 2.)]
    Q3          = -3e-6
    P3          = (2., 1., 3.)

    N = len(charges)

    #Cálculo
    F_total = calculate_force_on_charge(N, charges, coordinates, Q3, P3)

    #Forças individuais para conferência
    F13 = calculate_force_on_charge(1, [charges[0]], [coordinates[0]], Q3, P3)
    F23 = calculate_force_on_charge(1, [charges[1]], [coordinates[1]], Q3, P3)

    print("=" * 55)
    print("Problema 7 – Força sobre Q3")
    print("=" * 55)
    print(f"F13    = {F13 * 1e3} mN")
    print(f"F23    = {F23 * 1e3} mN")
    print(f"F_Q3   = {F_total * 1e3} mN")
    print(f"|F_Q3| = {np.linalg.norm(F_total) * 1e3:.4f} mN")

    #Visualização 3D
    all_pts   = np.array(list(coordinates) + [P3])
    max_range = np.ptp(all_pts, axis=0).max()
    F_norm    = normalize_vector(F_total, 0.3 * max_range)

    fig = go.Figure()

    info = [
        ("Q1 = +2 µC", "blue"),
        ("Q2 = −4 µC", "purple"),
    ]
    for coord, (lbl, clr) in zip(coordinates, info):
        fig.add_trace(go.Scatter3d(
            x=[coord[0]], y=[coord[1]], z=[coord[2]],
            mode='markers+text', text=lbl, textposition="top center",
            marker=dict(size=8, color=clr), name=lbl
        ))

    fig.add_trace(go.Scatter3d(
        x=[P3[0]], y=[P3[1]], z=[P3[2]],
        mode='markers+text', text="Q3 = −3 µC",
        textposition="top center",
        marker=dict(size=10, color='red'),
        name="Q3 (avaliada)"
    ))

    add_vector_arrow(fig, P3, F_norm,
                     name="Força resultante", color="green",
                     cone_scale=0.15, max_range=max_range)

    fig.update_layout(
        title="Problema 7 – Força sobre Q3",
        scene=dict(xaxis_title="X (m)",
                   yaxis_title="Y (m)",
                   zaxis_title="Z (m)")
    )
    fig.show()


if __name__ == "__main__":
    main()
