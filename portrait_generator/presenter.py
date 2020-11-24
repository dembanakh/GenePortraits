from .models import FrequencyPortrait, UserFrequencyPortrait
from .generator import Alphabet
from .ncbi_api import NCBIAPI


def extract_gene(data: dict) -> (str, str):
    method = data['gene_load_method']
    if method == 'T':
        term_description = data['gene_term']
        parts = term_description.split(':')
        term = parts[0]
        gene_id = NCBIAPI.search(term)
        original = NCBIAPI.fetch(gene_id, parts[1] if len(parts) > 1 else None)
        code = ''.join(original.strip().split('\n')[1:])
        return term_description, ''.join(c for c in code.upper() if c in Alphabet)
    elif method == 'U':
        return '', ''
    raise ValueError('gene_load_method is not from the set {T, U}')


def get_repository_database(user):
    portraits = UserFrequencyPortrait.objects.filter(user=user)
    images = []
    for userFP in portraits:
        images.append([userFP.portrait.portrait, str(userFP.portrait.mod), str(userFP.portrait.remainder),
                       str(userFP.portrait.depth), str(userFP.portrait.size), userFP.generation_id])
    return images


def get_repository_cookies(cookies):
    images = []
    if 'num_saved_images' in cookies:
        num_saved_images = int(cookies['num_saved_images'])
        for i in range(num_saved_images):
            images.append(cookies['saved_image_' + str(i)].split(','))
    return images


def add_to_database(user, portraits):
    try:
        last = UserFrequencyPortrait.objects.latest('generation_id').generation_id + 1
    except UserFrequencyPortrait.DoesNotExist:
        last = 0

    for gene_id, mod, rem, depth, size, contrast, frame, portrait in portraits:
        fp = get_portrait(gene_id=gene_id, mod=mod, remainder=rem, depth=depth, size=size,
                          contrast=contrast, frame=frame)
        if fp is None:
            fp = FrequencyPortrait.objects.create(gene_id=gene_id, mod=mod, remainder=rem, depth=depth, size=size,
                                                  contrast=contrast, frame=frame, portrait=portrait)

        UserFrequencyPortrait.objects.create(user=user, portrait=fp, generation_id=last)


def add_to_cookies(cookies, portraits, response):
    if 'num_saved_images' in cookies:
        last = int(cookies['num_saved_images'])
    else:
        last = 0
    current = last
    for gene_id, mod, rem, depth, size, contrast, frame, portrait in portraits:
        response.set_cookie('saved_image_' + str(current), ','.join(map(str, [portrait, mod, rem, depth, size, last])))
        current += 1
    response.set_cookie('num_saved_images', str(current))


def get_portrait(gene_id, mod, remainder, depth, size, contrast, frame) -> FrequencyPortrait:
    return FrequencyPortrait.objects.filter(gene_id=gene_id, mod=mod, remainder=remainder, depth=depth,
                                            size=size, contrast=contrast, frame=frame).first()
