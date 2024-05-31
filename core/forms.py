

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Item

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    preferred_colors = forms.MultipleChoiceField(
        choices=Item.COLOR_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text='Select preferred colors'
    )
    preferred_categories = forms.MultipleChoiceField(
        choices=Item.CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text='Select preferred categories'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                preferred_colors=','.join(self.cleaned_data['preferred_colors']),
                preferred_categories=','.join(self.cleaned_data['preferred_categories'])
            )
        return user


from django import forms

class UserInputForm(forms.Form):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    city = forms.CharField(label='City', max_length=100)
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES)
    temp_sensitivity = forms.IntegerField(label='Temperature Sensitivity', required=False)
    preferred_colors = forms.CharField(label='Preferred Colors', required=False)
