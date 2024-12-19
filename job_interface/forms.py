from django import forms

class UrlScraperForm(forms.Form):
    url_list = forms.CharField(
        widget=forms.HiddenInput(attrs={
            "name": "url_list",
            "id": "url_list",
            "value": ""
        }),
        required=True
    )

class ContentScraperForm(forms.Form):
    url = forms.URLField(
        max_length=255,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter webScraping Url...",
            "id": "url",
            "name": "url"
            }),
        required=True
        )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Enter content...",
            "id": "content",
            "name": "content",
            "style": "height: 100px"
        }),
        required=True
        )
