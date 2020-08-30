from django.contrib import admin
from django.forms import ModelForm

from plants.models import Plant, Species, Fertilizer, Lighting, Shop, Spot, Watering, Room

admin.site.disable_action('delete_selected')


class AlwaysChangedModelForm(ModelForm):
    def has_changed(self):
        """ Should returns True if data differs from initial.
        By always returning true even unchanged inlines will get validated and saved."""
        return True


class WaterInline(admin.TabularInline):
    model = Watering
    extra = 0
    form = AlwaysChangedModelForm


def water(PlantAdmin, request, queryset):
    watering_objects = [Watering(plant=plant) for plant in queryset]
    Watering.objects.bulk_create(watering_objects)


water.short_description = 'Water selected plants'


class PlantAdmin(admin.ModelAdmin):
    search_fields = ('display_name', 'species__name', 'spot__name', 'spot__room__name')
    inlines = [WaterInline]
    actions = [water]


class SpeciesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'count')

    @staticmethod
    def count(instance):
        return instance.plant_set.count()


class FertilizerAdmin(admin.ModelAdmin):
    list_display = ('description',)


class LightingAdmin(admin.ModelAdmin):
    list_display = ('description',)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SpotAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Plant, PlantAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Fertilizer, FertilizerAdmin)
admin.site.register(Lighting, LightingAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Spot, SpotAdmin)
admin.site.register(Room, RoomAdmin)
