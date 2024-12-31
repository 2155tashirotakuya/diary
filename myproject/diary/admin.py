from django.contrib import admin
from .models import Page

# admin.site.register(Page)
# デコレータをつける
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    # 読み取り専用のフィールドとして設定
    readonly_fields = ["id", "created_at", "updated_at"]
