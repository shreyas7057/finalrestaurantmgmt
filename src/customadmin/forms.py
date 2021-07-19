from menu.models import Food

from django import forms

class AddFoodMenu(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

    