"""
problema_06.py
--------------
Problema 6 da Lista 2 – TI0166
Carga total em região com densidade volumétrica de carga em coordenadas esféricas.

Região: 4 < r < 5 m, 0 < θ < 25°, 0.9π < φ < 1.1π
Densidade: ρ_v = 10(r−4)(r−5)·sinθ·sin(φ/2)

Disciplina: Eletromagnetismo Básico – TI0166 | Prof. João Batista | UFC
"""

import numpy as np
from scipy import integrate


def rho_v(r, theta, phi):
    """Densidade volumétrica de carga [C/m³]."""
    return 10 * (r - 4) * (r - 5) * np.sin(theta) * np.sin(phi / 2)


def integrand(phi, theta, r):
    """Integrando completo: ρ_v · dV = ρ_v · r² · sinθ."""
    return rho_v(r, theta, phi) * r**2 * np.sin(theta)


def main():
    # ------------------------------------------------------------------ #
    # Limites de integração                                                #
    # ------------------------------------------------------------------ #
    r_lim     = (4, 5)
    theta_lim = (0, 25 * np.pi / 180)
    phi_lim   = (0.9 * np.pi, 1.1 * np.pi)

    # ------------------------------------------------------------------ #
    # Integração numérica tripla                                           #
    # ------------------------------------------------------------------ #
    Q, erro = integrate.tplquad(
        integrand,
        r_lim[0], r_lim[1],
        lambda r: theta_lim[0],
        lambda r: theta_lim[1],
        lambda r, t: phi_lim[0],
        lambda r, t: phi_lim[1]
    )

    print("=" * 55)
    print("Problema 6 – Carga Total (Integração Numérica)")
    print("=" * 55)
    print(f"Q     = {Q:.4f} C")
    print(f"Erro estimado = {erro:.2e} C")

    # ------------------------------------------------------------------ #
    # Verificação por fatoração das integrais                              #
    # ------------------------------------------------------------------ #
    Ir, _ = integrate.quad(
        lambda r: 10 * (r - 4) * (r - 5) * r**2, 4, 5
    )
    It, _ = integrate.quad(
        lambda t: np.sin(t)**2, 0, 25 * np.pi / 180
    )
    Ip, _ = integrate.quad(
        lambda p: np.sin(p / 2), 0.9 * np.pi, 1.1 * np.pi
    )

    print()
    print("Verificação por fatoração das integrais separadas:")
    print(f"  I_r = {Ir:.4f}")
    print(f"  I_θ = {It:.5f}")
    print(f"  I_φ = {Ip:.4f}")
    print(f"  Q = I_r · I_θ · I_φ = {Ir * It * Ip:.4f} C")


if __name__ == "__main__":
    main()
