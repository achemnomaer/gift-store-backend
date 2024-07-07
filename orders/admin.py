import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import Order, OrderItem, Address



@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'created', 'updated']
    list_filter = ['created', 'updated']
   

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'price', 'quantity']
    extra = 0


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = 'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields(
    ) if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid', 'total_amount', 'status', 'created', ]
    list_filter = ['paid', 'status', 'created', 'updated']
    list_editable = ['paid', 'status']
    search_fields = ['id', 'user__username', 'user__email']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
