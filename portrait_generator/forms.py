from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class GeneratorForm(forms.Form):
    gene_load_method = forms.ChoiceField(choices=(("R", "RAW INPUT"), ("F", "FILE"), ("U", "URL")))
    gene_raw = forms.CharField(label='Gene', required=False)
    gene_file = forms.FileField(label='Gene', required=False)
    gene_url = forms.URLField(label='Gene', required=False)
    depth = forms.IntegerField(label='Depth', min_value=0)
    mod = forms.IntegerField(label='Mod', min_value=1, initial=1)
    remainder = forms.IntegerField(label='Remainder', min_value=0, initial=0)
    size = forms.IntegerField(label='Size', initial=256)
    contrast = forms.BooleanField(label='Contrast', required=False)
    frame = forms.BooleanField(label='Frame', required=False)

    def clean_gene_raw(self):
        method = self.cleaned_data['gene_load_method']
        gene = self.cleaned_data['gene_raw']

        if method == "R":
            if len(gene) == 0:
                raise ValidationError(_('Empty gene'))
        return gene

    def clean_gene_file(self):
        method = self.cleaned_data['gene_load_method']
        gene = self.cleaned_data['gene_file']

        if method == "F":
            if gene is None:
                raise ValidationError(_('Empty gene'))
        return gene

    def clean_gene_url(self):
        method = self.cleaned_data['gene_load_method']
        gene = self.cleaned_data['gene_url']

        if method == "U":
            if len(gene) == 0:
                raise ValidationError(_('Empty gene'))
        return gene

    def clean_remainder(self):
        remainder = self.cleaned_data['remainder']
        mod = self.cleaned_data['mod']

        if mod > remainder:
            raise ValidationError(_('Remainder must be in range [0, Mod]'))

        return remainder
