import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

k = 8.9875517923e9


def potencial_placa_analitico(Q, L, z):
    sigma = Q / L**2
    eps0 = 1 / (4 * np.pi * k)

    def integrando(y, x):
        return sigma / (4 * np.pi * eps0 * np.sqrt(x**2 + y**2 + z**2))

    V, _ = integrate.dblquad(
        integrando, -L/2, L/2, -L/2, L/2,
        epsabs=1e-8, epsrel=1e-8
    )
    return V


def potencial_placa_computacional(Q, L, N, x_p, y_p, z_p):
    sigma = Q / L**2
    dq = sigma * (L / N)**2
    xs = np.linspace(-L/2 + L/(2*N), L/2 - L/(2*N), N)
    XX, YY = np.meshgrid(xs, xs)
    dist = np.sqrt((XX - x_p)**2 + (YY - y_p)**2 + z_p**2)
    return np.sum(k * dq / dist)


def mapa_potencial_placa(Q, L, N, x_range, z_range):
    """
    Calcula V(x, 0, z) para grades 1D de x e z usando broadcasting numpy.
    Retorna array 2D de forma (len(z_range), len(x_range)).
    """
    sigma = Q / L**2
    dq = sigma * (L / N)**2
    xs = np.linspace(-L/2 + L/(2*N), L/2 - L/(2*N), N)
    XX_src, YY_src = np.meshgrid(xs, xs)
    X_src = XX_src.ravel()
    Y_src = YY_src.ravel()

    X_eval = x_range[np.newaxis, :, np.newaxis]
    Z_eval = z_range[:, np.newaxis, np.newaxis]
    dist = np.sqrt((X_src - X_eval)**2 + Y_src**2 + Z_eval**2)
    return np.sum(k * dq / dist, axis=2)


def main():
    Q = 1e-6
    L = 2.0
    z_vals = [0.5, 1.0, 3.0]
    N_vals = [10, 50, 100]
    cores = ['tab:blue', 'tab:orange', 'tab:green']
    marcadores = ['o', 's', '^']
    estilos_linha = ['--', '-.', ':']

    print("=" * 65)
    print(f"Placa quadrada: Q = {Q:.2e} C, L = {L} m (plano xy, centro na origem)")
    print("Potencial avaliado no eixo z")
    print("=" * 65)

    erros = []
    for z in z_vals:
        V_an = potencial_placa_analitico(Q, L, z)
        erros_z = []
        print(f"\nz = {z} m")
        print(f"  Analítico (quad. dupla): V = {V_an:.6e} V")
        for N in N_vals:
            V_comp = potencial_placa_computacional(Q, L, N, 0, 0, z)
            erro = abs(V_comp - V_an) / abs(V_an) * 100
            erros_z.append(erro)
            print(f"  N = {N:3d} (grade N²)    : V = {V_comp:.6e} V  |  erro = {erro:.4f}%")
        erros.append(erros_z)

    #Visualização
    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    fig.suptitle(
        f"Questão 4 – Placa Quadrada  (Q = {Q:.1e} C, L = {L} m)",
        fontsize=13, fontweight='bold'
    )

    # Gráfico 1: V(z) no eixo
    ax1 = axes[0]
    z_plot = np.linspace(0.3, 5.0, 30)
    print("\nComputando perfil V(z) analítico para o gráfico (aguarde)...")
    V_an_plot = np.array([potencial_placa_analitico(Q, L, z) for z in z_plot])
    ax1.plot(z_plot, V_an_plot, 'k-o', linewidth=2.5, markersize=4,
             label='Analítico (dblquad)', zorder=5)
    for N, ls, cor in zip(N_vals, estilos_linha, cores):
        V_comp_plot = np.array([potencial_placa_computacional(Q, L, N, 0, 0, z)
                                for z in z_plot])
        ax1.plot(z_plot, V_comp_plot, ls, color=cor, linewidth=1.8, label=f'N = {N}')
    ax1.set_xlabel("z (m)", fontsize=11)
    ax1.set_ylabel("V (V)", fontsize=11)
    ax1.set_title("Perfil de potencial V(z) no eixo z", fontsize=11)
    ax1.legend(fontsize=9)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Gráfico 2: convergência
    ax2 = axes[1]
    for i, (z, marcador, cor) in enumerate(zip(z_vals, marcadores, cores)):
        ax2.plot(N_vals, erros[i],
                 marker=marcador, color=cor,
                 linewidth=2, markersize=7, label=f"z = {z} m")
    ax2.set_xlabel("N  (grade N × N de cargas)", fontsize=11)
    ax2.set_ylabel("Erro relativo (%)", fontsize=11)
    ax2.set_title("Convergência: erro relativo vs. N", fontsize=11)
    ax2.set_xticks(N_vals)
    ax2.set_yscale('log')
    ax2.legend(fontsize=9)
    ax2.grid(True, linestyle='--', alpha=0.5)

    # Gráfico 3: mapa de potencial V(x, 0, z)
    ax3 = axes[2]
    N_mapa = 50
    x_range = np.linspace(-2.5, 2.5, 80)
    z_range = np.linspace(0.15, 4.5, 80)
    print(f"Computando mapa V(x, 0, z) com N = {N_mapa} (broadcasting)...")
    V_mapa = mapa_potencial_placa(Q, L, N_mapa, x_range, z_range)

    cf = ax3.contourf(x_range, z_range, V_mapa, levels=25, cmap='plasma')
    ax3.contour(x_range, z_range, V_mapa, levels=25,
                colors='white', linewidths=0.4, alpha=0.35)
    fig.colorbar(cf, ax=ax3, label='V (V)')

    ax3.plot([-L/2, L/2], [0, 0], color='cyan', linewidth=3,
             solid_capstyle='round', label=f'Placa  |x| ≤ {L/2} m')
    ax3.axvline(-L/2, color='cyan', linewidth=1, linestyle='--', alpha=0.6)
    ax3.axvline( L/2, color='cyan', linewidth=1, linestyle='--', alpha=0.6)
    ax3.set_xlabel("x (m)  [y = 0]", fontsize=11)
    ax3.set_ylabel("z (m)", fontsize=11)
    ax3.set_title(f"Mapa de potencial V(x, 0, z)  (N = {N_mapa})", fontsize=11)
    ax3.legend(fontsize=8, loc='upper right')

    plt.tight_layout()
    plt.savefig("questao4_placa.png", dpi=150, bbox_inches='tight')
    print("\nGráfico salvo em questao4_placa.png")
    plt.show()


if __name__ == "__main__":
    main()