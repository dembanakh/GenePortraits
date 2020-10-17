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
        form = GeneratorForm(request.POST)
        if form.is_valid():
            data: dict = form.cleaned_data
            gene = extract_gene(data, request.FILES)
            image = generate(gene, data["depth"], data["mod"], data["remainder"],
                             data["size"], data["contrast"])
            buffer = BytesIO()
            image.save(buffer, "PNG")
            image_str = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            return HttpResponse(
                loader.get_template('portrait_generator/result.html').render({'generated_image': image_str},
                                                                             request))
    return Http404()
