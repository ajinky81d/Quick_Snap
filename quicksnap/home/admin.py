from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from datetime import datetime
from .models import Data

class MonthFilter(admin.SimpleListFilter):
    title = _('Month')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        months = Data.objects.annotate(month=Count('date__month')).values_list('date__month', flat=True).distinct()
        choices = [(str(month), datetime(1900, month, 1).strftime('%B')) for month in months]
        return choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date__month=self.value())

class DataAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'detail')
    list_display_links = ['date', 'user', 'detail']
    list_filter = ('date', MonthFilter)
    search_fields = ['date']  

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            month = datetime.strptime(search_term, '%B').month
            queryset |= self.model.objects.filter(date__month=month)
        except ValueError:
            pass   
        return queryset, use_distinct

admin.site.register(Data, DataAdmin)