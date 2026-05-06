from django import forms
from UserApp.models import User

class UserAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-black outline-none transition',
        'placeholder': 'Enter password'
    }), required=False)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'mobile', 'city', 'profile_pic', 'is_active', 'is_verified', 'is_staff']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-black outline-none transition',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-black outline-none transition',
                'placeholder': 'Email Address'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-black outline-none transition',
                'placeholder': 'Mobile Number'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-black outline-none transition',
                'placeholder': 'City'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-black border-gray-300 rounded focus:ring-black'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-black border-gray-300 rounded focus:ring-black'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-black border-gray-300 rounded focus:ring-black'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['password'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
