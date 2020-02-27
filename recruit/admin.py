from django.contrib import admin
from .models import Recruit, ShadowHandTest, ShadowHandQuestion


@admin.register(Recruit)
class RecruitAdmin(admin.ModelAdmin):
    oredering = ('name', 'planet', 'age',)
    search_fields = ('name', )
    list_display = ('name', 'planet', 'age', 'email', 'created_at', )

class ShadowHandQuestionInLine(admin.TabularInline):
    model = ShadowHandQuestion
    extra = 1
    min_num = 1

@admin.register(ShadowHandTest)
class ShadowHandTestAdmin(admin.ModelAdmin):
    oredering = ('order_code', 'created_at',)
    list_display = ('order_code', 'created_at',)
    
    inlines = [
        ShadowHandQuestionInLine
    ]
