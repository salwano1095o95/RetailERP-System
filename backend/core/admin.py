from django.contrib import admin
from .models import (
    UserProfile, Supplier, Customer, Product,
    PurchaseOrder, PurchaseItem, SalesOrder, SalesItem, StockMovement
)


# =============================================================================
# تسجيل نموذج ملف المستخدم (UserProfile)
# =============================================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'created_at']
    list_filter = ['role', 'is_active']
    search_fields = ['user__username', 'user__email', 'phone']
    ordering = ['-created_at']
    verbose_name = 'ملف المستخدم'
    verbose_name_plural = 'ملفات المستخدمين'


# =============================================================================
# تسجيل نموذج الموردين (Supplier)
# =============================================================================

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'balance', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'phone', 'email']
    ordering = ['name']
    verbose_name = 'مورد'
    verbose_name_plural = 'الموردين'


# =============================================================================
# تسجيل نموذج العملاء (Customer)
# =============================================================================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'debt', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'phone', 'email']
    ordering = ['name']
    verbose_name = 'عميل'
    verbose_name_plural = 'العملاء'


# =============================================================================
# تسجيل نموذج الأصناف (Product)
# =============================================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'barcode', 'name', 'category', 'purchase_price', 
        'selling_price', 'stock_quantity', 'alert_threshold', 
        'is_low_stock', 'is_active'
    ]
    list_filter = ['is_active', 'category', 'supplier']
    search_fields = ['barcode', 'name', 'description']
    ordering = ['name']
    readonly_fields = ['profit_margin', 'is_low_stock']
    verbose_name = 'صنف'
    verbose_name_plural = 'الأصناف'
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('barcode', 'name', 'description', 'category')
        }),
        ('الأسعار', {
            'fields': ('purchase_price', 'selling_price', 'profit_margin')
        }),
        ('المخزن', {
            'fields': ('stock_quantity', 'alert_threshold', 'min_order_quantity', 'is_low_stock')
        }),
        ('المورد', {
            'fields': ('supplier',)
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
    )


# =============================================================================
# تسجيل نموذج فواتير الشراء (PurchaseOrder)
# =============================================================================

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    verbose_name = 'عنصر شراء'
    verbose_name_plural = 'عناصر الشراء'


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'supplier', 'status', 'total_amount', 
        'paid_amount', 'remaining_amount', 'order_date', 'created_by'
    ]
    list_filter = ['status', 'order_date']
    search_fields = ['order_number', 'supplier__name']
    ordering = ['-order_date']
    readonly_fields = ['total_amount', 'remaining_amount', 'is_paid']
    inlines = [PurchaseItemInline]
    verbose_name = 'فاتورة شراء'
    verbose_name_plural = 'فواتير الشراء'
    
    fieldsets = (
        ('معلومات الفاتورة', {
            'fields': ('order_number', 'supplier', 'status')
        }),
        ('المبالغ', {
            'fields': ('total_amount', 'paid_amount', 'discount', 'remaining_amount', 'is_paid')
        }),
        ('تواريخ', {
            'fields': ('order_date', 'received_date')
        }),
        ('معلومات إضافية', {
            'fields': ('notes', 'created_by'),
            'classes': ('collapse',)
        }),
    )


# =============================================================================
# تسجيل نموذج عناصر فاتورة الشراء (PurchaseItem)
# =============================================================================

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'product', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['purchase_order__status']
    search_fields = ['product__name', 'purchase_order__order_number']
    verbose_name = 'عنصر شراء'
    verbose_name_plural = 'عناصر الشراء'


# =============================================================================
# تسجيل نموذج فواتير البيع (SalesOrder)
# =============================================================================

class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 1
    verbose_name = 'عنصر بيع'
    verbose_name_plural = 'عناصر البيع'


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'customer', 'status', 'payment_status',
        'total_amount', 'paid_amount', 'remaining_amount', 
        'order_date', 'created_by'
    ]
    list_filter = ['status', 'payment_status', 'order_date']
    search_fields = ['order_number', 'customer__name']
    ordering = ['-order_date']
    readonly_fields = ['total_amount', 'remaining_amount', 'is_paid', 'profit']
    inlines = [SalesItemInline]
    verbose_name = 'فاتورة بيع'
    verbose_name_plural = 'فواتير البيع'
    
    fieldsets = (
        ('معلومات الفاتورة', {
            'fields': ('order_number', 'customer', 'status', 'payment_status')
        }),
        ('المبالغ', {
            'fields': ('total_amount', 'paid_amount', 'discount', 'tax', 'remaining_amount', 'is_paid')
        }),
        ('الربح', {
            'fields': ('profit',),
            'classes': ('collapse',)
        }),
        ('تواريخ', {
            'fields': ('order_date',)
        }),
        ('معلومات إضافية', {
            'fields': ('notes', 'created_by'),
            'classes': ('collapse',)
        }),
    )


# =============================================================================
# تسجيل نموذج عناصر فاتورة البيع (SalesItem)
# =============================================================================

@admin.register(SalesItem)
class SalesItemAdmin(admin.ModelAdmin):
    list_display = ['sales_order', 'product', 'quantity', 'unit_price', 'subtotal', 'profit']
    list_filter = ['sales_order__status']
    search_fields = ['product__name', 'sales_order__order_number']
    verbose_name = 'عنصر بيع'
    verbose_name_plural = 'عناصر البيع'


# =============================================================================
# تسجيل نموذج حركات المخزن (StockMovement)
# =============================================================================

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'movement_type', 'quantity', 
        'reference_type', 'reference_id', 'created_by', 'created_at'
    ]
    list_filter = ['movement_type', 'created_at']
    search_fields = ['product__name', 'reference_id']
    ordering = ['-created_at']
    verbose_name = 'حركة مخزن'
    verbose_name_plural = 'حركات المخزن'
