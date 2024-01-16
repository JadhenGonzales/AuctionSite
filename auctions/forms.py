from django import forms

from .models import Bid, Category, Comment

class AddForm(forms.Form):
    # For Adding postings
    item_name = forms.CharField(
        label="Item name",
        max_length=64,
        widget=forms.TextInput(attrs={"class": "form-control border border-dark"}),
        )
    
    item_categories = forms.ModelMultipleChoiceField(
        Category.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select border border-dark"}),
    )

    item_description = forms.CharField(
        label="Description",
        max_length=500,
        widget=forms.Textarea(attrs={"class": "form-control border border-dark", "rows": 10}),
        )
    
    item_img = forms.CharField(
        label="Image URL",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control  border border-dark"}),
        )
    
    initial_bid = forms.IntegerField(
        label="Initial Bid",
        widget=forms.NumberInput(attrs={"class": "form-control  border border-dark"}),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content",]

        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control border border-dark mb-2",
                "placeholder": "Add a comment.",
                "rows": 4,
            })
        }

        labels = {"content": ""}


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount",]

        widgets = {
            "amount": forms.NumberInput(attrs={
                "class": "form-control border border-dark",
                "placeholder": "Enter bid amount.",
            })
        }

        labels = {"amount": ""}