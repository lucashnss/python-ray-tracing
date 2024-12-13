from obj_reader import ObjReader

# Divirtam-se :)

def main():
    obj = ObjReader('inputs/icosahedron.obj')
    obj.print_faces()

if __name__ == "__main__":
    main()
