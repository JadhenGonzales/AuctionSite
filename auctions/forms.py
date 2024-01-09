from django import forms

from .models import Category

class AddForm(forms.Form):
    # For Adding postings
    item_name = forms.CharField(
        label="Item name",
        max_length=64
        )
    
    item_categories = forms.ModelMultipleChoiceField(
        Category.objects.all(),
    )

    item_description = forms.CharField(
        label="Description",
        widget=forms.Textarea(),
        max_length=500
        )
    
    item_img = forms.CharField(
        label="Image URL",
        required=False,
        max_length=100,
        )
    
    initial_bid = forms.IntegerField(
        label="Initial Bid",
    )


class CommentForm:
    content = forms.CharField(
        widget=forms.Textarea(),
        label="Comment",
        max_length=200,
    )


class BidForm:
    amount = forms.IntegerField(
        label="Bid",
    )