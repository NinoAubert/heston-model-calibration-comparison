import numpy as np
import scipy.integrate as spi
from scipy.stats import norm
import cmath

# --- CLASSE BLACK-SCHOLES (BS) ---

class BSModel:
    """
    Modèle Black-Scholes pour la valorisation d'options Call/Put.
    """
    def __init__(self, S, K, T, r):
        self.S = S
        self.K = K
        self.T = T
        self.r = r

    def black_scholes_value(self, vol, type_flag='call'):
        """ Calcule le prix du Call ou du Put selon BS. """
        d1 = (1.0 / (vol * np.sqrt(self.T))) * (np.log(self.S / self.K) + (self.r + 0.5 * vol**2.0) * self.T)
        d2 = d1 - (vol * np.sqrt(self.T))
       
        if type_flag == 'call':
            return norm.cdf(d1) * self.S - norm.cdf(d2) * self.K * np.exp(-self.r * self.T)
        elif type_flag == 'put':
            return norm.cdf(-d2) * self.K * np.exp(-self.r * self.T) - norm.cdf(-d1) * self.S
        return 0.0

# --- CLASSE HESTON ---

class HestonModel:
    """
    Modèle de Heston pour la valorisation d'options Call (Formulation Heston 1993).
    """
    def __init__(self, S0, K, T, r, parms):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        # parms = [v0, kappa, theta, sigma_v, rho]
        self.parms = parms 

    def characteristic_function(self, phi, type_flag):
        """ Calcule la fonction caractéristique phi_j (j=1 ou j=2). """
        v0, kappa, theta, sigma, rho = self.parms
        
        # Définition des paramètres u et b selon P1 (type_flag=1) ou P2 (type_flag=2)
        if type_flag == 1:
            u = 0.5
            b = kappa - rho * sigma
        else: 
            u = -0.5
            b = kappa
        
        a = kappa * theta
        x = np.log(self.S0)
        
        # Note: cmath est crucial pour les fonctions sqrt et log dans le domaine complexe
        d = cmath.sqrt((rho * sigma * phi * 1j - b)**2 - sigma**2 * (2 * u * phi * 1j - phi**2))
        g = (b - rho * sigma * phi * 1j + d) / (b - rho * sigma * phi * 1j - d)
        
        # Termes C et D (formulation Heston 93)
        D_term = self.r * phi * 1j * self.T + (a / sigma**2) * ((b - rho * sigma * phi * 1j + d) * self.T - 2 * cmath.log((1 - g * cmath.exp(d * self.T)) / (1 - g)))
        E_term = ((b - rho * sigma * phi * 1j + d) / sigma**2) * (1 - cmath.exp(d * self.T)) / (1 - g * cmath.exp(d * self.T))
        
        return cmath.exp(D_term + E_term * v0 + 1j * phi * x)

    def integral_function(self, phi, type_flag):
        """ Intégrand pour la formule de Gil-Pelaez (partie réelle). """
        # La fonction caractéristique doit être convertie de cmath à numpy (géré par le wrapper spi.quad)
        numerator = cmath.exp(-1j * phi * cmath.log(self.K)) * self.characteristic_function(phi, type_flag)
        return (numerator / (1j * phi)).real

    def Heston_P_Value(self, type_flag):
        """ Calcule la probabilité P1 ou P2 par intégration. """
        # Intégration de 1e-8 à 100
        # On utilise une fonction lambda pour adapter la signature de l'intégrand à spi.quad
        ifun = lambda phi: self.integral_function(phi, type_flag)
        
        # Le second élément de spi.quad est l'estimation de l'erreur, on ne prend que le résultat [0]
        try:
            result = spi.quad(ifun, 1e-8, 100, limit=100)[0] 
        except Exception:
            # En cas d'erreur de convergence (instabilité), on retourne 0 ou on lève une exception claire
            print(f"ATTENTION: Échec de la convergence pour P{type_flag} (Heston)")
            return np.nan

        return 0.5 + (1 / np.pi) * result

    def Heston_Call_Value(self):
        """ Calcule le prix final du Call. """
        P1 = self.Heston_P_Value(1)
        P2 = self.Heston_P_Value(2)
        
        if np.isnan(P1) or np.isnan(P2):
            return np.nan

        call_price = self.S0 * P1 - self.K * np.exp(-self.r * self.T) * P2
        
        # Petite vérification de stabilité
        if call_price < 0:
             print("AVERTISSEMENT: Prix Heston négatif (instabilité).")
        return call_price
