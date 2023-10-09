#!/usr/bin/env python3
import matplotlib.pyplot as plt

input = {
    'mode': 'ideal',  # käytetään ideaalikaasua
    'gas': 'O2',      # happikaasu
    'temp': 270,      # lämpötila kelvineinä
    'mass': 12,       # massa grammoina
}

data = {
    'O2': {'molar_mass': 31.999}, # g/mol
    'H2': {'molar_mass': 2.016, 'a': 0.0245, 'b': 0.00002661}, # g/mol, Pa m⁶, m³/mol
    'CO2': {'molar mass': 44.01, 'a': 3.592, 'b': 0.04267} # g/mol, L² atm / mol², L/mol
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

def ideal_pressure(n, T, V):
    """
    Laskee kaasun paineen ideaalikaasun tilanyhtälön avulla.

    Parameters
    ----------
    n : float
        Kaasun ainemäärä mooleina
    T : float
        Kaasun lämpötila kelvineinä
    V : float
        Kaasun tilavuus kuutiometreinä
    """
    R = 8.3135 # J/mol*K, ideaalikaasulain kaasuvakio
    return (n * R * T) / V

def vdw_pressure(n, T, V, a, b):
    """
    Laskee kaasun paineen van der Waals -tilanyhtälön avulla.

    Parameters
    ----------
    n : float
        Kaasun ainemäärä mooleina
    T : float
        Kaasun lämpötila kelvineinä
    V : float
        Kaasun tilavuus litroina
    a : float
        van der Waals -tilanyhtälön vakio a yksikössä L^2 * atm / mol^2
    b : float
        van der Waals -tilanyhtälön vakio b yksikössä L/mol

    Return
    ------
    Palauttaa van der Waals -tilanyhtälön avulla lasketun paineen yksikössä atm

    """
    R = 0.0820574 # L*atm / mol*K

    second_term = V/n-b
    to_substract = a*(n/V)**2

    return (R*T)/second_term - to_substract

def test_oxygen():
    """
    Testifunktio hapelle ideaalikaasumallilla.

    40 l, 1 kg happikaasua pitäisi antaa 19,1 atm paineen.
    """
    m = 1000
    V = 0.040
    M = data['O2']['molar_mass']
    T = 298
    n = calculate_n(m, M)
    print(ideal_pressure(n, T, V) / 101325)

def test_carbondioxide():
    """
    Testifunktio hiilidioksidille. V = 22,4 l, T = 0 C, n = 1 mol

    Ideaalikaasun pitäisi antaa 1 atm
    vdw-kaasun pitäisi antaa 0.995 atm
    """
    n = 1
    T = 273
    V = 0.0224
    a = data['CO2']['a']
    b = data['CO2']['b']
    p_ideal = ideal_pressure(n, T, V)
    p_vdw = vdw_pressure(n, T , 22.4, a, b)
    print(f'Ideal gas: {p_ideal}, vdw: {p_vdw}')

if __name__ == '__main__':
    # test_oxygen()
    test_carbondioxide()
    # Lasketaan 200 g 290 K vetykaasun paine eri tilavuuksilla
    # m = 50
    # V = [i/1000 for i in range(1, 10)]
    # p_ideal = []
    # p_vdw = []
    # M = data['H2']['molar_mass']
    # a = data['H2']['a']
    # b = data['H2']['b']
    # n = calculate_n(m, M)
    # T = 350
    # for v in V:
    #     p_ideal.append(ideal_pressure(n, T, v))
    #     p_vdw.append(vdw_pressure(n, T, v, a, b))

    # for i in range(len(V)):
    #     print(V[i], p_ideal[i], p_vdw[i])

    # plt.xlabel('volume')
    # plt.ylabel('pressure')
    # plt.plot(V, p_ideal, '.')
    # plt.plot(V, p_vdw, 'x')
    # plt.show()