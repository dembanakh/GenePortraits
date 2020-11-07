from typing import Tuple

import base64
from io import BytesIO

from django.http import HttpResponse, Http404
from django.template import loader

from .forms import GeneratorForm
from .generator import generate, extract_gene


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
            if mod > rem:
                generated_images = [generate_one_image(gene, data["depth"],
                                                       data["mod"], data["remainder"],
                                                       data["size"], data["contrast"],
                                                       data["frame"])]
                response = HttpResponse(
                    loader.get_template('portrait_generator/result.html')
                        .render({'gene_10': None, 'generated_images': generated_images,
                                 'gene': gene, 'depth': data["depth"], 'size': data["size"]}, request))
            else:
                depth, size, contrast, frame = data["depth"], data["size"], data["contrast"], data["frame"]
                generated_images = []
                for i in range(mod):
                    generated_images.append(generate_one_image(gene, depth, mod, i, size, contrast, frame))
                response = HttpResponse(
                    loader.get_template('portrait_generator/result.html')
                        .render({'gene_10': generate_one_image(gene, depth, 1, 0, size, contrast, frame)[0],
                                 'generated_images': generated_images,
                                 'gene': gene, 'depth': data["depth"], 'size': data["size"]}, request)
                )
            if 'num_saved_images' in request.COOKIES:
                last = int(request.COOKIES['num_saved_images'])
            else:
                last = 0
            for img in generated_images:
                response.set_cookie('saved_image_' + str(last), img)
                last += 1
            response.set_cookie('num_saved_images', str(last))
            return response

    return Http404()


def repository(request):
    if request.method == 'POST':
        return Http404()

    images = []
    if 'num_saved_images' in request.COOKIES:
        num_saved_images = int(request.COOKIES['num_saved_images'])
        for i in range(num_saved_images):
            images.append(request.COOKIES['saved_image_' + str(i)])

    return HttpResponse(loader.get_template('portrait_generator/repository.html').render({'images': images}, request))


def generate_one_image(gene, depth, mod, remainder, size, contrast, frame) -> Tuple[str, int, int]:
    image = generate(gene, depth, mod, remainder, size, contrast, frame)
    buffer = BytesIO()
    image.save(buffer, "PNG")
    image_str = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return image_str, mod, remainder
