from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        help_text="Пароль має містити не менше 8 символів, включаючи цифри та літери."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Підтвердіть пароль"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Паролі не співпадають.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError("Цей емейл вже зареєстровано.")

        return email


class UserChangeProfile(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        help_text="Введіть ім'я",
        initial='',
    )
    email = forms.EmailField(
        help_text="Введіть електронну адресу",
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        help_text="Введіть прізвище",
    )
    user_phone = forms.CharField(
        max_length=15,
        required=False,
        help_text="Введіть номер телефону",
    )

    class Meta:
        model = User
        fields = ['first_name', 'email', 'last_name', 'user_phone']
