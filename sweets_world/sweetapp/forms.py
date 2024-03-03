from django import forms
from .models import Profile, CustomUser

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'profile_pic', 'city', 'state', 'country']
    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-contol'
    

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile']

    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-contol'




from django import forms
from category.models import products

class DateForm(forms.Form):
    salesdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Select a date'
    )

class image_form(forms.ModelForm):
    class Meta:
      model=products
      fields=('prod_image',)



