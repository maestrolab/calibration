"""
Created on Jan 21 2019
@author: Pedro Leal
"""

from scipy.optimize import differential_evolution, minimize
from calibration.filehandling import output_reader
import numpy as np


def fitting(f, optimizer='differential_evolution'):
    """Optimize properties for class f to represent raw data.
       - f: any class with attributes .error, .x0, and .bound
       - optimizer: BFGS (gradient) or differential_evolution"""

    print('Fitting ' + f.transformation)

    if optimizer == 'BFGS':
        result = minimize(f.error, f.x0, method='BFGS')
    elif optimizer == 'differential_evolution':
        result = differential_evolution(f.error, f.bounds, popsize=100,
                                        maxiter=100)

    f.update(result.x)
    if f.transformation == 'Austenite':
        print('As=', f.props[1, 0], 'Af=', f.props[-2, 0])
    elif f.transformation == 'Martensite':
        print('Ms=', f.props[-2, 0], 'Mf=', f.props[1, 0])
    return(f)


def processing_raw(filename, driven='temperature'):
    """Convert .txt file to a numpy array (temperature, strain, sigma) for
       Austenite and Martensite.
       - filename: string for file to process"""
    ok = input('You will be asked for 3 column inputs. Only temperaure and strain is necessary. The 3rd data set can be named another name other than "temperature" and/or "stress" to preserve the data for future use. Use lowercase for inputs. Type "ok" to continue: ')
    x1a = input('Enter the 1st Column name: ')
    x2a = input('Enter the 2nd Column name: ')
    x3a = input('Enter the 3rd Column name: ')

    raw_data = output_reader(filename, header=[x1a, x2a, x3a])

#below is the function to move around the read columns based on the format of the column datatypes
    if (x1a == 'temperature') and (x2a == 'strain'):
        x1b = raw_data[x1a] #ideal temperature
        x2b = raw_data[x2a] #ideal strain
        x3b = raw_data[x3a] #anything else, irrelavent
    elif (x1a == 'temperature') and (x3a == 'strain'):
        x1b = raw_data[x1a] #ideal temperature
        x3b = raw_data[x2a] #ideal strain
        x2b = raw_data[x3a] #anything else, irrelavent
    elif (x2a == 'temperature') and (x1a == 'strain'):
        x2b = raw_data[x1a] #ideal temperature
        x1b = raw_data[x2a] #ideal strain
        x3b = raw_data[x3a] #anything else, irrelavent
    elif (x2a == 'temperature') and (x3a == 'strain'):
        x2b = raw_data[x1a] #ideal temperature
        x3b = raw_data[x2a] #ideal strain
        x1b = raw_data[x3a] #anything else, irrelavent
    elif (x3a == 'temperature') and (x2a == 'strain'):
        x3b = raw_data[x1a] #ideal temperature
        x2b = raw_data[x2a] #ideal strain
        x1b = raw_data[x3a] #anything else, irrelavent
    elif (x3a == 'temperature') and (x1a == 'strain'):
        x3b = raw_data[x1a] #ideal temperature
        x1b = raw_data[x2a] #ideal strain
        x2b = raw_data[x3a] #anything else, irrelavent

    if driven == 'temperature':
        i = x1b.index(max(x1b))
    else:
        raise NotImplementedError

    austenite = np.vstack([x1b[:i+1], x2b[:i+1], x3b[:i+1]]).T
    martensite = np.vstack([x1b[i:], x2b[i:], x3b[i:]]).T
    return({'Austenite': austenite, 'Martensite': martensite})


""" raw_data = output_reader(filename, header=['Temperature', "Strain", "Stress"])
    temperature = raw_data['Temperature']
    strain = raw_data['Strain']
    stress = raw_data['Stress']

    if driven == 'temperature':
        i = temperature.index(max(temperature))
    else:
        raise NotImplementedError

    austenite = np.vstack([temperature[:i+1], strain[:i+1], stress[:i+1]]).T
    martensite = np.vstack([temperature[i:], strain[i:], stress[i:]]).T
    return({'Austenite': austenite, 'Martensite': martensite})"""