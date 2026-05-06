"""
utils.py

Funções utilitárias retiradas do collab, e extras, para a Atividade 1.
Disciplina: Eletromagnetismo Básico – TI0166 | Prof. João Batista | UFC
"""

import numpy as np

# Constante de Coulomb [N·m²/C²]
K = 8.9875517923e9


def calculate_force_on_charge(N, charges, coordinates, eval_charge, eval_coord):
    eval_coord  = np.array(eval_coord, dtype=float)
    total_force = np.zeros(3)

    for i in range(N):
        r_vec = eval_coord - np.array(coordinates[i], dtype=float)
        r_mag = np.linalg.norm(r_vec)
        if r_mag != 0:
            force_magnitude = K * eval_charge * charges[i] / r_mag**2
            total_force    += force_magnitude * (r_vec / r_mag)

    return total_force


def electric_field(charges, coordinates, obs_point):
    obs_point = np.array(obs_point, dtype=float)
    E = np.zeros(3)
    for qi, ri in zip(charges, coordinates):
        R = obs_point - np.array(ri, dtype=float)
        E += K * qi / np.linalg.norm(R)**3 * R
    return E


def normalize_vector(vector, max_length):
    magnitude = np.linalg.norm(vector)
    if magnitude == 0:
        return vector
    return vector * (max_length / magnitude)


def add_vector_arrow(fig, origin, direction, name="Vetor", color="green",
                     line_width=5, cone_scale=0.15, max_range=1.0):
    import plotly.graph_objects as go

    tip = np.array(origin) + np.array(direction)

    fig.add_trace(go.Scatter3d(
        x=[origin[0], tip[0]],
        y=[origin[1], tip[1]],
        z=[origin[2], tip[2]],
        mode='lines',
        line=dict(color=color, width=line_width),
        name=name
    ))
    fig.add_trace(go.Cone(
        x=[tip[0]], y=[tip[1]], z=[tip[2]],
        u=[direction[0]], v=[direction[1]], w=[direction[2]],
        colorscale=[[0, color], [1, color]],
        sizemode='absolute',
        sizeref=cone_scale * max_range,
        showscale=False,
        name=f"{name} (ponta)"
    ))
