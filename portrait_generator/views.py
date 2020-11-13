import base64
from io import BytesIO

from django.http import HttpResponse, Http404
from django.template import loader

from .forms import GeneratorForm
from .generator import generate, extract_gene
from .presenter import get_repository_cookies, get_repository_database, add_to_cookies, add_to_database, get_portrait


def index(request):
    if request.method == 'POST':
        return Http404()
    else:
        form = GeneratorForm()

    return HttpResponse(loader.get_template('portrait_generator/index.html').render({'form': form}, request))


def result(request):
    if request.method == 'POST':
        form = GeneratorForm(request.POST, request.FILES)
        if form.is_valid():
            data: dict = form.cleaned_data
            gene = extract_gene(data, request.FILES)
            mod, rem = data["mod"], data["remainder"]
            depth, size, contrast, frame = data["depth"], data["size"], data["contrast"], data["frame"]
            if mod > rem:
                generated_images = [(gene, mod, rem, depth, size, contrast, frame,
                                     generate_one_image(gene, depth, mod, rem, size, contrast, frame))]
                response = HttpResponse(
                    loader.get_template('portrait_generator/result.html')
                        .render({'gene_10': None, 'generated_images': generated_images,
                                 'gene': gene, 'depth': data["depth"], 'size': data["size"]}, request))
            else:
                generated_images = []
                for i in range(mod):
                    generated_images.append((gene, mod, i, depth, size, contrast, frame,
                                             generate_one_image(gene, depth, mod, i, size, contrast, frame)))
                response = HttpResponse(
                    loader.get_template('portrait_generator/result.html')
                        .render({'gene_10': generate_one_image(gene, depth, 1, 0, size, contrast, frame),
                                 'generated_images': generated_images,
                                 'gene': gene, 'depth': depth, 'size': size}, request)
                )
            if request.user.is_authenticated:
                add_to_database(request.user, generated_images)
            else:
                add_to_cookies(request.COOKIES, generated_images, response)
            return response

    return Http404()


def repository(request):
    if request.method == 'POST':
        return Http404()

    if request.user.is_authenticated:
        images = get_repository_database(request.user)
    else:
        images = get_repository_cookies(request.COOKIES)

    return HttpResponse(loader.get_template('portrait_generator/repository.html').render({'images': images}, request))


def generate_one_image(gene, depth, mod, remainder, size, contrast, frame) -> str:
    portrait = get_portrait(gene, depth, mod, remainder, size, contrast, frame)
    if portrait is None:
        image = generate(gene, depth, mod, remainder, size, contrast, frame)
        buffer = BytesIO()
        image.save(buffer, "PNG")
        image_str = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
    else:
        image_str = portrait.portrait
    return image_str
