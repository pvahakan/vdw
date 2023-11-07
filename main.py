#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import csv
from gasmodels import Ideal, VDW

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

class FileHandler:
    def __init__(self, inputfile : str):
        """
        Parameters
        ----------
        inputfile : str
            File path to the inputfile. MUST END WITH .inp with small letters!
        
        """
        self.input = inputfile
        self.output = inputfile.split('.inp')[0] + '.out'

    def __enter__(self):
        self.file = open(self.input)
        self.reader = csv.reader(self.file, delimiter=' ')
        return self

    def __exit__(self, *args):
        self.file.close()

    def read_file(self):
        """
        Reads data from input file and returns gas model as a dictionary.
        """
        calculation = None
        type, gas, temp, pressure, mass, volume = None, None, None, None, None, None
        for row in self.reader:
            row = self.remove_comments(row)
            if 'calculation' in row:
                calculation = self.find_value(row)
            if 'type' in row:
                type = self.find_value(row)
            if 'gas' in row:
                gas = self.find_value(row)
            if 'temp' in row:
                temp = self.find_value(row)
            if 'mass' in row:
                mass = self.find_value(row)
            if 'pressure' in row:
                pressure = self.find_value(row)
                start = pressure.split('-')[0]
                end = pressure.split('-')[-1]
                pressure = np.linspace(float(start), float(end), 20)
            if 'volume' in row:
                volume = self.find_value(row)
                start = volume.split('-')[0]
                end = volume.split('-')[-1]
                volume = np.linspace(float(start), float(end), 20)

        gas_model = {
            'calculation': calculation,
            'type': type,
            'gas': gas,
            'mass': mass,
            'temp': temp,
            'pressure': pressure,
            'volume': volume
        }

        return gas_model

    def remove_comments(self, row):
        if '#' in row:
            comment_index = row.index('#')
            return row[:comment_index]
        return row

    def find_value(self, row):
        return row[row.index(':') + 1]

    def create_model(self):
        pass

class Gas:
    def __init__(self, model: dict):
        self.model = model
        self.type = model['type']
        self.name = self.model['gas']

        self.a = float(data[self.model['gas']]['a'])
        self.b = float(data[self.model['gas']]['b'])
        self.n = float(self.calculate_n())
        try:
            self.V = float(self.model['volume'])
        except Exception as e:
            self.V = None
        try:
            self.p = self.model['pressure']
        except Exception as e:
            self.p = None
        try:
            self.T = float(self.model['temp'])
        except Exception as e:
            print(e)
            

    def __repr__(self):
        rpr = '================\n'
        rpr += f'  {self.name}  \n'
        rpr += f'  {self.type}  \n'
        rpr += '================\n\n'
        return rpr

    def calculate_n(self):
        M = float(data[self.model['gas']]['molar_mass'])
        m = float(self.model['mass'])
        return m/M

# class Model:
#     def __init__(self, gas : Gas):
#         self.gas = gas
#         if self.gas.type == 'ideal':
#             self.model = Ideal(gas.n, gas.T, gas.p, gas.V)
#         if self.gas.type == 'vdw':
#             self.model = VDW(gas.a, gas.b, gas.n, gas.T, gas.p, gas.V)
# 
#     def get_model(self):
#         return self.model


class UserInterface:
    def __init__(self, filehandler: FileHandler):
        self.fh = filehandler
        self.gas_model = self.fh.read_file()
        self.gas = Gas(self.gas_model)
        self.calculation = self.gas_model['calculation']
        self.model = self.create_gas_model()

    def create_gas_model(self):
        if self.gas.type == 'ideal':
            return Ideal(self.gas.n, self.gas.T, self.gas.p, self.gas.V)
        if self.gas.type == 'vdw':
            return VDW(self.gas.a, self.gas.b, self.gas.n, self.gas.T, self.gas.p, self.gas.V)

    def calculate_value(self):
        if self.calculation == 'vol':
            result = self.model.volume()
        if self.calculation == 'pre':
            result = self.model.pressure()

        return result

## Tests
########

def test_oxygen():
    """
    Testifunktio hapelle ideaalikaasumallilla.

    40 l, 1 kg happikaasua pitäisi antaa 19,1 atm paineen.
    """
    m = 1000
    V = 40
    M = data['O2']['molar_mass']
    T = 298
    n = calculate_n(m, M)
    o2 = Ideal(n, T, V=V)
    print('1 kg happikaasua 40 l tilavuudessa pitäisi olla 19,1 atm paineessa')
    print('Laskettu arvo:')
    print(f'Määrä: {m} g, tilavuus: {V} l, paine: {o2.pressure()} atm')

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

    ideal = Ideal(n, T, V=V)
    vdw = VDW(a, b, n, T, V=V)

    print('Testifunktio hiilidioksidille. V = 22,4 l, T = 0 C, n = 1 mol')
    print('Ideaalikaasun pitäisi antaa 1 atm ja vdw-kaasun 0.995 atm')
    print('Lasketut arvot:')
    print(f'Ideal gas: {ideal.pressure()}, vdw: {vdw.pressure()}')

if __name__ == '__main__':

    inputfile = './test_input.inp'
    fh = FileHandler(inputfile)

    with fh:
        ui = UserInterface(fh)
        
    # model = ui.create_gas_model()

    print(ui.calculate_value())









    # with open('./test_input.inp') as file:
    #     reader = csv.reader(file, delimiter=' ')
    #     for row in reader:
    #         if '#' in row:
    #             comment_index = row.index('#')
    #             print(row[:comment_index])



    # n = 1.00
    # T = 273 
    # # p = [i/10 for i in range(1, 100, 5)]
    # p = np.linspace(1, 1000, 50)
    # Vi = np.array([])
    # Vv = np.array([])

    # a = data['H2']['a']
    # b = data['H2']['b']

    # for paine in p:
    #     ideal_gas = Ideal(n, T, paine)
    #     vdw_gas = VDW(a, b, n, T, p=paine)
    #     Vi = np.append(Vi, ideal_gas.volume())
    #     Vv = np.append(Vv, vdw_gas.volume())
    #     
    # plt.plot(p, p*Vi, '.', color='blue', label='ideal')
    # plt.plot(p, p*Vv, '.', color='red', label='van der Waals')
    # plt.legend()
    # plt.title('H2')
    # plt.ylabel('V (l)')
    # plt.xlabel('p (atm)')
    # plt.show()
