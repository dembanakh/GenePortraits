from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class GeneratorForm(forms.Form):
    gene_load_method = forms.ChoiceField(choices=(("T", "TERM"), ("U", "URL")))
    gene_term = forms.CharField(label='Gene', required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        'placeholder': "E.g. NC_003155.5:c6374929-6373649"
                                    })
                                )
    gene_url = forms.URLField(label='Gene', required=False)
    depth = forms.IntegerField(label='Depth', min_value=0, initial=3)
    mod = forms.IntegerField(label='Mod', min_value=1, initial=1)
    remainder = forms.IntegerField(label='Remainder', min_value=0, initial=0,
                                   widget=forms.NumberInput(
                                       attrs={
                                           'placeholder': "Must be <=Remainder"
                                       })
                                   )
    size = forms.IntegerField(label='Size', initial=256)
    contrast = forms.BooleanField(label='Contrast', required=False)
    frame = forms.BooleanField(label='Frame', required=False, initial=True)

    def clean_gene_term(self):
        method = self.cleaned_data['gene_load_method']
        gene = self.cleaned_data['gene_term']

        if method == "T":
            if len(gene) == 0:
                raise ValidationError(_('Empty term'))
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

        if mod < remainder:
            raise ValidationError(_('Remainder must be in range [0, Mod]'))

        return remainder
