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
                return HttpResponse(
                    loader.get_template('portrait_generator/result.html')
                        .render({'num_generated_images': 1,
                                 'generated_images': [generate_one_image(gene, data["depth"],
                                                                         data["mod"], data["remainder"],
                                                                         data["size"], data["contrast"],
                                                                         data["frame"])]}, request))
            else:
                depth, size, contrast, frame = data["depth"], data["size"], data["contrast"], data["frame"]
                images = []
                for i in range(mod):
                    images.append(generate_one_image(gene, depth, mod, i, size, contrast, frame))
                return HttpResponse(
                    loader.get_template('portrait_generator/result.html')
                        .render({'num_generated_images': len(images),
                                 'generated_images': images}, request)
                )

    return Http404()


def generate_one_image(gene, depth, mod, remainder, size, contrast, frame) -> str:
    image = generate(gene, depth, mod, remainder, size, contrast, frame)
    buffer = BytesIO()
    image.save(buffer, "PNG")
    image_str = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return image_str
