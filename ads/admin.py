from django.contrib import admin

from ads.models import Ads, Review


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "description", "author", "created_at")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "ad")
