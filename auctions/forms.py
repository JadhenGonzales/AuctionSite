from django import forms

class AddForm(forms.Form):

    item_name = forms.CharField(
        label="Item name",
        max_length=64
        )
    
    item_description = forms.CharField(
        label="Description",
        widget=forms.Textarea,
        max_length=500
        )
    
    item_img = forms.CharField(
        label="Image URL",
        required=False,
        max_length=100
        )
    
    initial_bid = forms.IntegerField(
        label="Initial Bid",
    )