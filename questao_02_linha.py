"""
Questão 2 da Atividade 1
Linha de carga finita: solução analítica vs. modelagem por cargas pontuais.

Configuração:
  - Linha ao longo do eixo z, centrada na origem
  - Comprimento L = 1 m, carga total Q = 10 C → ρ_L = 10 C/m
  - Ponto de observação: P(0, 10, 0)
"""

import numpy as np
import plotly.graph_objects as go
from utils import K


# Resultado analítico
def E_analitico_linha(Q, L, rho):
    return K * Q / (rho * np.sqrt(rho**2 + (L / 2)**2))


# Modelo de cargas pontuais
def campo_linha_pontual(N, Q, L, P):
    
    z_coords = np.linspace(-L / 2, L / 2, N, endpoint=False) + L / (2 * N)
    qi = Q / N
    E  = np.zeros(3)
    for z in z_coords:
        R = P - np.array([0., 0., z])
        E += K * qi / np.linalg.norm(R)**3 * R
    return E


def main():
    Q = 10.0
    L = 1.0 
    P = np.array([0., 10., 0.])
    rho = np.linalg.norm(P[:2])

    # Resultados
    E_an = E_analitico_linha(Q, L, rho)

    print("=" * 60)
    print("Questão 2 – Linha de Carga Finita  |  P(0, 10, 0)")
    print("=" * 60)
    print(f"Analítico:  Ey = {E_an:.6e} V/m")
    print()
    print(f"{'N':>4}  {'Ey [V/m]':>18}  {'Erro [%]':>10}")
    print("-" * 36)

    Ns_teste = [10, 15, 30]
    for N in Ns_teste:
        E   = campo_linha_pontual(N, Q, L, P)
        err = abs(E[1] - E_an) / abs(E_an) * 100
        print(f"{N:>4}  {E[1]:>18.6e}  {err:>10.4f}")

    # Curva de convergência
    Ns      = list(range(5, 101, 5))
    Ey_vals = [campo_linha_pontual(N, Q, L, P)[1] for N in Ns]
    erros   = [abs(Ey - E_an) / abs(E_an) * 100 for Ey in Ey_vals]

    # Gráfico: Ey vs N
    fig1 = go.Figure()
    fig1.add_hline(y=E_an, line_dash='dash', line_color='red',
                   annotation_text='Analítico', annotation_position='top right')
    fig1.add_trace(go.Scatter(
        x=Ns, y=Ey_vals, mode='lines+markers',
        line=dict(color='blue'), marker=dict(size=5),
        name='Computacional'
    ))
    fig1.update_layout(
        title='Questão 2 – Convergência: Linha de carga em P(0, 10, 0)',
        xaxis_title='Número de cargas N',
        yaxis_title='Ey (V/m)'
    )
    fig1.show()

    # Gráfico de erro relativo
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=Ns, y=erros, mode='lines+markers',
        line=dict(color='orange'), marker=dict(size=5),
        name='Erro relativo (%)'
    ))
    fig2.update_layout(
        title='Questão 2 – Erro relativo (%) vs N  [escala log]',
        xaxis_title='N',
        yaxis_title='Erro (%)',
        yaxis_type='log'
    )
    fig2.show()

    #Comparação com linha infinita
    rhoL   = Q / L
    E_inf  = 2 * K * rhoL / rho
    print(f"\nLinha infinita: E∞ = {E_inf:.4e} V/m")
    print(f"Razão E_finita / E_infinita = {E_an / E_inf:.4f}  (L/ρ = {L/rho:.2f})")


if __name__ == "__main__":
    main()
