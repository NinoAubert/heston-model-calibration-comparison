import numpy as np
import heston_model # Importer le module contenant les classes
from heston_model import BSModel, HestonModel

# --- DONNÉES D'ENTRÉE ---

# Données de marché
S0 = 6627.88
K = 6630.00
T = 0.25      # Maturité en années (3 mois)
r = 0.03864   # Taux sans risque
C_obs = 295.00 # Prix observé sur le marché
vol_implicite_bs = 0.2104 # Volatilité pour le pricing BS

# Paramètres Heston [v0, kappa, theta, sigma_v, rho]
heston_params = [0.035, 2.5, 0.03, 0.4, -0.7]

# --- FONCTION PRINCIPALE D'EXÉCUTION ---

def run_valuation():
    print("--- 📊 VALORISATION COMPARATIVE HESTON vs BLACK-SCHOLES ---")
    print(f"Option Call: S0={S0:.2f}, K={K:.2f}, T={T:.2f}, C_obs={C_obs:.2f}\n")

    # 1. Valorisation Black-Scholes
    bs = BSModel(S0, K, T, r)
    price_bs = bs.black_scholes_value(vol_implicite_bs, 'call')
    
    # 2. Valorisation Heston
    heston = HestonModel(S0, K, T, r, heston_params)
    price_heston = heston.Heston_Call_Value()

    # --- AFFICHAGE DES RÉSULTATS ---
    
    results = {
        "C_obs": C_obs,
        "BS_price": price_bs,
        "BS_error": price_bs - C_obs,
        "Heston_price": price_heston,
        "Heston_error": price_heston - C_obs
    }

    print("--- RÉSULTATS FINAUX ---")
    print(f"Prix Observé (Cobs) : {results['C_obs']:.3f}")
    
    print("\n--- Modèle BLACK-SCHOLES ---")
    print(f"Prix calculé : {results['BS_price']:.3f}")
    print(f"Erreur simple : {results['BS_error']:.3f}")

    print("\n--- Modèle HESTON ---")
    if np.isnan(results['Heston_price']):
        print("Prix calculé : ÉCHEC DE CONVERGENCE")
    else:
        print(f"Prix calculé : {results['Heston_price']:.3f}")
        print(f"Erreur simple : {results['Heston_error']:.3f}")
    
    return results

# Exécuter l'analyse
if __name__ == "__main__":
    run_valuation()
