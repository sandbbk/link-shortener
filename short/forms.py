from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class User_Creation_Form(UserCreationForm):
    email = models.EmailField(blank=False, null=False)

    def __init__(self, *args, **kwargs):
        super(User_Creation_Form, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
