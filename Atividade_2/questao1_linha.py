import numpy as np
import matplotlib.pyplot as plt

k = 8.9875517923e9


def potencial_linha_analitico(Q, L, x, y, z):
    rho = np.sqrt(x**2 + y**2)
    if rho == 0:
        return None
    za = z + L / 2
    zb = z - L / 2
    return (k * Q / L) * np.log(
        (za + np.sqrt(za**2 + rho**2)) /
        (zb + np.sqrt(zb**2 + rho**2))
    )


def potencial_linha_computacional(Q, L, N, x, y, z):
    z_coords = np.linspace(-L/2, L/2, N, endpoint=False) + L / (2 * N)
    dq = Q / N
    P = np.array([x, y, z])
    ri = np.column_stack([np.zeros(N), np.zeros(N), z_coords])
    dists = np.linalg.norm(P - ri, axis=1)
    return np.sum(k * dq / dists)


def main():
    Q = 1e-6
    L = 2.0
    pontos = [(1, 0, 0), (0, 2, 1), (1, 1, 3)]
    N_vals = [10, 50, 100]
    cores = ['tab:blue', 'tab:orange', 'tab:green']
    marcadores = ['o', 's', '^']
    estilos_linha = ['--', '-.', ':']

    print("=" * 65)
    print(f"Linha de carga: Q = {Q:.2e} C, L = {L} m (eixo z, centrada na origem)")
    print("=" * 65)

    erros = []
    for (x, y, z) in pontos:
        V_an = potencial_linha_analitico(Q, L, x, y, z)
        erros_ponto = []
        print(f"\nPonto P = ({x}, {y}, {z})")
        print(f"  Analítico      : V = {V_an:.6e} V")
        for N in N_vals:
            V_comp = potencial_linha_computacional(Q, L, N, x, y, z)
            erro = abs(V_comp - V_an) / abs(V_an) * 100
            erros_ponto.append(erro)
            print(f"  N = {N:3d}         : V = {V_comp:.6e} V  |  erro = {erro:.4f}%")
        erros.append(erros_ponto)

    # Visualização L
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(
        f"Questão 1 – Linha de Carga Finita  (Q = {Q:.1e} C, L = {L} m)",
        fontsize=13, fontweight='bold'
    )

    # Gráfico 1: convergência
    for i, (x, y, z) in enumerate(pontos):
        ax1.plot(N_vals, erros[i],
                 marker=marcadores[i], color=cores[i],
                 linewidth=2, markersize=7,
                 label=f"P = ({x}, {y}, {z})")
    ax1.set_xlabel("N  (número de cargas pontuais)", fontsize=11)
    ax1.set_ylabel("Erro relativo (%)", fontsize=11)
    ax1.set_title("Convergência: erro relativo vs. N", fontsize=11)
    ax1.set_xticks(N_vals)
    ax1.set_yscale('log')
    ax1.legend(fontsize=9)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Gráfico 2: perfil radial V(ρ) no plano z = 0
    rho_vals = np.linspace(0.5, 5.0, 300)
    V_an_rho = np.array([potencial_linha_analitico(Q, L, rho, 0, 0)
                         for rho in rho_vals])
    ax2.plot(rho_vals, V_an_rho, 'k-', linewidth=2.5,
             label='Analítico', zorder=5)
    for N, ls, cor in zip(N_vals, estilos_linha, cores):
        V_comp_rho = np.array([potencial_linha_computacional(Q, L, N, rho, 0, 0)
                               for rho in rho_vals])
        ax2.plot(rho_vals, V_comp_rho, ls, color=cor, linewidth=1.8,
                 label=f'N = {N}')
    ax2.set_xlabel("ρ (m)  [y = 0, z = 0]", fontsize=11)
    ax2.set_ylabel("V (V)", fontsize=11)
    ax2.set_title("Perfil de potencial V(ρ)  no plano z = 0", fontsize=11)
    ax2.legend(fontsize=9)
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig("questao1_linha.png", dpi=150, bbox_inches='tight')
    print("\nGráfico salvo em questao1_linha.png")
    plt.show()


if __name__ == "__main__":
    main()