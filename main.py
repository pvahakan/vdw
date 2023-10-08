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
    'O2': {'molar_mass': 31.999}, # g/mol
    'H2': {'molar_mass': 2.016, 'a': 0.0245, 'b': 0.00002661} # g/mol, Pa m⁶, m³/mol
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

def vdw_pressure(n, R, T, V, a, b):
    """
    Laskee kaasun paineen van der Waals -tilanyhtälön avulla.
    """
    print('!!! !!! !!!')
    print('Tarkista vakioiden a ja b yksiköt, meneehän kaikki oikein!!!')
    print('!!! !!! !!!')
    second_term = V/n-b
    to_substract = a*(n/V)**2
    return (R*T)/second_term - to_substract


if __name__ == '__main__':
    # Lasketaan 12 g 290 K vetykaasun paine eri tilavuuksilla
    m = 12
    V = [i/1000 for i in range(1, 10)]
    p_ideal = []
    p_vdw = []
    M = data['H2']['molar_mass']
    a = data['H2']['a']
    b = data['H2']['b']
    R = input['ideal_R']
    n = calculate_n(m, M)
    T = 290
    for v in V:
        p_ideal.append(ideal_pressure(n, R, T, v))
        p_vdw.append(vdw_pressure(n, R, T, v, a, b))

    for i in range(len(V)):
        print(V[i], p_ideal[i], p_vdw[i])

    plt.xlabel('volume')
    plt.ylabel('pressure')
    plt.plot(V, p_ideal, '.')
    plt.plot(V, p_vdw, 'x')
    plt.show()