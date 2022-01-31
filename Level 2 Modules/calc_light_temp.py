import math

def temp(value, Unit = 'F'):
    unit = Unit.upper()
    voltage = value / 255.0 * 3.3
    if (voltage != 3.3):
        Rt = 10*voltage/(3.3-voltage)
        tempK = 1/(1/(273.15+25)+math.log(Rt/10)/3950.0)
        tempC = tempK - 275.13
        tempD = tempC * 9/5 + 32
        if (unit == 'K'):
            return tempK
        elif(unit == 'C'):
            return tempC
        else:
            return tempD
    else:
        return 0

def light(value, Rref = 10):
    voltage = value / 255.0 * 3.3
    if (voltage != 3.3):
        Rp = Rref*voltage/(3.3-voltage)
        return 500/Rp
    else:
        return 0
    