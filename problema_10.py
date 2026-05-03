"""
problema_10.py
--------------
Problema 10 da Lista 2 – TI0166
Campo elétrico em P(0,0,6) devido a quatro cargas nos vértices de um quadrado 4×4 m.

Configuração (z = 0):
  +Q  em (−2, +2, 0)      +2Q  em (+2, +2, 0)
 −2Q  em (−2, −2, 0)       −Q  em (+2, −2, 0)

Com Q = 15 µC

Disciplina: Eletromagnetismo Básico – TI0166 | Prof. João Batista | UFC
"""

import numpy as np
import plotly.graph_objects as go
from utils import K, electric_field, normalize_vector, add_vector_arrow


def main():
    # ------------------------------------------------------------------ #
    # Dados do problema                                                    #
    # ------------------------------------------------------------------ #
    Q = 15e-6  # C

    posicoes = np.array([
        [-2.,  2., 0.],   # +Q
        [ 2.,  2., 0.],   # +2Q
        [-2., -2., 0.],   # -2Q
        [ 2., -2., 0.],   # -Q
    ])
    cargas  = np.array([Q, 2*Q, -2*Q, -Q])
    rotulos = ["+Q", "+2Q", "−2Q", "−Q"]

    P = np.array([0., 0., 6.])  # ponto de observação

    # ------------------------------------------------------------------ #
    # Cálculo                                                              #
    # ------------------------------------------------------------------ #
    E = electric_field(cargas, posicoes, P)

    print("=" * 55)
    print("Problema 10 – Campo Elétrico em P(0,0,6)")
    print("=" * 55)
    print(f"E   = ({E[0]:.2f} ax + {E[1]:.2f} ay + {E[2]:.2f} az) V/m")
    print(f"|E| = {np.linalg.norm(E):.2f} V/m")
    print(f"Soma das cargas = {cargas.sum()*1e6:.1f} µC  (deve ser zero → Ez = 0)")

    # ------------------------------------------------------------------ #
    # Visualização 3D                                                      #
    # ------------------------------------------------------------------ #
    all_pts   = np.vstack([posicoes, P])
    max_range = np.ptp(all_pts, axis=0).max()
    E_norm    = normalize_vector(E, 0.5 * max_range)

    fig = go.Figure()

    for ri, qi, lbl in zip(posicoes, cargas, rotulos):
        cor  = "blue" if qi > 0 else "red"
        size = abs(qi / Q) * 5 + 4
        fig.add_trace(go.Scatter3d(
            x=[ri[0]], y=[ri[1]], z=[ri[2]],
            mode='markers+text', text=lbl, textposition="top center",
            marker=dict(size=size, color=cor), name=lbl
        ))

    fig.add_trace(go.Scatter3d(
        x=[P[0]], y=[P[1]], z=[P[2]],
        mode='markers+text', text="P(0,0,6)",
        textposition="top center",
        marker=dict(size=8, color='green'), name="Ponto P"
    ))

    add_vector_arrow(fig, P, E_norm,
                     name="Campo E", color="orange",
                     cone_scale=0.3, max_range=max_range)

    fig.update_layout(
        title="Problema 10 – Campo Elétrico em P(0, 0, 6)",
        scene=dict(xaxis_title="X (m)",
                   yaxis_title="Y (m)",
                   zaxis_title="Z (m)")
    )
    fig.show()


if __name__ == "__main__":
    main()
