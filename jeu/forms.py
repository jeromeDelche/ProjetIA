from django import forms
from django.contrib.auth.models import User

class ConnexionForm(forms.Form) :
	username = forms.CharField(max_length = 30 , label = "Nom d'utilisateur")
	password = forms.CharField(max_length = 100, label = "Mot de passe", widget = forms.PasswordInput)

	def clean(self) :
		cleaned_data = super(ConnexionForm, self).clean()
		if not User.objects.filter(username=self.cleaned_data['username']).exists() or User.objects.get(username=self.cleaned_data['username']).check_password(cleaned_data['password']) :
			raise forms.ValidationError("Nom de compte ou mot de passe incorrecte")
		return cleaned_data

class RegisterForm(forms.Form) :
	username = forms.CharField(max_length = 30 , label = "Nom d'utilisateur")
	password = forms.CharField(max_length = 100, label = "Mot de passe", widget = forms.PasswordInput)
	passwordConfirmation = forms.CharField(max_length = 100, label = "confirmer le mot de passe", widget = forms.PasswordInput)
	email = forms.EmailField(label = "Adresse E-Mail")
	nickname = forms.CharField(max_length = 30 , label = "Pseudo")

	def clean_username(self) : 
		if User.objects.filter(username=self.cleaned_data['username']).exists() :
			raise forms.ValidationError("Nom de compte déjà existant.")
		return self.cleaned_data['username']

	def clean_email(self) : 
		if User.objects.filter(email=self.cleaned_data['email']).exists() :
			raise forms.ValidationError("E-mail déjà existant.")
		return self.cleaned_data['email']

	def clean(self) :
		cleaned_data = super(RegisterForm, self).clean()
		if cleaned_data.get('password') != cleaned_data.get('passwordConfirmation') :
			self.add_error("password", "Mots de passes non identique")
		return cleaned_data


