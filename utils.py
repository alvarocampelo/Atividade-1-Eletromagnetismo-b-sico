"""
utils.py
--------
Funções utilitárias compartilhadas entre os problemas da Atividade 1.
Disciplina: Eletromagnetismo Básico – TI0166 | Prof. João Batista | UFC
"""

import numpy as np

# Constante eletrostática de Coulomb [N·m²/C²]
K = 8.9875517923e9


def calculate_force_on_charge(N, charges, coordinates, eval_charge, eval_coord):
    """
    Calcula a força elétrica total sobre uma carga pontual
    devido a N outras cargas no espaço livre (Lei de Coulomb – superposição).

    Parâmetros
    ----------
    N            : int   – número de cargas fonte
    charges      : list  – magnitudes [Q1, Q2, ..., QN] em Coulombs
    coordinates  : list  – posições [(x1,y1,z1), ..., (xN,yN,zN)] em metros
    eval_charge  : float – carga sobre a qual a força é calculada [C]
    eval_coord   : tuple – posição da carga avaliada (x, y, z) [m]

    Retorna
    -------
    total_force : np.ndarray shape (3,) – vetor força [N]
    """
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
    """
    Calcula o campo elétrico em obs_point devido a N cargas pontuais.

    Parâmetros
    ----------
    charges      : list  – [Q1, ..., QN] em Coulombs
    coordinates  : list  – [(x1,y1,z1), ..., (xN,yN,zN)] em metros
    obs_point    : array – ponto de observação (x, y, z) [m]

    Retorna
    -------
    E : np.ndarray shape (3,) – vetor campo elétrico [V/m]
    """
    obs_point = np.array(obs_point, dtype=float)
    E = np.zeros(3)
    for qi, ri in zip(charges, coordinates):
        R = obs_point - np.array(ri, dtype=float)
        E += K * qi / np.linalg.norm(R)**3 * R
    return E


def normalize_vector(vector, max_length):
    """
    Reescala um vetor para o comprimento max_length,
    preservando sua direção (para fins de visualização).

    Parâmetros
    ----------
    vector     : array – vetor a ser normalizado
    max_length : float – comprimento desejado

    Retorna
    -------
    np.ndarray – vetor reescalado
    """
    magnitude = np.linalg.norm(vector)
    if magnitude == 0:
        return vector
    return vector * (max_length / magnitude)


def add_vector_arrow(fig, origin, direction, name="Vetor", color="green",
                     line_width=5, cone_scale=0.15, max_range=1.0):
    """
    Adiciona um vetor 3D com ponta de seta (go.Cone) a uma figura Plotly.

    Parâmetros
    ----------
    fig        : go.Figure – figura Plotly existente
    origin     : array (3,) – ponto de origem do vetor
    direction  : array (3,) – direção e magnitude normalizada do vetor
    name       : str  – rótulo na legenda
    color      : str  – cor da linha
    line_width : int  – espessura da linha
    cone_scale : float – fração de max_range para o tamanho do cone
    max_range  : float – escala de referência do gráfico
    """
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
