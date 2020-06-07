from django.contrib import admin

# Register your models here.
from plants.models import Plant, Species, Fertilizer, Lighting, Shop, Spot


class PlantAdmin(admin.ModelAdmin):
    search_fields = ('species',)
    list_display = ('species',)

    # @staticmethod
    # def nlg_about_truncated(instance):
    #     return truncatechars(instance.nlg_about, 150)


class SpeciesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


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
