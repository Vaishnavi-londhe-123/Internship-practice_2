from django import forms
from django.contrib.auth.models import User, Group
from .models import Contract

class CustomUserForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(), 
        required=False, 
        label="Assign Role",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        required=False, 
        label="Password"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Contract Form
class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['contract_name', 'description', 'status', 'file']
        widgets = {
            'contract_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contract Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Description'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }