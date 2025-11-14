from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Objeto3D import Objeto3D
from Ponto import Ponto
import math
import sys


class Main:
    
    look_at_x = 0
    look_at_y = 0
    look_at_z = 1
    user_pos_x = 2
    user_pos_y = 2
    user_pos_z = 2

    constante_camera = 0.2


    objeto1 = Objeto3D()
    objeto2 = Objeto3D()
    objeto_morph = Objeto3D()
    

    janela1_id = None
    janela2_id = None
    janela_morph_id = None
        
    animacao_ativa = False
    frame_atual = 0
    total_frames = 120
    associacoes = []
        
    arquivo1 = None
    arquivo2 = None

    
    def CarregarObjetos(self, arquivo1, arquivo2):
        print("comecando")
        self.arquivo1 = arquivo1
        self.arquivo2 = arquivo2        
        self.objeto1.LoadFile(arquivo1)        
        self.objeto2.LoadFile(arquivo2)
        self.NormalizarObjeto(self.objeto1)
        self.NormalizarObjeto(self.objeto2)
        
        self.AssociarFaces()
        print("carregamento terminado")

    def NormalizarObjeto(self, obj):
      
        min_p = Ponto(10000.0, 10000.0, 10000.0)
        max_p = Ponto(-10000.0, -10000.0, -10000.0)
        
        for vertice in obj.vertices:
            min_p.x = min(min_p.x, vertice.x)
            min_p.y = min(min_p.y, vertice.y)
            min_p.z = min(min_p.z, vertice.z)
            max_p.x = max(max_p.x, vertice.x)
            max_p.y = max(max_p.y, vertice.y)
            max_p.z = max(max_p.z, vertice.z)
        
        centro = Ponto(
            (min_p.x + max_p.x) / 2,
            (min_p.y + max_p.y) / 2,
            (min_p.z + max_p.z) / 2
        )
        
        normal_x = max_p.x - min_p.x
        normal_y = max_p.y - min_p.y
        normal_z = max_p.z - min_p.z
        max_dim = max(normal_x, normal_y, normal_z)
        
        if max_dim == 0:
            return
        

        for vertice in obj.vertices:
            vertice.x = (vertice.x - centro.x) / max_dim
            vertice.y = (vertice.y - centro.y) / max_dim
            vertice.z = (vertice.z - centro.z) / max_dim
            

    def CalculaCentroideFace(self, obj, face_indices):
        soma = Ponto(0, 0, 0)
        for indice in face_indices:
            vertice = obj.vertices[indice]
            soma.x += vertice.x
            soma.y += vertice.y
            soma.z += vertice.z
        
        quant_vert = len(face_indices)
        return Ponto(soma.x/quant_vert, soma.y/quant_vert, soma.z/quant_vert)

    def Distancia(self, ponto_1, ponto_2):
        dis_x = ponto_1.x - ponto_2.x
        dis_y = ponto_1.y - ponto_2.y
        dis_z = ponto_1.z - ponto_2.z
        return math.sqrt(dis_x*dis_x + dis_y*dis_y + dis_z*dis_z)

    def AssociarFaces(self):
        self.associacoes = []
        
        centroides1 = [self.CalculaCentroideFace(self.objeto1, face) 
                      for face in self.objeto1.faces]
        centroides2 = [self.CalculaCentroideFace(self.objeto2, face) 
                      for face in self.objeto2.faces]
        
        quant_faces_1 = len(self.objeto1.faces)
        quant_faces_2 = len(self.objeto2.faces)
        
        if quant_faces_1 <= quant_faces_2:
            faces2_usadas = set()
            for i, c1 in enumerate(centroides1):
                melhor_dist = 100000.0
                melhor_j = -1
                
                for j, c2 in enumerate(centroides2):
                    if j in faces2_usadas:
                        continue
                    dist = self.Distancia(c1, c2)
                    if dist < melhor_dist:
                        melhor_dist = dist
                        melhor_j = j
                
                if melhor_j != -1:
                    self.associacoes.append((i, melhor_j))
                    faces2_usadas.add(melhor_j)
        else:                   
            faces1_usadas = set()
            for j, c2 in enumerate(centroides2):
                melhor_dist = 100000.0
                melhor_i = -1
                
                for i, c1 in enumerate(centroides1):
                    if i in faces1_usadas:
                        continue
                    dist = self.Distancia(c1, c2)
                    if dist < melhor_dist:
                        melhor_dist = dist
                        melhor_i = i
                
                if melhor_i != -1:
                    self.associacoes.append((melhor_i, j))
                    faces1_usadas.add(melhor_i)

    def InterpolaPonto(self, p1, p2, tempo):
        return Ponto(
            p1.x + (p2.x - p1.x) * tempo,
            p1.y + (p2.y - p1.y) * tempo,
            p1.z + (p2.z - p1.z) * tempo
        )

    def CriaObjetoMorphing(self, momento):
        obj = Objeto3D()
        
        for indice1, indice2 in self.associacoes:
            face1 = self.objeto1.faces[indice1]
            face2 = self.objeto2.faces[indice2]
            
            n_vertices = max(len(face1), len(face2))
            nova_face = []
            
            for i in range(n_vertices):
                i1 = i % len(face1)
                i2 = i % len(face2)
                
                vertice1 = self.objeto1.vertices[face1[i1]]
                vertice2 = self.objeto2.vertices[face2[i2]]
                
                novo_vertice = self.InterpolaPonto(vertice1, vertice2, momento)
                
                indice_vertice = len(obj.vertices)
                obj.vertices.append(novo_vertice)
                nova_face.append(indice_vertice)
            
            obj.faces.append(nova_face)
        
        return obj

    def ConfigurarJanela(self):
        glClearColor(0.5, 0.5, 0.9, 1.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        self.DefineLuz()
        self.ConfigurarCamera()

    def DefineLuz(self):
        luz_ambiente = [0.4, 0.4, 0.4]
        luz_difusa = [0.7, 0.7, 0.7]
        luz_especular = [0.9, 0.9, 0.9]
        posicao_luz = [2.0, 3.0, 0.0]
        especularidade = [1.0, 1.0, 1.0]
        
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)
        glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
        glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
        glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)
        glEnable(GL_LIGHT0)
        glMaterialfv(GL_FRONT, GL_SPECULAR, especularidade)
        glMateriali(GL_FRONT, GL_SHININESS, 51)

    def ConfigurarCamera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, 1.0, 0.01, 50)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            self.user_pos_x, self.user_pos_y, self.user_pos_z,  
            self.look_at_x, self.look_at_y, self.look_at_z,      
            0, 1, 0                                                
        )

    def DesenhaObjeto(self, obj):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glColor3f(0.7, 0.7, 0.7)
        for f in obj.faces:
            glBegin(GL_TRIANGLE_FAN)
            for iv in f:
                v = obj.vertices[iv]
                glVertex3f(v.x, v.y, v.z)
            glEnd()
        
        glColor3f(0, 0, 0)
        glLineWidth(1)
        for f in obj.faces:
            glBegin(GL_LINE_LOOP)
            for iv in f:
                v = obj.vertices[iv]
                glVertex3f(v.x, v.y, v.z)
            glEnd()
        
        glutSwapBuffers()

    def InicializarJanelas(self):

        glutInitWindowSize(400, 400)
        glutInitWindowPosition(100, 100)
        self.janela1_id = glutCreateWindow(b'janela 1')
        self.ConfigurarJanela()
        glutDisplayFunc(lambda: self.DesenhaObjeto(self.objeto1))
        glutReshapeFunc(self.Redimensiona)
        glutKeyboardFunc(self.Teclado)
        
        glutInitWindowSize(400, 400)
        glutInitWindowPosition(510, 100)
        self.janela2_id = glutCreateWindow(b'janela 2')
        self.ConfigurarJanela()
        glutDisplayFunc(lambda: self.DesenhaObjeto(self.objeto2))
        glutReshapeFunc(self.Redimensiona)
        glutKeyboardFunc(self.Teclado)

        

    def AbrirJanelaMorph(self):
        
        glutInitWindowSize(400, 400)
        glutInitWindowPosition(920, 100)
        self.janela_morph_id = glutCreateWindow(b'janela 3 morphing')
        self.ConfigurarJanela()
        glutDisplayFunc(self.DesenhaMorph)
        glutReshapeFunc(self.Redimensiona)
        glutKeyboardFunc(self.Teclado)
        

        
        
        self.animacao_ativa = False
        self.frame_atual = 0
        glutTimerFunc(33, self.AnimacaoTimer, 0)

    def DesenhaMorph(self):
        tempo = self.frame_atual / self.total_frames
        self.objeto_morph = self.CriaObjetoMorphing(tempo)
        self.DesenhaObjeto(self.objeto_morph)

    def Redimensiona(self, w, h):
        if h == 0:
            h = 1
        glViewport(0, 0, w, h)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h
        gluPerspective(60, aspect, 0.01, 50)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(2, 2, 2, 0, 0, 0, 0, 1, 0)

    def Teclado(self, key, x, y):
        atualiza_camera = False

        if key == b' ': 
            self.AbrirJanelaMorph() 
            self.animacao_ativa = not self.animacao_ativa
            if self.animacao_ativa:
                glutTimerFunc(33, self.AnimacaoTimer, 0)

            
        elif key == b'm':
            self.frame_atual = 0         
            glutPostRedisplay()
            glLoadIdentity()

    
        
        elif key == b'\x1b':  
            sys.exit(0)

        elif key == b'w':
            self.user_pos_z -= self.constante_camera
            self.look_at_z -= self.constante_camera
            atualiza_camera = True
        
        elif key == b's': 
            self.user_pos_z += self.constante_camera
            self.look_at_z += self.constante_camera
            atualiza_camera = True
        
        elif key == b'a':
            self.user_pos_x -= self.constante_camera
            self.look_at_x -= self.constante_camera
            atualiza_camera = True
        
        elif key == b'd':  
            self.user_pos_x += self.constante_camera
            self.look_at_x += self.constante_camera
            atualiza_camera = True
        
        elif key == b'q':
            self.user_pos_y += self.constante_camera
            self.look_at_y += self.constante_camera
            atualiza_camera = True
        
        elif key == b'e':  
            self.user_pos_y -= self.constante_camera
            self.look_at_y -= self.constante_camera
            atualiza_camera = True

        if atualiza_camera:
            self.ConfigurarCamera()
            glutPostRedisplay()


    
    def AnimacaoTimer(self, valor):
        if not self.animacao_ativa:
            return
        
        if self.frame_atual < self.total_frames:
            self.frame_atual += 1

        
        if self.janela_morph_id is not None:
            glutSetWindow(self.janela_morph_id)
            glutPostRedisplay()
        
        glutTimerFunc(30, self.AnimacaoTimer, 0)

    def Executar(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH | GLUT_DOUBLE)
        
        self.InicializarJanelas()
        glutKeyboardFunc(self.Teclado)
        
        
        try:
            glutMainLoop()
        except SystemExit:
            pass


if __name__ == '__main__':
    
    arquivo1 = sys.argv[1]  
    arquivo2 = sys.argv[2]  
    
    
    sistema = Main()
    sistema.CarregarObjetos(arquivo1, arquivo2)
    sistema.Executar()




    