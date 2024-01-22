#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
from gasmodels import Ideal, VDW

data = {
    'O2': {'molar_mass': 31.999, 'a': 1.36, 'b': 0.0319}, # g/mol, L^2 * atm / mol^2, L/mol
    'H2': {'molar_mass': 2.016, 'a': 0.242, 'b': 0.0265}, # g/mol, L^2 * atm / mol^2, L/mol
    'CO2': {'molar_mass': 44.01, 'a': 3.592, 'b': 0.04267} # g/mol, L^2 * atm / mol^2, L/mol
}

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
        try:
            self.file = open(self.input)
            self.reader = csv.reader(self.file, delimiter=' ')
            return self
        except FileNotFoundError:
            print('Check that the given input file name is correct.')
            exit()

    def __exit__(self, *args):
        self.file.close()

    def read_file(self):
        """
        Reads data from input file.
         
        Return
        ------ 
        gas_model : dictionary with keys
            'calculation' = which calculation will be executed ex. gas volume = 'vol' and pressure = 'pre'
            'type' = which model type is used, ideal or vdw
            'gas' = which gas is used, for example O2
            'temp' = gas temperature in kelvins
            'mass' = gas mass in grams
            'pressure' = gas pressure in atm, this can be a numpy array
            'volume' = gas volume in l, this can be a numpy array
        """
        number_of_values = 20
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
                pressure = np.linspace(float(start), float(end), number_of_values)
            if 'volume' in row:
                volume = self.find_value(row)
                start = volume.split('-')[0]
                end = volume.split('-')[-1]
                volume = np.linspace(float(start), float(end), number_of_values)

        self.gas_model = {
            'calculation': calculation,
            'type': type,
            'gas': gas,
            'mass': mass,
            'temp': temp,
            'pressure': pressure,
            'volume': volume
        }

        return self.gas_model

    def write_output(self, model, variable : np.array, result : np.array):
        """
        Writes calculation info and result to the output file named with same name
        as input file but with .out extension.

        Parameters
        ----------
        model : Model
            Object of Model class that describes the gas and parameters used in calculation.
        variable : np.array
            Quantity that has been given in input file.
        result : np.array
            Quantity that has been calculated based on variable.
        """

        desc_str = '\n-------------\n'
        desc_str += 'TULOS\n'
        desc_str += '-------------\n\n\n'
        desc_str += 'Tilavuus (l) \tPaine (atm)\n'

        with open(self.output, 'w') as opfile:
            opfile.write('\n-------------\n')
            opfile.write('LÄHTÖTIEDOT')
            opfile.write('\n-------------\n\n')
            opfile.write(str(model))
            opfile.write(desc_str)

            for i in range(len(variable)):
                opfile.write(f'{variable[i]:.6f}\t{result[i]:.6f}\n')

            opfile.write('\n\n***\n')
            opfile.write('End of output file')
            opfile.write('\n***')


    def remove_comments(self, row):
        """
        Removes commented parts from input file.

        Parameters
        ----------
        row : list
            A list of words in one line in input file.
        """

        if '#' in row:
            comment_index = row.index('#')
            return row[:comment_index]
        return row

    def find_value(self, row):
        """
        Finds a value from the row of input file. Value is separated
        from the keyword with ":".

        Parameters
        ----------
        row : list
            A list of words in one line in input file.
        """
        return row[row.index(':') + 1]

class Gas:
    def __init__(self, model: dict):
        """
        Parameters
        ----------
        model : dictionary with keys
            'calculation' = which calculation will be executed ex. gas volume = 'vol' and pressure = 'pre'
            'type' = which model type is used, ideal or vdw
            'gas' = which gas is used, for example O2
            'temp' = gas temperature in kelvins
            'mass' = gas mass in grams
            'pressure' = gas pressure in atm, this can be a numpy array
            'volume' = gas volume in l, this can be a numpy array
        """

        self.model = model
        self.type = model['type']
        self.name = self.model['gas']

        try:
            self.a = float(data[self.model['gas']]['a'])
            self.b = float(data[self.model['gas']]['b'])
            self.n = float(self.calculate_n())
        except KeyError:
            print('Check your input file.')
            print('Error might be found in gas definition.')
            exit()
        try:
            self.V = self.model['volume']
        except Exception as e:
            self.V = None
        try:
            self.p = self.model['pressure']
        except Exception as e:
            self.p = None
        try:
            self.T = float(self.model['temp'])
        except Exception as e:
            self.T = None
            

    def __repr__(self):
        rpr = '================\n'
        rpr += f'  {self.name}  \n'
        rpr += f'  {self.type}  \n'
        rpr += '================\n\n'
        return rpr

    def calculate_n(self):
        """
        Calculates molar mass for Gas object (self).
        """

        M = float(data[self.model['gas']]['molar_mass'])
        m = float(self.model['mass'])
        return m/M

class UserInterface:
    def __init__(self, filehandler: FileHandler):
        self.fh = filehandler
        self.gas_model = self.fh.read_file()
        self.gas = Gas(self.gas_model)
        self.calculation = self.gas_model['calculation']
        self.model = self.create_gas_model()

    def create_gas_model(self):
        """
        Function that creates right gas model based on 'type' keyword on input file.
        """

        try:
            if self.gas.type == 'ideal':
                return Ideal(self.gas.n, self.gas.T, self.gas.p, self.gas.V)
            if self.gas.type == 'vdw':
                return VDW(self.gas.a, self.gas.b, self.gas.n, self.gas.T, self.gas.p, self.gas.V)
        except AttributeError:
            print('Check the input file.')
            print('There might be something wrong with gas definition.')
            exit()

    def calculate_value(self):
        """
        Function that executes right calculation based on input files 'calculation' keyword.
        """

        try:
            if self.calculation == 'vol':
                result = self.model.volume()
            if self.calculation == 'pre':
                result = self.model.pressure()

            return result
        except Exception:
            print('Something went wrong with calculation.')
            print('Check your input files keywords and values.')
            exit()

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
    n = m / M
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

    # inputfile = './test_input.inp'
    inputfile = sys.argv[1]
    fh = FileHandler(inputfile)

    with fh:
        ui = UserInterface(fh)
        
    model = ui.create_gas_model()

    # Test, calculating volumes when pressures has been given
    volume = ui.calculate_value()

    pressure = model.p
    fh.write_output(model, pressure, volume)

    # plt.plot(pressure, pressure*volume)
    # plt.show()