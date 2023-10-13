#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

input = {
    'mode': 'ideal',  # käytetään ideaalikaasua
    'gas': 'O2',      # happikaasu
    'temp': 270,      # lämpötila kelvineinä
    'mass': 12,       # massa grammoina
}

data = {
    'O2': {'molar_mass': 31.999, 'a': 1.36, 'b': 0.0319}, # g/mol, L^2 * atm / mol^2, L/mol
    'H2': {'molar_mass': 2.016, 'a': 0.242, 'b': 0.0265}, # g/mol, L^2 * atm / mol^2, L/mol
    'CO2': {'molar mass': 44.01, 'a': 3.592, 'b': 0.04267} # g/mol, L^2 * atm / mol^2, L/mol
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

class Ideal:
    def __init__(self, n, T, p=None, V=None):
        """
        Parameters
        ----------
        n : float
            Kaasun ainemäärä mooleina
        T : float
            Kaasun lämpötila kelvineinä
        p : float
            Kaasun paine ilmakehän paineena (atm)
        V : float
            Kaasun tilavuus litroina
        """

        self.n = n
        self.T = T
        self.p = p
        self.V = V
        self.R = 0.0820574 # L*atm / mol*K

    def pressure(self):
        """
        Laskee kaasun paineen ideaalikaasun tilanyhtälön avulla.

        Return
        ------
        Palauttaa ideaalikaasumallin mukaisen paineen yksikössä atm.

        """
        self.p = (self.n * self.R * self.T) / self.V
        return self.p
    

    def volume(self):
        """
        Laskee kaasun tilavuuden ideaalikaasun tilanyhtälön avulla.


        Return
        ------
        Palauttaa ideaalikaasumallin mukaisen tilavuuden litroina.

        """
        self.V = (self.n * self.R * self.T) / self.p
        return self.V

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

def vdw_volume(n, T, P, a, b):
    """
    Laskee kaasun tilavuuden van der Waals -tilanyhtälön avulla.

    Parameters
    ----------
    n : float
        Kaasun ainemäärä mooleina
    T : float
        Kaasun lämpötila kelvineinä
    P : float
        Kaasun paine yksikössä atm
    a : float
        van der Waals -tilanyhtälön vakio a yksikössä L^2 * atm / mol^2
    b : float
        van der Waals -tilanyhtälön vakio b yksikössä L/mol

    Return
    ------
    Palauttaa van der Waals -tilanyhtälön avulla lasketun kaasun tilavuuden litroina

    """
    R = 0.0820574 # L*atm / mol*K
    func = lambda V : (p + a*n**2/V**2) * (V - n*b) - n*R*T
    test_value = 1

    print(func(test_value))
    print(fsolve(func, test_value))


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
    V = 22.4
    a = data['CO2']['a']
    b = data['CO2']['b']
    p_ideal = ideal_pressure(n, T, V)
    p_vdw = vdw_pressure(n, T , V, a, b)
    print(f'Ideal gas: {p_ideal}, vdw: {p_vdw}')

if __name__ == '__main__':
    n = 1.00
    T = 273
    p = 4

    a = data['O2']['a']
    b = data['O2']['b']

    ideal_gas = Ideal(n, T, p)
    print(ideal_gas.volume())
    print(ideal_gas.pressure())
