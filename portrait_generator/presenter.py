from .models import FrequencyPortrait, UserFrequencyPortrait


def get_repository_database(user):
    portraits = UserFrequencyPortrait.objects.filter(user=user)
    images = []
    for userFP in portraits:
        images.append([userFP.portrait.portrait, str(userFP.portrait.mod), str(userFP.portrait.remainder),
                       userFP.generation_id])
    return images


def get_repository_cookies(cookies):
    images = []
    if 'num_saved_images' in cookies:
        num_saved_images = int(cookies['num_saved_images'])
        for i in range(num_saved_images):
            images.append(cookies['saved_image_' + str(i)].split(','))
    return images


def add_to_database(user, portraits):
    last = UserFrequencyPortrait.objects.latest('generation_id').generation_id
    last += 1
    for gene, mod, rem, depth, size, contrast, frame, portrait in portraits:
        fp = get_portrait(gene=gene, mod=mod, remainder=rem, depth=depth, size=size,
                          contrast=contrast, frame=frame)
        if fp is None:
            fp = FrequencyPortrait.objects.create(gene=gene, mod=mod, remainder=rem, depth=depth, size=size,
                                                  contrast=contrast, frame=frame, portrait=portrait)

        UserFrequencyPortrait.objects.create(user=user, portrait=fp, generation_id=last)


def add_to_cookies(cookies, portraits, response):
    if 'num_saved_images' in cookies:
        last = int(cookies['num_saved_images'])
    else:
        last = 0
    current = last
    for gene, mod, rem, depth, size, contrast, frame, portrait in portraits:
        response.set_cookie('saved_image_' + str(current), portrait + ',' + str(mod) + ',' + str(rem) + ',' + str(last))
        current += 1
    response.set_cookie('num_saved_images', str(current))


def get_portrait(gene, mod, remainder, depth, size, contrast, frame) -> FrequencyPortrait:
    return FrequencyPortrait.objects.filter(gene=gene, mod=mod, remainder=remainder, depth=depth,
                                                size=size, contrast=contrast, frame=frame).first()
