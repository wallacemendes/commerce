from django import forms

from .models import Comment, Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "initial_bid",
            "category",
            "description",
            "image_url",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "initial_bid": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "image_url": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                self.fields[field_name].label = f"{field.label} *"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text_content"]
        labels = {"text_content": "Leave your Comment here"}
        widgets = {
            "text_content": forms.Textarea(attrs={"class": "form-control"}),
        }
