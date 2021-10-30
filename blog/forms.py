from django import forms


class TextForm(forms.Form):
    mymail = forms.EmailField()
    mypass = forms.CharField()
    youmail = forms.EmailField(label='to-address')
    body = forms.CharField(label='text',widget=forms.Textarea,max_length=100)

class Text2Form(forms.Form):
    mymail = forms.EmailField()
    mypass = forms.CharField()

