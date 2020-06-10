from django.contrib import admin

from plants.models import Plant, Species, Fertilizer, Lighting, Shop, Spot, Watering


class WaterInline(admin.TabularInline):
    model = Watering
    extra = 0


class PlantAdmin(admin.ModelAdmin):
    search_fields = ('species',)
    inlines = [WaterInline]


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


admin.site.register(Plant, PlantAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Fertilizer, FertilizerAdmin)
admin.site.register(Lighting, LightingAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Spot, SpotAdmin)
