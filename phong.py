import numpy as np


def phong(ka, Ia, Il, kd, Od, N, L, ks, R, V, n):
    """
        ka (entre 0 e 1): coeficiente ambiental
        Ia (conjunto RGB do tipo [[0,255],[0,255], [0,255]]): cor da luz ambiental
        Il (array de RGBs do tipo [[0,255], [0,255], [0,255],  ...]) = array com as luzes do ambiente
        kd (entre 0 e 1): coeficiente de difusão do objeto
        Od (conjunto RGB do tipo [[0,255],[0,255], [0,255]]): conjunto RGB que representa a cor do objeto
        N (vetor): vetor normal ao ponto de interseção do objeto com a câmera
        L (array de vetores): vetores que representam as direções das luzes
        ks (entre 0 e 1): coeficiente especular do objeto
        R (array de vetores): vetores que representam as direções dos raios refletidos
        V (vetor): vetor que representa a direção da câmera
        n (inteiro): expoente da componente especular do objeto
    Retorna:
            Um vetor RGB que representa a cor final do objeto

    """
    # Normalização das componentes
    Ia = np.array(Ia)/255.0
    Il = np.array(Il)/255.0
    Od = np.array(Od)/255.0

    # Componente Ambiental
    environmental_component = ka * Ia

    diffuse_component = np.zeros(3)
    specular_component = np.zeros(3)

    for i in range(len(Il)):
        # Cálculo da componente difusa e da componente especular
        diffuse_component += kd * Il[i] * np.maximum(0, np.dot(N, L[i])) * Od
        specular_component += ks * Il[i] * np.maximum(0, np.dot(R[i], V)**n)

    final_color = environmental_component + diffuse_component + specular_component
    final_color = np.clip(final_color, 0, 1) * 255

    return final_color