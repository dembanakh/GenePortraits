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
                        .render({'num_generated_images': 1,
                                 'generated_images': generated_images}, request))
            else:
                depth, size, contrast, frame = data["depth"], data["size"], data["contrast"], data["frame"]
                generated_images = []
                for i in range(mod):
                    generated_images.append(generate_one_image(gene, depth, mod, i, size, contrast, frame))
                response = HttpResponse(
                    loader.get_template('portrait_generator/result.html')
                        .render({'num_generated_images': len(generated_images),
                                 'generated_images': generated_images}, request)
                )
            print(len(request.COOKIES['saved_images'].split(',')))
            if 'saved_images' not in request.COOKIES:
                response.set_cookie('saved_images', ','.join(generated_images))
            else:
                response.set_cookie('saved_images', request.COOKIES['saved_images'] + ',' + ','.join(generated_images))
            return response

    return Http404()


def repository(request):
    if request.method == 'POST':
        return Http404()

    images = []
    if 'saved_images' in request.COOKIES:
        images = request.COOKIES['saved_images'].split(',')

    print(len(images))

    return HttpResponse(loader.get_template('portrait_generator/repository.html').render({'images': images}, request))


def generate_one_image(gene, depth, mod, remainder, size, contrast, frame) -> str:
    image = generate(gene, depth, mod, remainder, size, contrast, frame)
    buffer = BytesIO()
    image.save(buffer, "PNG")
    image_str = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return image_str
