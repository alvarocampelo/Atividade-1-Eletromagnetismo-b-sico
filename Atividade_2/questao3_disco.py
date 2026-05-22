import numpy as np
import matplotlib.pyplot as plt

k = 8.9875517923e9


def potencial_disco_analitico(Q, a, z):
    sigma = Q / (np.pi * a**2)
    eps0 = 1 / (4 * np.pi * k)
    return (sigma / (2 * eps0)) * (np.sqrt(a**2 + z**2) - abs(z))


def potencial_disco_computacional(Q, a, N, z):
    i_vals = np.arange(1, N + 1)
    r_i = a * np.sqrt((i_vals - 0.5) / N)
    dists = np.sqrt(r_i**2 + z**2)
    return np.sum(k * (Q / N) / dists)


def main():
    Q = 1e-6
    valores_a = [0.5, 2.0]
    z_vals = [1.0, 3.0]
    N_vals = [10, 50, 100]
    cores_a = ['royalblue', 'crimson']
    estilos_linha = ['--', '-.', ':']
    marcadores = ['o', 's', 'D', '^']

    print("=" * 65)
    print(f"Disco de carga: Q = {Q:.2e} C (plano xy, centro na origem)")
    print("Potencial avaliado no eixo z")
    print("=" * 65)

    casos = [(a, z) for a in valores_a for z in z_vals]
    erros = []
    for a, z in casos:
        V_an = potencial_disco_analitico(Q, a, z)
        erros_caso = []
        print(f"\na = {a} m, z = {z} m")
        print(f"  Analítico: V = {V_an:.6e} V")
        for N in N_vals:
            V_comp = potencial_disco_computacional(Q, a, N, z)
            erro = abs(V_comp - V_an) / abs(V_an) * 100
            erros_caso.append(erro)
            print(f"  N = {N:3d}    : V = {V_comp:.6e} V  |  erro = {erro:.4f}%")
        erros.append(erros_caso)

    #Visualização
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(
        f"Questão 3 – Disco Uniforme de Cargas  (Q = {Q:.1e} C)",
        fontsize=13, fontweight='bold'
    )

    # Gráfico 1: V(z) para ambos os raios
    z_plot = np.linspace(0.1, 6.0, 400)
    for j, a in enumerate(valores_a):
        cor = cores_a[j]
        V_an_z = np.array([potencial_disco_analitico(Q, a, z) for z in z_plot])
        ax1.plot(z_plot, V_an_z, color=cor, linewidth=2.5,
                 label=f'Analítico (a = {a} m)', zorder=5)
        for N, ls in zip(N_vals, estilos_linha):
            V_comp_z = np.array([potencial_disco_computacional(Q, a, N, z)
                                 for z in z_plot])
            ax1.plot(z_plot, V_comp_z, ls, color=cor, linewidth=1.4,
                     alpha=0.75, label=f'N = {N}  (a = {a} m)')
    ax1.set_xlabel("z (m)", fontsize=11)
    ax1.set_ylabel("V (V)", fontsize=11)
    ax1.set_title("Perfil de potencial V(z) no eixo do disco", fontsize=11)
    ax1.legend(fontsize=7.5, ncol=2)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Gráfico 2: convergência
    rotulos = [f"a = {a} m,  z = {z} m" for a, z in casos]
    for i, (rotulo, marcador) in enumerate(zip(rotulos, marcadores)):
        ax2.plot(N_vals, erros[i],
                 marker=marcador, linewidth=2, markersize=7, label=rotulo)
    ax2.set_xlabel("N  (número de anéis de área igual)", fontsize=11)
    ax2.set_ylabel("Erro relativo (%)", fontsize=11)
    ax2.set_title("Convergência: erro relativo vs. N", fontsize=11)
    ax2.set_xticks(N_vals)
    ax2.set_yscale('log')
    ax2.legend(fontsize=9)
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig("questao3_disco.png", dpi=150, bbox_inches='tight')
    print("\nGráfico salvo em questao3_disco.png")
    plt.show()


if __name__ == "__main__":
    main()