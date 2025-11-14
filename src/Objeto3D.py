from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Ponto import *

class Objeto3D:
        
    def __init__(self):
        self.vertices = []
        self.faces    = []
        self.position = Ponto(0,0,0)
        self.rotation = (0,0,0,0)
        pass

    def LoadFile(self, file:str):
        f = open(file, "r")

        for line in f:
            values = line.split(' ')

            if values[0] == 'v': 
                self.vertices.append(Ponto(float(values[1]),
                                           float(values[2]),
                                           float(values[3])))

            if values[0] == 'f':
                self.faces.append([])
                for fVertex in values[1:]:
                    fInfo = fVertex.split('/')
                    self.faces[-1].append(int(fInfo[0]) - 1) 
        pass

    def DesenhaVertices(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(.1, .1, .8)
        glPointSize(8)

        glBegin(GL_POINTS)
        for v in self.vertices:
            glVertex(v.x, v.y, v.z)
        glEnd()
        
        glPopMatrix()
        pass

    def DesenhaWireframe(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0, 0, 0)
        glLineWidth(2)        
        
        for f in self.faces:            
            glBegin(GL_LINE_LOOP)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()
        
        glPopMatrix()
        pass

    def Desenha(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0.34, .34, .34)
        glLineWidth(2)        
        
        for f in self.faces:            
            glBegin(GL_TRIANGLE_FAN)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()
        
        glPopMatrix()
        pass

def CalculaBounding(self):
    
    min_p = Ponto(100000.0,100000.0, 100000.0)
    max_p = Ponto(-100000.0, -100000.0, -100000.0)
    
    for vertice in self.vertices:
        min_p.x = min(min_p.x, vertice.x)
        min_p.y = min(min_p.y, vertice.y)
        min_p.z = min(min_p.z, vertice.z)
        max_p.x = max(max_p.x, vertice.x)
        max_p.y = max(max_p.y, vertice.y)
        max_p.z = max(max_p.z, vertice.z)

    return min_p, max_p

def CalculaCentroide(self):

    
    soma = Ponto(0, 0, 0)
    for vertice in self.vertices:
        soma.x += vertice.x
        soma.y += vertice.y
        soma.z += vertice.z
    
    n = len(self.vertices)
    return Ponto(soma.x/n, soma.y/n, soma.z/n)

def Normalizar(self):
    min_p, max_p = self.CalculaBounding()
    
    dx = max_p.x - min_p.x
    dy = max_p.y - min_p.y
    dz = max_p.z - min_p.z
    
    max_dim = max(dx, dy, dz)
    
    if max_dim == 0:
        return
    centroide = self.CalculaCentroide()
    
    for vertice in self.vertices:
        vertice.x = (vertice.x - centroide.x) / max_dim
        vertice.y = (vertice.y - centroide.y) / max_dim
        vertice.z = (vertice.z - centroide.z) / max_dim


def CalculaCentroideFace(self, face_indices):

    soma = Ponto(0, 0, 0)
    for indice in face_indices:
        vertice = self.vertices[indice]
        soma.x += vertice.x
        soma.y += vertice.y
        soma.z += vertice.z
    
    n = len(face_indices)
    return Ponto(soma.x/n, soma.y/n, soma.z/n)

def Distancia(p1: Ponto, p2: Ponto):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dz = p1.z - p2.z
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def AssociarFaces(obj1: Objeto3D, obj2: Objeto3D):
    associacoes = []
    
    centroides_1 = [obj1.CalculaCentroideFace(face) for face in obj1.faces]
    centroides_2 = [obj2.CalculaCentroideFace(face) for face in obj2.faces]
    
    faces2_usadas = set()
    
    for i, cen_1 in enumerate(centroides_1):
        melhor_dist = 100000
        melhor_j = -1
        
        for j, cen_2 in enumerate(centroides_2):
            if j in faces2_usadas:
                continue
            
            dist = Distancia(cen_1, cen_2)
            if dist < melhor_dist:
                melhor_dist = dist
                melhor_j = j
        
        if melhor_j != -1:
            associacoes.append((i, melhor_j))
            faces2_usadas.add(melhor_j)
    
    faces1_nao_associadas = set(range(len(obj1.faces))) - set([a[0] for a in associacoes])
    faces2_nao_associadas = set(range(len(obj2.faces))) - faces2_usadas
    

    return associacoes


def InterpolaPonto(p1: Ponto, p2: Ponto, t: float):
    return Ponto(
        p1.x + (p2.x - p1.x) * t,
        p1.y + (p2.y - p1.y) * t,
        p1.z + (p2.z - p1.z) * t
    )

def CriarObjetoIntermediario(obj1: Objeto3D, obj2: Objeto3D, associacoes, t: float):
    obj_morph = Objeto3D()
    
    for idx_face1, idx_face2 in associacoes:
        face1 = obj1.faces[idx_face1]
        face2 = obj2.faces[idx_face2]
        
        
        
        novos_vertices = []
        for i in range(min(len(face1), len(face2))):
            v1 = obj1.vertices[face1[i]]
            v2 = obj2.vertices[face2[i]]
            novo_v = InterpolaPonto(v1, v2, t)
            novos_vertices.append(novo_v)
        
       
    
    return obj_morph

def Animar(self):
    if not self.animacao_ativa:
        return
    
    self.frame_atual += 1
    
    if self.frame_atual > self.total_frames:
        self.frame_atual = 0
    
    t = self.frame_atual / self.total_frames
    self.objeto_morph = CriarObjetoIntermediario(
        self.objeto1, 
        self.objeto2, 
        self.associacoes, 
        t
    )
    
    glutPostRedisplay()
    glutTimerFunc(33, lambda x: self.Animar(), 0)  # ~30 FPS

def CriarJanelas(self):
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(100, 100)
    self.janela1_id = glutCreateWindow(b'Objeto 1')
    self.ConfigurarJanela()
    glutDisplayFunc(lambda: self.DesenhaJanela1())
    
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(510, 100)
    self.janela2_id = glutCreateWindow(b'Objeto 2')
    self.ConfigurarJanela()
    glutDisplayFunc(lambda: self.DesenhaJanela2())