from django.contrib import admin
from .models import Building, Department, NearbyAtraction, DepartmenGalery
from recursos import AdminImageWidget


class GaleryInLine(admin.StackedInline):
    model = DepartmenGalery
    extra = 2
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'picture':
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(GaleryInLine,self).formfield_for_dbfield(db_field, **kwargs)

class AdminDepartment(admin.ModelAdmin):
    model = Department
    list_display      = ('id','building', 'number_of_apartment', 'type_department', 'bedrooms', 'bathrooms')
    inlines=[GaleryInLine,]
    ordering = ["building",]
    list_filter = ['building','bedrooms',]

class AtractionInLine(admin.StackedInline):
    model = NearbyAtraction
    extra = 2
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'picture':
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(AtractionInLine,self).formfield_for_dbfield(db_field, **kwargs)

class AdminBuilding(admin.ModelAdmin):
    model = Building
    list_display      = ('adress', 'location_description', 'building_apartments')
    inlines=[AtractionInLine,]
    ordering = ["adress",]

class AdminNearbyAtraction(admin.ModelAdmin):
    model = NearbyAtraction
    list_display      = ('id','titulo_img', 'building',)
    list_filter = ['building',]

admin.site.register(Building, AdminBuilding)
admin.site.register(Department, AdminDepartment)
admin.site.register(NearbyAtraction, AdminNearbyAtraction)
admin.site.register(DepartmenGalery)