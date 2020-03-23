from django.forms import forms, fields
from .models import Post


class PostForm(forms.Form):
    title = fields.CharField(max_length=255, required=True)
    description = fields.CharField(max_length=500, required=True)
    content = fields.TextInput()
    date = fields.DateField(required=True)

    def save(self, author):
        if self.is_valid():
            post = Post(author_id=author.pk, **self.cleaned_data)
            post.full_clean()
            post.save()
