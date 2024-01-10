## Design Considerations

___

### Bid validation

<p>The Bid.save() method of the Bid model is modified so that you cannot add a bid that is smaller than the latest bid. This is done to make sure that even if an unwanted bid bypasses the form, it will still raise an error. 

### Bid and comment ModelForms

<p>The ModelForms for both models does not include the posting, user, and datetime in its fields. This makes sure that only the content is gathered from the front-end and everything else is assigned at the back-end ensuring it cannot be tampered with.