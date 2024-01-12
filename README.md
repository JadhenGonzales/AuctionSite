## Design Considerations

___

## Views

### Add post
<p> The add view is decorated with the atomic decorator. The add view does 2 model.save() back to back. The decorator ensures that if any of the database queries fail, the database is rolled back.

### Bid validation

<p>The Bid.save() method of the Bid model is modified so that you cannot add a bid that is smaller than the latest bid. This is done to make sure that even if an unwanted bid bypasses the form, it will still raise an error. 

### Bid and comment ModelForms

<p>The ModelForms for both models does not include the user and datetime in its fields. This makes sure that only the content and posting_id is gathered from the front-end and everything else is assigned at the back-end ensuring it cannot be tampered with.

## UI

### nav_filters
<p> A custom filter ``'navbar_item'|is_current:current_page`` is added to make sure that current pages are highlighted in the navbar.