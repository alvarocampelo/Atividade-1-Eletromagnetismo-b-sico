"""
Problema 9 da Lista 2
Carga total em distribuições de diferentes geometrias.

(a) Linha: 0 < x < 5 m, ρ_L = 12x² mC/m
(b) Cilindro: ρ = 3 m, 0 < z < 4 m, ρ_s = z² nC/m²
(c) Esfera: r = 4 m, ρ_v = 10/(r·sinθ) C/m³
"""

import numpy as np
from scipy import integrate


def main():
    print("=" * 55)
    print("Problema 9 – Cargas Totais")
    print("=" * 55)

    # (a) Carga linear                                                     

    Qa, err_a = integrate.quad(lambda x: 12e-3 * x**2, 0, 5)
    print(f"(a) Carga linear:")
    print(f"    Qa = {Qa:.4f} C  (analítico: 0.5 C)  | erro num. = {err_a:.2e}")

    # (b) Carga superficial cilíndrica com ρ = 3 m
    rho_cil = 3.0
    Qb, err_b = integrate.dblquad(
        lambda z, phi: z**2 * 1e-9 * rho_cil,
        0, 2 * np.pi,
        0, 4
    )
    print(f"\n(b) Carga superficial cilíndrica:")
    print(f"    Qb = {Qb * 1e9:.4f} nC  (~{Qb * 1e9 / np.pi:.4f}·π nC)")
    print(f"    Analítico: 128·π = {128 * np.pi:.4f} nC  | erro num. = {err_b:.2e}")

    # (c) Carga volumétrica esférica
    eps = 1e-9

    Qc, err_c = integrate.tplquad(
        lambda phi, theta, r: 10 * r,   
        0, 4,                            
        lambda r: eps,
        lambda r: np.pi - eps,         
        lambda r, t: 0,
        lambda r, t: 2 * np.pi 
    )
    print(f"\n(c) Carga volumétrica esférica:")
    print(f"    Qc = {Qc:.4f} C  (~{Qc / np.pi**2:.4f}·π² C)")
    print(f"    Analítico: 160·π² = {160 * np.pi**2:.4f} C  | erro num. = {err_c:.2e}")


if __name__ == "__main__":
    main()
