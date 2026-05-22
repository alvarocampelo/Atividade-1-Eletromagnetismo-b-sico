import numpy as np
import matplotlib.pyplot as plt

k = 8.9875517923e9


def potencial_anel_eixo(Q, a, z):
    """Forma fechada exata para P sobre o eixo z (x = y = 0)."""
    return k * Q / np.sqrt(a**2 + z**2)


def potencial_anel_referencia(Q, a, x, y, z, N_ref=100_000):
    """Referência de alta precisão por integração discreta densa."""
    phi = np.linspace(0, 2 * np.pi, N_ref, endpoint=False)
    r_primes = np.column_stack([a * np.cos(phi), a * np.sin(phi), np.zeros(N_ref)])
    P = np.array([x, y, z])
    return np.sum(k * (Q / N_ref) / np.linalg.norm(P - r_primes, axis=1))


def potencial_anel_computacional(Q, a, N, x, y, z):
    phi = np.linspace(0, 2 * np.pi, N, endpoint=False)
    r_primes = np.column_stack([a * np.cos(phi), a * np.sin(phi), np.zeros(N)])
    P = np.array([x, y, z])
    return np.sum(k * (Q / N) / np.linalg.norm(P - r_primes, axis=1))


def main():
    Q = 1e-6
    a = 1.0
    pontos = [(0, 0, 2), (0, 0, 5), (0, 0, -1)]
    N_vals = [10, 50, 100]
    cores = ['tab:blue', 'tab:orange', 'tab:green']
    marcadores = ['o', 's', '^']
    estilos_linha = ['--', '-.', ':']

    print("=" * 65)
    print(f"Anel de carga: Q = {Q:.2e} C, a = {a} m (plano xy, centro na origem)")
    print("=" * 65)

    erros = []
    for (x, y, z) in pontos:
        V_ref = potencial_anel_referencia(Q, a, x, y, z)
        erros_ponto = []
        print(f"\nPonto P = ({x}, {y}, {z})")
        print(f"  Referência (N=100000): V = {V_ref:.6e} V")
        for N in N_vals:
            V_comp = potencial_anel_computacional(Q, a, N, x, y, z)
            erro = abs(V_comp - V_ref) / abs(V_ref) * 100
            erros_ponto.append(erro)
            print(f"  N = {N:3d}              : V = {V_comp:.6e} V  |  erro = {erro:.4f}%")
        erros.append(erros_ponto)

    #Visualização L
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(
        f"Questão 2 – Anel de Carga  (Q = {Q:.1e} C, a = {a} m)",
        fontsize=13, fontweight='bold'
    )

    # Gráfico 1: V(z) no eixo
    z_ax = np.linspace(0.2, 8.0, 400)
    ax1.plot(z_ax, potencial_anel_eixo(Q, a, z_ax),
             'k-', linewidth=2.5, label='Analítico (forma fechada)', zorder=5)
    for N, ls, cor in zip(N_vals, estilos_linha, cores):
        V_comp_ax = np.array([potencial_anel_computacional(Q, a, N, 0, 0, z)
                              for z in z_ax])
        ax1.plot(z_ax, V_comp_ax, ls, color=cor, linewidth=1.8, label=f'N = {N}')
    ax1.set_xlabel("z (m)  [x = y = 0]", fontsize=11)
    ax1.set_ylabel("V (V)", fontsize=11)
    ax1.set_title("Perfil de potencial V(z) no eixo do anel", fontsize=11)
    ax1.legend(fontsize=9)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Gráfico 2: convergência
    PISO = 1e-12
    for i, (x, y, z) in enumerate(pontos):
        erros_plot = [max(e, PISO) for e in erros[i]]
        label = f"P = ({x}, {y}, {z})"
        ax2.plot(N_vals, erros_plot,
                 marker=marcadores[i], color=cores[i],
                 linewidth=2, markersize=7, label=label)
    ax2.axhline(PISO, color='gray', linestyle=':', linewidth=1,
                label='Piso numérico (≈ 0)')
    ax2.set_xlabel("N  (número de cargas pontuais)", fontsize=11)
    ax2.set_ylabel("Erro relativo (%)", fontsize=11)
    ax2.set_title("Convergência: erro relativo vs. N", fontsize=11)
    ax2.set_xticks(N_vals)
    ax2.set_yscale('log')
    ax2.legend(fontsize=9)
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig("questao2_anel.png", dpi=150, bbox_inches='tight')
    print("\nGráfico salvo em questao2_anel.png")
    plt.show()


if __name__ == "__main__":
    main()