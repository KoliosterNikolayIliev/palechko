from django import forms


from items.models import Item


class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Item
        fields = ('type', 'category', 'name', 'description', 'image', 'user')

        widgets = {'image': forms.FileInput(
            attrs={'style': 'display: none;', 'class': 'form-control', 'required': False, }
        )}


#
class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control rounded-2', }))


class FilterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Item
        fields = ('category',)
