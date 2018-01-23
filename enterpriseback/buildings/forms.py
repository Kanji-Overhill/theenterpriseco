from django.forms import ModelForm
from buildings.models import Building, Department, NearbyAtraction

class BuildingForm(ModelForm):
    class Meta:
        model = Building
        fields = ['adress', 'picture', 'location_description']


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        