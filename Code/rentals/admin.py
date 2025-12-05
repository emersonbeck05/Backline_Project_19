from django.contrib import admin
from .models import Instrument, Customer, Rental, RentalItem


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'category', 'status')
    search_fields = ('name', 'barcode', 'category')
    list_filter = ('status', 'category')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('last_name',)


class RentalItemInline(admin.TabularInline):
    model = RentalItem
    extra = 0


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'rental_date', 'returned', 'return_date', 'instruments_list')
    search_fields = ('customer__first_name', 'customer__last_name')
    list_filter = ('returned', 'rental_date')
    inlines = [RentalItemInline]

    # Custom display of all instruments in a rental
    def instruments_list(self, obj):
        items = RentalItem.objects.filter(rental=obj)
        return ", ".join(i.instrument.name for i in items)

    instruments_list.short_description = "Instruments"
