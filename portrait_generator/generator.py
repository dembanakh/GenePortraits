import math
import numpy as np
from PIL import Image


def generate(gene: str, depth: int, mod: int, remainder: int, size: int, contrast: bool) -> Image:
    portrait = frequency_portrait(gene, depth, mod, remainder)
    portrait = resize(portrait, size)
    if contrast:
        portrait = contrast_portrait(portrait)
    image = image_from_portrait(portrait, size)
    return image


def extract_gene(data: dict) -> str:
    method = data['gene_load_method']
    if method == 'R':
        return data['gene_raw']
    elif method == 'F':
        pass
    elif method == 'U':
        pass
    raise ValueError('gene_load_method is not from the set {R, F, U}')


Alphabet = {"A", "C", "G", "T"}

Xletter = {"T": 0, "C": 0, "A": 1, "G": 1}
Yletter = {"T": 0, "C": 1, "A": 1, "G": 0}


def frequency_portrait(gene: str, depth: int, mod: int, remainder: int) -> np.array:
    m_matrix = np.zeros((2**depth, 2**depth))
    r_matrix = np.zeros((2**depth, 2**depth))

    for k in range(len(gene)-depth):
        ii = 0
        jj = 0
        for i in range(depth):
            ii += 2 ** (depth - i - 1) * Xletter[gene[k + i]]
            jj += 2 ** (depth - i - 1) * Yletter[gene[k + i]]
        m_matrix[ii, jj] += 1
        if k % mod == remainder:
            r_matrix[ii, jj] += 1
    if remainder == mod:
        r_matrix = m_matrix
    r_matrix *= 1/m_matrix.max()
    return r_matrix


def resize(portrait: np.array, size: int) -> np.array:
    portrait_length = len(portrait)
    matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            matrix[i, j] = portrait[int(portrait_length * i // size), int(portrait_length * j // size)]
    return matrix


def contrast_portrait(portrait: np.array) -> np.array:
    portrait_length = len(portrait)
    matrix = np.zeros((portrait_length, portrait_length))
    for i in range(portrait_length):
        for j in range(portrait_length):
            matrix[i, j] = math.sqrt(portrait[i, j])
    return matrix


def image_from_portrait(original: np.array, size: int) -> Image:
    portrait = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            portrait[i, j] = 255 * (1 - original[i, j])
    img = Image.fromarray(np.uint8(portrait), 'L')
    return img


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
def Ramka(portret):  # this function draws borders of codons on the Codon Table
    size=len(portret)
    port = portret
    siz = size/8
    for i in range(size):
        port[i,0]=1
        port[0,i]=1
        port[size-1,i]=1
        port[i,size-1]=1
        port[int(2*siz),i]=1
        port[int(4*siz),i]=1
        port[int(6*siz),i]=1
        port[i,int(4*siz)]=1
        port[i,int(6*siz)]=1
    for i in range(int(6*siz)):
        port[int(7*siz),i+int(2*siz)]=1
    for i in range(int(4*siz)):
        port[i+int(4*siz),int(2*siz)]=1
        port[int(3*siz),i]=1
    for i in range(int(3*siz)):
        port[i,int(2*siz)]=1
    for i in range(int(2*siz)):
        port[int(siz),i]=1
        port[int(3*siz),i+int(6*siz)]=1
    for i in range(int(siz)):
        port[i+int(3*siz),int(siz)]=1
        port[int(5*siz),i+int(4*siz)]=1
        port[i+int(5*siz),int(5*siz)]=1
    return port

def Resize(portrait,size):
    l=len(portrait)
    matrix=np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            matrix[i,j]=portrait[int(l*i//size),int(l*j//size)]
    return matrix

def FrequencyPortrait(w,depth,mod,remainder):

    mmatrix = np.zeros((2**depth,2**depth))
    rmatrix = np.zeros((2**depth,2**depth))

    for k in range(len(w)-depth):
        ii = 0
        jj = 0
        for i in range(depth):
            ii += 2 ** (depth - i - 1) * Xletter[w[k + i]]
            jj += 2 ** (depth - i - 1) * Yletter[w[k + i]]
        mmatrix[ii, jj] += 1
        if k % mod == remainder:
            rmatrix[ii, jj] += 1
    if remainder==mod:
        rmatrix=mmatrix
    rmatrix*=1/mmatrix.max()
    return rmatrix

def ContrastPortrait(portrait):
    l=len(portrait)
    matrix=np.zeros((l,l))
    for i in range(l):
        for j in range(l):
            matrix[i,j]=math.sqrt(portrait[i,j])
    return matrix


def ImageFromPortrait(portrait):
    l=len(portrait)
    port = np.zeros((size,size))
    for i in range(size):
        for j in range(size):
           port[i, j] = 255 * (1 - portrait[i,j])
    img = Image.fromarray(np.uint8(port), 'L')
    return img

def FractalPortrait(w,size):
    matrix = np.zeros((size,size))
    x=1/2
    y=1/2
    for k in range(len(w)):
        x=(x+Xletter[w[k]])/2
        y=(y+Yletter[w[k]])/2
        matrix[min(size-1,int(size*x)),min(size-1,int(size*y))]=1
    return matrix

def FractalMeasurePortrait(w,size):
    matrix = np.zeros((size, size))
    x = 1 / 2
    y = 1 / 2
    for k in range(len(w)):
        x = (x + Xletter[w[k]]) / 2
        y = (y + Yletter[w[k]]) / 2
        matrix[min(size - 1, int(size * x)), min(size - 1, int(size * y))] += 1
    matrix*=1/matrix.max()
    return matrix




vyd = "adpA_avermitilis"
# vyd = "adpA_cattleya"
# vyd = "adpA_J1074"
# vyd = "adpA_thermoautotrophicusH1"
# vyd = "rbcL_agrobacterium"
# vyd = "rbcL_euglena"
# vyd = "rbcL_fischerella"
# vyd = "rbcL_nodularia"
# vyd = "rbcL_geranium"
# vyd = "rbcL_oryza"
# vyd = "rbcL_pinus"
# vyd = "rbcL_triticum"
# vyd="E_coli_K12_whole_genome"
# vyd="albidoflavusJ1074_whole_genome"
# vyd="ATCC21113_genome"
# vyd="ATCC10595_genome"
# vyd="lan_cluster"
# vyd = "Lan23646-24228-R"
# vyd = "GspB"
# vyd = "mycoplasma"
# vyd = "Plasmodium"
#vyd="COVID19"

code = open(vyd + ".txt", "r")
line = code.readline()
data = code.read().replace(line, '').replace('\n', '')
code.close()
data = data.upper()

w = ''
for char in data:
    if char in Alphabet:
        w += char


depth = 3
mod = 3
size = 128
contrast = True
ramka = True
show = True
write = False
file_name = vyd + '.bmp'

for r in range(mod + 1):
    port = FrequencyPortrait(w, depth, mod, r)
    port = Resize(port, size)
    if contrast:
        port = ContrastPortrait(port)
    if ramka:
        port = Ramka(port)
    img = ImageFromPortrait(port)
    if show:
        img.show()
    if write:
        file_name = vyd + str(depth)+str(r)+'.bmp'
        img.save(file_name, "bmp")
        print('Saving the image to:' + file_name)
'''
