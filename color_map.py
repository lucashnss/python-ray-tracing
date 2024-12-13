from vector import Vector

class Material:
    def __init__(self):
        self.ka = Vector(0, 0, 0)
        self.kd = Vector(0, 0, 0)
        self.ks = Vector(0, 0, 0)
        self.ke = Vector(0, 0, 0)
        self.ns = 0
        self.ni = 0
        self.d = 0


class Colormap:
    '''
    Classe de leitura de arquivos .mtl, que guarda cores e propriedades de materiais.

        A saber que:
        - kd = Difuso (Cor do objeto)
        - ks = Specular (Reflexivo)
        - ke = Emissivo 
        - ka = Ambiente
        - ns = Brilho
        - ni = Índice de refração
        - d = Opacidade

        A classe precisa ser instânciada passando o caminho do arquivo .mtl correspondente
    '''
    def __init__(self, input_file):
        self.materials = {}
        self.read_file(input_file)

    def read_file(self, input_file):
        with open(input_file, 'r') as file:
            for line in file:
                if line.startswith('newmtl '):
                    self.cur_material = line.split()[1]
                    self.materials[self.cur_material] = Material()
                elif line.startswith('Ka '):
                    self.materials[self.cur_material].ka = Vector(*map(float, line[2:].split()))
                elif line.startswith('Kd '):
                    self.materials[self.cur_material].kd = Vector(*map(float, line[2:].split()))
                elif line.startswith('Ks '):
                    self.materials[self.cur_material].ks = Vector(*map(float, line[2:].split()))
                elif line.startswith('Ke '):
                    self.materials[self.cur_material].ke = Vector(*map(float, line[2:].split()))
                elif line.startswith('Ns '):
                    self.materials[self.cur_material].ns = float(line[2:])
                elif line.startswith('Ni '):
                    self.materials[self.cur_material].ni = float(line[2:])
                elif line.startswith('d '):
                    self.materials[self.cur_material].d = float(line[2:])

    def get_color(self, material_name):
        return self.materials[material_name].kd

    def get_material(self, material_name):
        return self.materials[material_name]
