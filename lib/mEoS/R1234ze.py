#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class R1234ze(MEoS):
    """Multiparameter equation of state for R1234ze"""
    name = "trans-1,3,3,3-tetrafluoropropene"
    CASNumber = "29118-24-9"
    formula = "CHF=CHCF3"
    synonym = "R-1234ze"
    rhoc = unidades.Density(489.238464)
    Tc = unidades.Temperature(382.513)
    Pc = unidades.Pressure(3634.9, "kPa")
    M = 114.0416  # g/mol
    Tt = unidades.Temperature(168.62)
    Tb = unidades.Temperature(254.177)
    f_acent = 0.313
    momentoDipolar = unidades.DipoleMoment(1.27, "Debye")
    id = 671

    CP1 = {"ao": 6.259,
           "an": [], "pow": [],
           "ao_exp": [7.303, 8.597, 2.333], "exp": [691, 1705, 4216],
           "ao_hyp": [], "hyp": []}
           
    Fi2 = {"ao_log": [1, 3],
           "pow": [0, 1],
           "ao_pow": [-10.8724711, -30.1326538],
           "ao_exp": [6.07536, 9.95795],
           "titao": [289/Tc, 1303/Tc], 
           "ao_hyp": [], "hyp": []}

    helmholtz2 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for R1234ze of McLinden et al. (2010).",
        "__doc__":  u"""McLinden, M.O., Thol, M., and Lemmon, E.W. "Thermodynamic Properties of trans-1,3,3,3-Tetrafluoropropene [R1234ze(E)]: Measurements of Density and Vapor Pressure and a Comprehensive Equation of State," International Refrigeration and Air Conditioning Conference at Purdue, July 12-15, 2010.""",
        "R": 8.314472,
        "cp": CP1,
        
        "Tmin": Tt, "Tmax": 420.0, "Pmax": 20000.0, "rhomax": 13.20, 
        "Pmin": 0.23, "rhomin": 13.19, 

        "nr1": [0.4434245e-1, 0.1646369e1, -0.2437488e1, -0.517056, 0.1815626],
        "d1": [4, 1, 1, 2, 3],
        "t1": [1.0, 0.31, 0.923, 1.06, 0.44],

        "nr2": [-0.1210104e1, -0.5944653, 0.7521992, -0.6747216, -0.2448183e-1],
        "d2": [1, 3, 2, 2, 7],
        "t2": [2.08, 2.32, 1.25, 2.0, 1.0],
        "c2": [2, 2, 1, 2, 1],
        "gamma2": [1]*5,

        "nr3": [0.1379434e1, -0.4697024, -0.2036158, -0.8407447e-1, 0.5109529e-3],
        "d3": [1, 1, 3, 3, 2],
        "t3": [0.93, 1.93, 2.69, 1.0, 2.0],
        "alfa3": [1.0, 1.4, 1.134, 7.68, 24.],
        "beta3": [1.64, 1.57, 1.49, 257.0, 45.0],
        "gamma3": [1.13, 0.61, 0.65, 1.13, 1.34],
        "epsilon3": [0.711, 0.856, 0.753, 0.772, 1.88],
        "nr4": []}

    helmholtz3 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for R1234yf of Akasaka (2011).",
        "__doi__": {"autor": "Akasaka, R.",
                    "title": "New Fundamental Equations of State with a Common Functional Form for 2,3,3,3-Tetrafluoropropene (R-1234yf) and trans-1,3,3,3-Tetrafluoropropene (R-1234ze(E))", 
                    "ref": "Int J Thermophys (2011) 32:1125–1147",
                    "doi": "10.1007/s10765-011-0992-0"}, 
        "R": 8.314472,
        "cp": Fi2,
        "ref": "IIR", 

        "Tmin": 240., "Tmax": 420.0, "Pmax": 15000.0, "rhomax": 13.20, 
        "Pmin": 0.23, "rhomin": 13.19, 

        "nr1": [0.85579765e1, -0.94701332e1, -0.25013623, 0.13789870, 0.12177113e-1],
        "d1": [1, 1, 1, 2, 5],
        "t1": [0.66886, 0.83392, 1.6982, 1.8030, 0.36657],
 
        "nr2": [-0.14227996, 0.10096648, 0.17504319e-1, -0.17627303e-1, -0.14705120e-1, 0.37202269, -0.30138266, -0.92927274e-1, 0.87051177e-1, 0.18113770e-1, -0.16018424e-1, 0.53809860e-2],
        "d2": [1, 3, 5, 7, 1, 2, 2, 3, 4, 2, 3, 5],
        "t2": [3.8666, 1.0194, 0, 1.1655, 8.3101, 6.1459, 8.3495, 6.0422,
               7.444, 15.433, 21.543, 15.499],
        "c2": [1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3],
        "gamma2": [1]*12}

    eq = helmholtz1, helmholtz2, helmholtz3

    _surface = {"__doi__": 
                    {"autor": "Tanaka, K., Higashi, Y.",
                     "title": "Surface Tension of trans-1,3,3,3-Tetrafluoropropene and trans-1,3,3,3-Tetrafluoropropene + Difluoromethane Mixture", 
                     "ref": "J. Chem. Eng. Japan, 2013",
                     "doi": "10.1252/jcej.13we021"}, 
                "sigma": [0.05681], "exp": [1.23]}
    _vapor_Pressure = {
        "eq": 5,
        "ao": [-0.76813e1, 0.31759e1, -0.26397e1, -0.35234e1],
        "exp": [1.0, 1.5, 1.8, 3.9]}
    _liquid_Density = {
        "eq": 1,
        "ao": [0.16130e1, 0.46976e1, -0.68759e1, 0.34227e1],
        "exp": [0.31, 0.94, 1.2, 1.5]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-0.24897e1, -0.63324e1, -0.20262e2, -0.62612e2],
        "exp": [0.36, 1.07, 3.0, 6.8]}

    thermo0 = {"eq": 1,
               "__name__": "Perkins (2010)",
               "__doc__": """Perkins, R.A. and Huber, M.L., unpublished work, 2010.""",

               "Tref": 382.52, "kref": 1,
               "no": [0.285145e-2, -0.439091e-2, 0.232616e-1],
               "co": [0, 1, 2],

               "Trefb": 367.85, "rhorefb": 4.17, "krefb": 1.,
               "nb": [-0.10750600e-2, -0.11560800e-1, 0.76230400e-2, 0.0, 0.0,
                      0.0, 0.10181100e-1, -0.22450100e-2, 0.0, 0.0],
               "tb": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               "db": [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
               "cb": [0]*10,

               "critical": 3,
               "gnu": 0.63, "gamma": 1.239, "R0": 1.03,
               "Xio": 0.194e-9, "gam0": 0.0496, "qd": 5.285e-10, "Tcref": 573.78}

    _thermal = thermo0,


if __name__ == "__main__":
#    import doctest
#    doctest.testmod()

    cyc5=R1234ze(T=300., rho=5.0)
    print "%0.1f %0.2f %0.4f %0.6f %0.6f %0.6f %0.3f %0.5f %0.6f %0.9f" % (cyc5.T, cyc5.P.MPa, cyc5.rho, cyc5.cv.kJkgK, cyc5.cp.kJkgK, cyc5.cp0.kJkgK, cyc5.w, cyc5.joule.KMPa, cyc5.virialB, cyc5.virialC)
