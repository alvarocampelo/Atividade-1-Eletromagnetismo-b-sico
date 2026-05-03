"""
questao_03_anel.py
------------------
Questão 3 da Atividade 1 – TI0166
Anel de carga: solução analítica vs. modelagem por cargas pontuais.

Configuração:
  - Anel no plano xy, centro em (0,0,0), raio a = 1 m
  - Carga total Q = 10 C → ρ_L = Q / (2π·a)
  - Ponto de observação: P(0, 0, 10)

Disciplina: Eletromagnetismo Básico – TI0166 | Prof. João Batista | UFC
"""

import numpy as np
import plotly.graph_objects as go
from utils import K


# ------------------------------------------------------------------ #
# Resultado analítico                                                  #
# ------------------------------------------------------------------ #
def E_analitico_anel(Q, a, h):
    """
    Campo axial de um anel de raio a e carga Q,
    em ponto sobre o eixo de simetria a altura h.

    Ez = k·Q·h / (a² + h²)^(3/2)
    """
    return K * Q * h / (a**2 + h**2)**1.5


# ------------------------------------------------------------------ #
# Modelo de cargas pontuais                                            #
# ------------------------------------------------------------------ #
def campo_anel_pontual(N, Q, a, P):
    """
    Modela o anel como N cargas pontuais igualmente espaçadas
    em ângulo e calcula E em P por superposição.
    """
    phi_vals = np.linspace(0, 2 * np.pi, N, endpoint=False)
    qi = Q / N
    E  = np.zeros(3)
    for phi in phi_vals:
        r_i = np.array([a * np.cos(phi), a * np.sin(phi), 0.])
        R   = P - r_i
        E  += K * qi / np.linalg.norm(R)**3 * R
    return E


def main():
    Q = 10.0            # C
    a = 1.0             # m (raio)
    h = 10.0            # m (altura de P)
    P = np.array([0., 0., h])

    # ------------------------------------------------------------------ #
    # Resultados                                                           #
    # ------------------------------------------------------------------ #
    E_an = E_analitico_anel(Q, a, h)

    print("=" * 60)
    print("Questão 3 – Anel de Carga  |  P(0, 0, 10)")
    print("=" * 60)
    print(f"Analítico:  Ez = {E_an:.6e} V/m")
    print()
    print(f"{'N':>4}  {'Ez [V/m]':>18}  {'Erro [%]':>10}")
    print("-" * 36)

    for N in [10, 15, 30]:
        E   = campo_anel_pontual(N, Q, a, P)
        err = abs(E[2] - E_an) / abs(E_an) * 100
        print(f"{N:>4}  {E[2]:>18.6e}  {err:>10.4f}")

    # ------------------------------------------------------------------ #
    # Curva de convergência                                                #
    # ------------------------------------------------------------------ #
    Ns      = list(range(5, 201, 5))
    Ez_vals = [campo_anel_pontual(N, Q, a, P)[2] for N in Ns]
    erros   = [abs(Ez - E_an) / abs(E_an) * 100 for Ez in Ez_vals]

    # Análise da ordem de convergência (regressão log-log)
    erros_arr = np.array(erros)
    Ns_arr    = np.array(Ns)
    mask      = erros_arr > 1e-10
    p         = np.polyfit(np.log(Ns_arr[mask]), np.log(erros_arr[mask]), 1)
    print(f"\nAnálise de convergência (regressão log-log):")
    print(f"  Inclinação p = {p[0]:.2f}  (esperado: −2 para quadratura trapezoidal)")

    # Gráfico: Ez vs N
    fig1 = go.Figure()
    fig1.add_hline(y=E_an, line_dash='dash', line_color='red',
                   annotation_text='Analítico', annotation_position='top right')
    fig1.add_trace(go.Scatter(
        x=Ns, y=Ez_vals, mode='lines+markers',
        line=dict(color='green'), marker=dict(size=5),
        name='Computacional'
    ))
    fig1.update_layout(
        title='Questão 3 – Convergência: Anel de carga em P(0, 0, 10)',
        xaxis_title='Número de cargas N',
        yaxis_title='Ez (V/m)'
    )
    fig1.show()

    # Gráfico: erro relativo (log) vs N
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=Ns, y=erros, mode='lines+markers',
        line=dict(color='purple'), marker=dict(size=5),
        name='Erro relativo (%)'
    ))
    fig2.update_layout(
        title='Questão 3 – Erro relativo (%) vs N  [escala log]  |  O(N⁻²)',
        xaxis_title='N',
        yaxis_title='Erro (%)',
        yaxis_type='log'
    )
    fig2.show()

    # ------------------------------------------------------------------ #
    # Comparação linha × anel                                             #
    # ------------------------------------------------------------------ #
    print("\nComparação de convergência  (N=30):")
    from questao_02_linha import campo_linha_pontual, E_analitico_linha
    rho_linha = np.linalg.norm(np.array([0., 10., 0.])[:2])
    E_an_l    = E_analitico_linha(Q, 1.0, rho_linha)
    E_l30     = campo_linha_pontual(30, Q, 1.0, np.array([0., 10., 0.]))
    err_l30   = abs(E_l30[1] - E_an_l) / abs(E_an_l) * 100
    err_a30   = abs(campo_anel_pontual(30, Q, a, P)[2] - E_an) / abs(E_an) * 100
    print(f"  Linha (N=30): erro = {err_l30:.4f}%")
    print(f"  Anel  (N=30): erro = {err_a30:.4f}%")
    print("  → Linha converge mais rápido pois ρ ≫ L (ponto distante).")


if __name__ == "__main__":
    main()
