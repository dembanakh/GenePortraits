import numpy as np
from PIL import Image


class FrequencyPortrait:

    def __init__(self, gene: str, depth: int, mod: int, remainder: int):
        m_matrix = np.zeros((2 ** depth, 2 ** depth))
        self.matrix = np.zeros((2 ** depth, 2 ** depth))

        for k in range(len(gene) - depth):
            ii = 0
            jj = 0
            for i in range(depth):
                ii += 2 ** (depth - i - 1) * Xletter[gene[k + i]]
                jj += 2 ** (depth - i - 1) * Yletter[gene[k + i]]
            m_matrix[ii, jj] += 1
            if k % mod == remainder:
                self.matrix[ii, jj] += 1
        if remainder == mod:
            self.matrix = m_matrix
        self.matrix *= 1 / m_matrix.max()

    def resize(self, size: int):
        portrait_length = len(self.matrix)
        matrix = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                matrix[i, j] = self.matrix[int(portrait_length * i // size), int(portrait_length * j // size)]

        self.matrix = matrix

    def add_contrast(self):
        self.matrix = np.sqrt(self.matrix)

    def add_frame(self):
        size = len(self.matrix)
        matrix = self.matrix
        size8 = size / 8
        for i in range(size):
            matrix[i, 0] = 1
            matrix[0, i] = 1
            matrix[size - 1, i] = 1
            matrix[i, size - 1] = 1
            matrix[int(2 * size8), i] = 1
            matrix[int(4 * size8), i] = 1
            matrix[int(6 * size8), i] = 1
            matrix[i, int(4 * size8)] = 1
            matrix[i, int(6 * size8)] = 1
        for i in range(int(6 * size8)):
            matrix[int(7 * size8), i + int(2 * size8)] = 1
        for i in range(int(4 * size8)):
            matrix[i + int(4 * size8), int(2 * size8)] = 1
            matrix[int(3 * size8), i] = 1
        for i in range(int(3 * size8)):
            matrix[i, int(2 * size8)] = 1
        for i in range(int(2 * size8)):
            matrix[int(size8), i] = 1
            matrix[int(3 * size8), i + int(6 * size8)] = 1
        for i in range(int(size8)):
            matrix[i + int(3 * size8), int(size8)] = 1
            matrix[int(5 * size8), i + int(4 * size8)] = 1
            matrix[i + int(5 * size8), int(5 * size8)] = 1
        self.matrix = matrix

    def to_image(self):
        return Image.fromarray(np.uint8(255 * (1 - self.matrix)), 'L')


def generate(gene: str, depth: int, mod: int, remainder: int, size: int, contrast: bool, frame: bool) -> Image:
    portrait = FrequencyPortrait(gene, depth, mod, remainder)
    portrait.resize(size)
    if contrast:
        portrait.add_contrast()
    if frame:
        portrait.add_frame()
    return portrait.to_image()


Alphabet = {"A", "C", "G", "T"}

Xletter = {"T": 0, "C": 0, "A": 1, "G": 1}
Yletter = {"T": 0, "C": 1, "A": 1, "G": 0}

'''
def fractal_portrait(gene, size: int) -> np.array:
    matrix = np.zeros((size, size))
    x = 1/2
    y = 1/2
    for k in range(len(gene)):
        x = (x + Xletter[gene[k]])/2
        y = (y + Yletter[gene[k]])/2
        matrix[min(size-1, int(size * x)), min(size-1, int(size * y))] = 1
    return matrix


def fractal_measure_portrait(gene, size:int) -> np.array:
    matrix = np.zeros((size, size))
    x = 1 / 2
    y = 1 / 2
    for k in range(len(gene)):
        x = (x + Xletter[gene[k]]) / 2
        y = (y + Yletter[gene[k]]) / 2
        matrix[min(size - 1, int(size * x)), min(size - 1, int(size * y))] += 1
    matrix *= 1/matrix.max()
    return matrix
'''
