## 3D Object Morphing
Aplicação de morphing entre objetos 3D desenvolvida em Python com OpenGL, que permite visualizar o morphing suavelmente.

# Descrição
Este projeto implementa um sistema de morphing 3D que carrega dois objetos no formato OBJ e realiza uma interpolação animada entre eles. O sistema utiliza associação de faces baseada em proximidade de centroides para criar transições suaves entre geometrias diferentes.

# Funcionalidades
Visualização Múltipla: Três janelas simultâneas mostrando o objeto 1, objeto 2 e o morphing
Animação Automática: Transição suave com 120 frames entre os objetos
Normalização Automática: Os objetos são centralizados e escalados para melhor visualização
Iluminação 3D: Sistema de iluminação com componentes ambiente, difusa e especular
Controle de Câmera: Navegação interativa no ambiente 3D
Renderização Mista: Visualização com faces preenchidas e wireframe

# Tecnologias
Python 3.x
PyOpenGL - Biblioteca para renderização OpenGL
GLUT - Gerenciamento de janelas e eventos
📦 Instalação
Clone o repositório:
bash
git clone <url-do-repositorio>
cd morphing-3d
Instale as dependências:
bash
pip install PyOpenGL PyOpenGL-accelerate

# Como Usar
Execute o programa passando dois arquivos OBJ como argumentos:

bash
python Main.py objeto1.obj objeto2.obj
Controles
Tecla	Ação
Espaço	Abre a janela de morphing e inicia/pausa a animação
m	Reinicia a animação do morphing
w	Move a câmera para frente
s	Move a câmera para trás
a	Move a câmera para a esquerda
d	Move a câmera para a direita
q	Move a câmera para cima
e	Move a câmera para baixo
ESC	Sai da aplicação

# Algoritmo de Morphing
O sistema utiliza os seguintes passos para realizar o morphing:

Normalização: Ambos os objetos são centralizados e escalados proporcionalmente
Associação de Faces: Calcula centroides de cada face e associa faces mais próximas entre os objetos
Interpolação: Para cada frame, interpola linearmente os vértices correspondentes
Renderização: Desenha o objeto intermediário com a geometria interpolada
Associação de Faces
Calcula o centroide de cada face (média das posições dos vértices)
Associa faces dos dois objetos baseando-se na menor distância euclidiana
Lida com objetos com diferentes números de faces

# Formato de Entrada
Os arquivos devem estar no formato OBJ padrão:

v x y z          # Vértice
f v1 v2 v3 ...   # Face (índices dos vértices)
Nota: Os índices das faces no arquivo OBJ começam em 1, mas são convertidos para base 0 internamente.

# Parâmetros Configuráveis
No código Main.py, você pode ajustar:

total_frames: Número de frames da animação (padrão: 120)
constante_camera: Velocidade de movimento da câmera (padrão: 0.2)
Posição inicial da câmera: user_pos_x, user_pos_y, user_pos_z
Ponto de foco: look_at_x, look_at_y, look_at_z

