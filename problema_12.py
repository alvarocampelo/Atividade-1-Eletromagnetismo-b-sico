"""
problema_12.py
--------------
Problema 12 da Lista 2 – TI0166
Campo elétrico de uma carga Q = −10⁻⁸ C situada na origem.

(a) Expressão geral E(x, y, z)
(b) Valor em P(1, 1, 2) m

Disciplina: Eletromagnetismo Básico – TI0166 | Prof. João Batista | UFC
"""

import numpy as np
import plotly.graph_objects as go
from utils import K, electric_field, normalize_vector, add_vector_arrow


def E_geral(x, y, z, Q, k=K):
    """
    Campo elétrico de uma carga Q na origem, expresso em coordenadas cartesianas.

    E(x,y,z) = k·Q·(x ax + y ay + z az) / (x²+y²+z²)^(3/2)
    """
    r2 = x**2 + y**2 + z**2
    return k * Q * np.array([x, y, z]) / r2**1.5


def main():
    Q = -1e-8   # C

    print("=" * 55)
    print("Problema 12 – Campo de Carga na Origem")
    print("=" * 55)
    print(f"k·Q = {K * Q:.4f} V·m")
    print("E(x,y,z) = -89.875·(x ax + y ay + z az) / (x²+y²+z²)^(3/2)  [V/m]")

    # ------------------------------------------------------------------ #
    # Valor em P(1, 1, 2)                                                  #
    # ------------------------------------------------------------------ #
    P = np.array([1., 1., 2.])
    E = electric_field([Q], [(0., 0., 0.)], P)

    print(f"\nEm P(1, 1, 2):")
    print(f"E   = ({E[0]:.3f} ax + {E[1]:.3f} ay + {E[2]:.3f} az) V/m")
    print(f"|E| = {np.linalg.norm(E):.4f} V/m")

    # ------------------------------------------------------------------ #
    # Perfil de |E| ao longo do eixo z (com pequeno offset)               #
    # ------------------------------------------------------------------ #
    print("\nPerfil de |E| ao longo do eixo z (x = y = 0.01 m):")
    z_vals = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
    for z in z_vals:
        Ep = E_geral(0.01, 0.01, z, Q)
        print(f"  z = {z:5.1f} m  →  |E| = {np.linalg.norm(Ep):.4f} V/m")

    # ------------------------------------------------------------------ #
    # Visualização 3D                                                      #
    # ------------------------------------------------------------------ #
    max_range = 3.0
    E_norm    = normalize_vector(E, 0.5)

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers+text', text="Q = −10 nC",
        textposition="top center",
        marker=dict(size=10, color='red'), name="Carga Q"
    ))
    fig.add_trace(go.Scatter3d(
        x=[P[0]], y=[P[1]], z=[P[2]],
        mode='markers+text', text="P(1,1,2)",
        textposition="top center",
        marker=dict(size=7, color='green'), name="Ponto P"
    ))

    add_vector_arrow(fig, P, E_norm,
                     name="Vetor E em P", color="blue",
                     cone_scale=0.15, max_range=max_range)

    # Linha tracejada: origem → P (indica direção do campo)
    fig.add_trace(go.Scatter3d(
        x=[0, P[0]], y=[0, P[1]], z=[0, P[2]],
        mode='lines',
        line=dict(color='gray', width=2, dash='dash'),
        name='Origem → P'
    ))

    fig.update_layout(
        title="Problema 12 – Campo de Q = −10 nC na origem em P(1,1,2)",
        scene=dict(xaxis_title="X (m)",
                   yaxis_title="Y (m)",
                   zaxis_title="Z (m)")
    )
    fig.show()


if __name__ == "__main__":
    main()
