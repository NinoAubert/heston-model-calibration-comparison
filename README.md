# Analyse Comparative de la Valorisation d'Options (Black-Scholes vs. Heston)

Ce dépôt contient le code et l'analyse des résultats d'une étude de valorisation comparative entre le modèle standard de Black-Scholes (BS) et le modèle à volatilité stochastique de Heston (SQRV).

L'étude vise à démontrer la capacité du modèle de Heston à mieux s'ajuster à la **surface de volatilité** des options sur indices boursiers, en tenant compte de l'effet de levier et du "skew" (asymétrie) de volatilité.

## Contexte de la Valorisation

Les calculs sont effectués pour une option Call européenne sur indice S&P 500.

| Paramètre | Symbole | Valeur | Unité |
| :--- | :--- | :--- | :--- |
| **Sous-jacent initial** | $S_0$ | $6627.88$ | Points |
| **Strike** | $K$ | $6630.00$ | Points |
| **Maturité** | $T$ | $0.25$ | Années (3 mois) |
| **Taux sans risque** | $r$ | $0.03864$ | % |
| **Prix Observé** | $C_{obs}$ | $295.00$ | Points |

### Paramètres du Modèle de Heston (SQRV)

Ces paramètres ont été calibrés sur l'ensemble de la surface de volatilité.

| Paramètre | Description | Valeur |
| :--- | :--- | :--- |
| **Volatilité initiale** | $v_0$ | $0.035$ |
| **Vitesse de retour à la moyenne** | $\kappa$ | $2.5$ |
| **Variance à long terme** | $\theta$ | $0.03$ |
| **Volatilité de la variance** | $\sigma_v$ | $0.4$ |
| **Corrélation St/Vt** | $\rho$ | $-0.7$ |

## Résultats de la Valorisation

L'exécution du script `main_pricing.py` (basé sur l'implémentation Heston 1993 et l'intégration par `spi.quad`) donne les résultats suivants pour l'option test :

| Modèle | Prix Théorique ($C_{model}$) | Écart vs Prix Observé ($C_{model} - C_{obs}$) |
| :--- | :--- | :--- |
| **Black-Scholes** | **308.641** | $+13.641$ |
| **Heston** | **268.527** | $-26.473$ |

### Interprétation des Écarts

1.  **Black-Scholes (BS) :** Le modèle surévalue l'option de **+13.64** points. L'erreur est positive.
2.  **Heston :** Le modèle sous-évalue l'option de **-26.47** points. L'erreur est négative et plus grande en valeur absolue que celle de BS pour cette option spécifique.

**Conclusion :** Bien que l'erreur individuelle soit plus faible pour Black-Scholes sur cette option *At-The-Money* (ATM), **l'avantage du modèle de Heston réside dans sa performance globale (RMSE) sur l'ensemble de la surface de volatilité**. Le paramètre $\rho = -0.7$ permet à Heston de mieux tarifer le risque de krach (Skew), ce qui n'est pas reflété dans la valorisation d'une seule option ATM.

## Instructions pour l'Exécution

Pour exécuter le modèle et reproduire les résultats :

1.  Cloner le dépôt :
    ```bash
    git clone [https://github.com/NinoAubert/heston-model-calibration-comparison.git](https://github.com/votre-nom-utilisateur/heston-model-calibration-comparison.git)
    cd heston-model-calibration-comparison
    ```
2.  Installer les dépendances requises (principalement `numpy` et `scipy`) :
    ```bash
    pip install numpy scipy
    ```
3.  Exécuter le script principal :
    ```bash
    python src/main_pricing.py
    ```
