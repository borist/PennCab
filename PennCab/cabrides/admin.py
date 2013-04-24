from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from cabrides.models import CabUser, Ride

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CabUser
        fields = ('first_name', 'last_name', 'phone_number', 'email')

    def clean_password2(self):
        # Check that the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CabUser

    def clean_password(self):
        return self.initial["password"]


# Cr
class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('first_name', 'last_name', 'phone_number', 'email')

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'phone_number', 'email', 'password')}),
    )

    add_fieldsets = (
        (None, {
        'fields': ('first_name', 'last_name', 'phone_number', 
            'email', 'password1', 'password2')}),
    )

    search_fields = ('email',)
    filter_horizontal = ()


admin.site.register(CabUser)
admin.site.register(Ride)
admin.site.unregister(Group)
