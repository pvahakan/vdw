#!/usr/bin/env python3
import matplotlib.pyplot as plt

input = {
    'mode': 'ideal',  # käytetään ideaalikaasua
    'gas': 'O2',      # happikaasu
    'temp': 270,      # lämpötila kelvineinä
    'mass': 12,       # massa grammoina
    'ideal_R': 8.3135 # J/mol*K, ideaalikaasulain kaasuvakio
}

data = {
    'O2': {'molar_mass': 31.999} # g/mol
}

def calculate_n(m, M):
    """
    Laskee kaasun ainemäärän mooleina.

    Parameters
    ----------
    m : float
        Kaasun massa grammoina
    M : float
        Kaasun moolimassa, g/mol
    """
    return m/M

def ideal_pressure(n, R, T, V):
    """
    Laskee kaasun paineen ideaalikaasun tilanyhtälön avulla.

    Parameters
    ----------
    n : float
        Kaasun ainemäärä mooleina
    R : float
        Kaasuvakio
    T : float
        Kaasun lämpötila kelvineinä
    V : float
        Kaasun tilavuus kuutiometreinä
    """
    return (n * R * T) / V


if __name__ == '__main__':
    # Lasketaan 12 g 290 K happikaasun paine, kun tilavuus on 5 l
    m = 12
    V = [i/1000 for i in range(1, 10)]
    p = []
    M = data['O2']['molar_mass']
    R = input['ideal_R']
    n = calculate_n(m, M)
    T = 290
    for v in V:
        p.append(ideal_pressure(n, R, T, v))

    for i in range(len(V)):
        print(V[i], p[i])

    plt.plot(V, p, '.')
    plt.show()