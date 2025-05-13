from django import forms

class ProductUploadForm(forms.Form):
    csv_file = forms.FileField(label="Select CSV File")
