import math

class Ponto:   
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def imprime(self, msg=None):
        if msg is not None:
            print (msg, self.x, self.y, self.z)
        else:
            print (self.x, self.y, self.z)

    def set(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
            x = self.x + other.x
            y = self.y + other.y
            return Ponto(x, y)

    def __sub__(self, other):
            x = self.x - other.x
            y = self.y - other.y
            return Ponto(x, y)

    def __mul__(self, other: int):
            x = self.x * other
            y = self.y * other
            return Ponto(x, y)

    def rotacionaZ(self, angulo):
        anguloRad = angulo * 3.14159265359/180.0
        xr = self.x*math.cos(anguloRad) - self.y*math.sin(anguloRad)
        yr = self.x*math.sin(anguloRad) + self.y*math.cos(anguloRad)
        self.x = xr
        self.y = yr

    def rotacionaY(self, angulo):
        anguloRad = angulo* 3.14159265359/180.0
        xr =  self.x*math.cos(anguloRad) + self.z*math.sin(anguloRad)
        zr = -self.x*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        self.x = xr
        self.z = zr
   
    def rotacionaX(self, angulo):
        anguloRad = angulo* 3.14159265359/180.0
        yr =  self.y*math.cos(anguloRad) - self.z*math.sin(anguloRad)
        zr =  self.y*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        self.y = yr
        self.z = zr

def intersec2d(k: Ponto, l: Ponto, m: Ponto, n: Ponto) -> (int, float, float):
    det = (n.x - m.x) * (l.y - k.y)  -  (n.y - m.y) * (l.x - k.x)

    if (det == 0.0):
        return 0, None, None

    s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x))/ det
    t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x))/ det

    return 1, s, t # há intersecção

def HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto) -> bool:
    ret, s, t = intersec2d( k,  l,  m,  n)

    if not ret: return False

    return s>=0.0 and s <=1.0 and t>=0.0 and t<=1.0

