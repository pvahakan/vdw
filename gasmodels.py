from scipy.optimize import fsolve

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

    def __repr__(self) -> str:
        rpr = 'Type:\t\t ideal\n'
        rpr += '----------------------\n'
        rpr += f'Ainemäärä:\t {round(self.n, 3)} mol\n'
        rpr += f'Lämpötila:\t {self.T} K\n'
        if self.p is not None:
            rpr += f'Paineet:\n {self.p} atm\n'
        if self.V is not None:
            rpr += f'Tilavuus:\t {self.V} l\n'

        return rpr

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
        

class VDW:
    def __init__(self, a, b, n, T, p=None, V=None):
        """
        Parameters
        ----------
        a : float
            van der Waals -tilanyhtälön vakio a yksikössä L^2 * atm / mol^2
        b : float
            van der Waals -tilanyhtälön vakio b yksikössä L/mol
        n : float
            Kaasun ainemäärä mooleina
        T : float
            Kaasun lämpötila kelvineinä
        p : float
            Kaasun paine yksikössä atm
        V : float
            Kaasun tilavuus litroina
        """

        self.a = a
        self.b = b
        self.n = n
        self.T = T
        self.p = p
        self.V = V
        self.R = 0.0820574 # L*atm / mol*K

    def __repr__(self) -> str:
        rpr = 'Type:\t\t Van der Waals\n'
        rpr += '------------------------------\n'
        rpr += f'a:\t {self.a} L^2 * atm / mol^2\n'
        rpr += f'b:\t {self.b} L/mol\n\n'
        rpr += f'Ainemäärä:\t {round(self.n, 3)} mol\n'
        rpr += f'Lämpötila:\t {self.T} K\n\n'
        if self.p is not None:
            rpr += f'Paineet:\n {self.p} atm\n'
        if self.V is not None:
            rpr += f'Tilavuus:\t {self.V} l\n'

        return rpr

    def pressure(self):
        """
        Laskee kaasun paineen van der Waals -tilanyhtälön avulla.


        Return
        ------
        Palauttaa van der Waals -tilanyhtälön avulla lasketun paineen yksikössä atm

        """
        second_term = self.V / self.n - self.b
        to_substract = self.a * (self.n / self.V)**2

        self.p = (self.R * self.T) / second_term - to_substract
        return self.p

    def volume(self):
        """
        Laskee kaasun tilavuuden van der Waals -tilanyhtälön avulla.
        

        ### HOX
        ###
        ### Ei mitään hajua laskeeko tämä mitään oikein!
        ###
        ###################################################

        Return
        ------
        Palauttaa van der Waals -tilanyhtälön avulla lasketun kaasun tilavuuden litroina

        """
        # func = lambda V : (self.p + self.a * self.n**2 / V**2) * (V - self.n * self.b) - self.n * self.R * self.T
        func = lambda V, p : (p + self.a * self.n**2 / V**2) * (V - self.n * self.b) - self.n * self.R * self.T
        # print(self)
        test_value = 5

        self.V = []
        
        for p in self.p:
            sol = fsolve(func, test_value, p)
            self.V.append(sol[0])

        return self.V
