"""
problema_09.py
--------------
Problema 9 da Lista 2 – TI0166
Carga total em distribuições de diferentes geometrias.

(a) Linha: 0 < x < 5 m, ρ_L = 12x² mC/m
(b) Cilindro: ρ = 3 m, 0 < z < 4 m, ρ_s = z² nC/m²
(c) Esfera: r = 4 m, ρ_v = 10/(r·sinθ) C/m³

Disciplina: Eletromagnetismo Básico – TI0166 | Prof. João Batista | UFC
"""

import numpy as np
from scipy import integrate


def main():
    print("=" * 55)
    print("Problema 9 – Cargas Totais")
    print("=" * 55)

    # ------------------------------------------------------------------ #
    # (a) Carga linear                                                     #
    # Qa = ∫₀⁵ 12x² × 10⁻³ dx                                            #
    # ------------------------------------------------------------------ #
    Qa, err_a = integrate.quad(lambda x: 12e-3 * x**2, 0, 5)
    print(f"(a) Carga linear:")
    print(f"    Qa = {Qa:.4f} C  (analítico: 0.5 C)  | erro num. = {err_a:.2e}")

    # ------------------------------------------------------------------ #
    # (b) Carga superficial cilíndrica (ρ = 3 m)                          #
    # Qb = ∫₀²π dφ ∫₀⁴ z²·10⁻⁹·3 dz                                     #
    # ------------------------------------------------------------------ #
    rho_cil = 3.0
    Qb, err_b = integrate.dblquad(
        lambda z, phi: z**2 * 1e-9 * rho_cil,
        0, 2 * np.pi,
        0, 4
    )
    print(f"\n(b) Carga superficial cilíndrica:")
    print(f"    Qb = {Qb * 1e9:.4f} nC  (~{Qb * 1e9 / np.pi:.4f}·π nC)")
    print(f"    Analítico: 128·π = {128 * np.pi:.4f} nC  | erro num. = {err_b:.2e}")

    # ------------------------------------------------------------------ #
    # (c) Carga volumétrica esférica                                       #
    # ρ_v = 10/(r·sinθ); após multiplicar por dV = r²·sinθ dr dθ dφ,     #
    # o fator sinθ cancela → integrando simplificado = 10·r               #
    # ------------------------------------------------------------------ #
    eps = 1e-9  # evitar singularidade nos polos θ = 0 e θ = π

    Qc, err_c = integrate.tplquad(
        lambda phi, theta, r: 10 * r,   # integrando simplificado
        0, 4,                            # r de 0 a 4 m
        lambda r: eps,
        lambda r: np.pi - eps,           # θ (evitar singularidade nos polos)
        lambda r, t: 0,
        lambda r, t: 2 * np.pi          # φ de 0 a 2π
    )
    print(f"\n(c) Carga volumétrica esférica:")
    print(f"    Qc = {Qc:.4f} C  (~{Qc / np.pi**2:.4f}·π² C)")
    print(f"    Analítico: 160·π² = {160 * np.pi**2:.4f} C  | erro num. = {err_c:.2e}")


if __name__ == "__main__":
    main()
