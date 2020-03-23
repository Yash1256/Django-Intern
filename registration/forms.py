from django.core.exceptions import ValidationError
from django.forms import ModelForm, fields
from .models import Author, User


class AuthorForm(ModelForm):
    password = fields.CharField(max_length=288, required=True)

    class Meta:
        model = Author
        exclude = ['added']

    def save(self, commit=True):
        if self.is_valid():
            try:
                u = User.objects.get(email=self.cleaned_data.get('email'))
                raise ValidationError('Author Already Exists')
            except User.DoesNotExist:
                u = User(email=self.cleaned_data.get('email'))
            u.set_password(self.cleaned_data.get('password'))
            u.save()
            super().save()
