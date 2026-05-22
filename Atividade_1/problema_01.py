"""
Problema 1 da Lista 2
Força e campo elétrico de duas cargas pontuais sobre uma terceira carga em P(1,-3,7).
"""

import numpy as np
import plotly.graph_objects as go
from utils import K, calculate_force_on_charge, normalize_vector, add_vector_arrow


def main():
    #Dados do problema
    N           = 2
    charges     = [5e-9, -2e-9]
    coordinates = [(2., 0., 4.),
                   (-3., 0., 5.)]
    eval_charge = 1e-9
    eval_coord  = (1., -3., 7.)

    # Cálculo
    F = calculate_force_on_charge(N, charges, coordinates, eval_charge, eval_coord)
    E = F / eval_charge

    print("=" * 55)
    print("Problema 1 – Força e Campo Elétrico")
    print("=" * 55)
    print(f"F = {F * 1e9} nN")
    print(f"E = {E} V/m")
    print(f"|E| = {np.linalg.norm(E):.4f} V/m")

    # Visualização 3D
    all_pts   = np.array(list(coordinates) + [eval_coord])
    max_range = np.ptp(all_pts, axis=0).max()
    F_norm    = normalize_vector(F, 0.15 * max_range)

    fig = go.Figure()

    labels = [
        f"Q1 = {charges[0]*1e9:.0f} nC",
        f"Q2 = {charges[1]*1e9:.0f} nC",
    ]
    colors = ["blue", "purple"]
    for coord, lbl, clr in zip(coordinates, labels, colors):
        fig.add_trace(go.Scatter3d(
            x=[coord[0]], y=[coord[1]], z=[coord[2]],
            mode='markers+text', text=lbl, textposition="top center",
            marker=dict(size=7, color=clr), name=lbl
        ))

    fig.add_trace(go.Scatter3d(
        x=[eval_coord[0]], y=[eval_coord[1]], z=[eval_coord[2]],
        mode='markers+text',
        text=f"P: Q = {eval_charge*1e9:.0f} nC",
        textposition="top center",
        marker=dict(size=9, color='red'),
        name="Carga avaliada"
    ))

    add_vector_arrow(fig, eval_coord, F_norm,
                     name="Força resultante", color="green",
                     cone_scale=0.1, max_range=max_range)

    fig.update_layout(
        title="Problema 1 – Força elétrica em P(1, −3, 7)",
        scene=dict(xaxis_title="X (m)",
                   yaxis_title="Y (m)",
                   zaxis_title="Z (m)")
    )
    fig.show()


if __name__ == "__main__":
    main()
