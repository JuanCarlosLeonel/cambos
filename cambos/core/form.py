from django import forms
from .models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import Permission

class UserCreationForm(forms.ModelForm):
    
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}))        

    class Meta:
        model = User
        fields = (
            "username",
            'setor'           
        )
    
        widgets = {                         
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'setor': forms.Select(attrs={'class':'form-control'}),
        } 
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
