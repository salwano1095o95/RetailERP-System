from django.db import models
from django.utils import timezone


# =============================================================================
# نموذج التصنيف (Category)
# =============================================================================

class Category(models.Model):
    """
    نموذج لتخزين تصنيفات المنتجات
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='اسم التصنيف')
    description = models.TextField(blank=True, null=True, verbose_name='وصف التصنيف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ آخر تحديث')
    
    class Meta:
        verbose_name = 'تصنيف'
        verbose_name_plural = 'التصنيفات'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Supplier(models.Model):
    """
    نموذج المورد
    """
    name = models.CharField(max_length=200, verbose_name="اسم المورد")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الهاتف")
    balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00, 
        verbose_name="الرصيد"
    )
    address = models.TextField(blank=True, null=True, verbose_name="العنوان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "مورد"
        verbose_name_plural = "الموردين"

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    نموذج العميل
    """
    name = models.CharField(max_length=200, verbose_name="اسم العميل")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الهاتف")
    debt = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00, 
        verbose_name="الدين"
    )
    address = models.TextField(blank=True, null=True, verbose_name="العنوان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"

    def __str__(self):
        return self.name


# =============================================================================
# نموذج المنتج (Product)
# =============================================================================

class Product(models.Model):
    """
    نموذج لتخزين بيانات المنتجات والأصناف
    """
    barcode = models.CharField(max_length=50, unique=True, verbose_name='الباركود')
    name = models.CharField(max_length=200, verbose_name='اسم المنتج')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='products', verbose_name='التصنيف')
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='سعر الشراء')
    selling_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='سعر البيع')
    quantity = models.IntegerField(default=0, verbose_name='الكمية')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ آخر تحديث')
    
    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['name']
        indexes = [
            models.Index(fields=['barcode']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.barcode})"


# =============================================================================
# نموذج فاتورة البيع (SalesOrder)
# =============================================================================

class SalesOrder(models.Model):
    """
    نموذج فاتورة البيع (الرأس)
    يمثل عملية بيع لعميل معين تحتوي على معلومات عامة عن الفاتورة
    """
    PAYMENT_METHODS = [
        ('cash', 'نقدي'),
        ('card', 'بطاقة ائتمان'),
        ('bank_transfer', 'تحويل بنكي'),
        ('credit', 'آجل/دين'),
    ]
    
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='sales_orders',
        verbose_name="العميل"
    )
    order_date = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الفاتورة")
    total_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0.00, 
        verbose_name="الإجمالي"
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHODS, 
        default='cash',
        verbose_name="طريقة الدفع"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")
    is_paid = models.BooleanField(default=False, verbose_name="تم الدفع")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "فاتورة بيع"
        verbose_name_plural = "فواتير المبيعات"
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['order_date']),
            models.Index(fields=['customer']),
        ]

    def __str__(self):
        return f"فاتورة #{self.id} - {self.customer.name if self.customer else 'عميل عام'} ({self.order_date.strftime('%Y-%m-%d')})"


# =============================================================================
# نموذج تفاصيل فاتورة البيع (SalesItem)
# =============================================================================

class SalesItem(models.Model):
    """
    نموذج تفاصيل فاتورة البيع (الأصناف)
    يمثل كل صنف داخل فاتورة البيع، ويربط المنتج بالفاتورة مع الكمية والسعر
    """
    order = models.ForeignKey(
        SalesOrder, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="الفاتورة"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT, 
        related_name='sales_items',
        verbose_name="المنتج"
    )
    quantity = models.PositiveIntegerField(verbose_name="الكمية المباعة")
    price = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name="سعر الوحدة"
    )
    subtotal = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name="المجموع الجزئي"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "صنف مباع"
        verbose_name_plural = "أصناف المبيعات"
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} في فاتورة #{self.order.id}"

    def save(self, *args, **kwargs):
        """
        حساب المجموع الجزئي تلقائياً قبل الحفظ
        """
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)


# =============================================================================
# نموذج فاتورة الشراء (PurchaseOrder)
# =============================================================================

class PurchaseOrder(models.Model):
    """
    نموذج فاتورة الشراء (الرأس)
    يمثل عملية شراء من مورد معين تحتوي على معلومات عامة عن الفاتورة
    """
    PAYMENT_STATUS = [
        ('pending', 'قيد الانتظار'),
        ('partial', 'مدفوع جزئياً'),
        ('paid', 'مدفوع بالكامل'),
    ]
    
    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='purchase_orders',
        verbose_name="المورد"
    )
    order_date = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الفاتورة")
    total_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0.00, 
        verbose_name="الإجمالي"
    )
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS, 
        default='pending',
        verbose_name="حالة الدفع"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "فاتورة شراء"
        verbose_name_plural = "فواتير المشتريات"
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['order_date']),
            models.Index(fields=['supplier']),
        ]

    def __str__(self):
        return f"فاتورة شراء #{self.id} - {self.supplier.name if self.supplier else 'مورد عام'} ({self.order_date.strftime('%Y-%m-%d')})"


# =============================================================================
# نموذج تفاصيل فاتورة الشراء (PurchaseItem)
# =============================================================================

class PurchaseItem(models.Model):
    """
    نموذج تفاصيل فاتورة الشراء (الأصناف)
    يمثل كل صنف داخل فاتورة الشراء، ويربط المنتج بالفاتورة مع الكمية والسعر
    """
    order = models.ForeignKey(
        PurchaseOrder, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="الفاتورة"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT, 
        related_name='purchase_items',
        verbose_name="المنتج"
    )
    quantity = models.PositiveIntegerField(verbose_name="الكمية المشتراة")
    price = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name="سعر الوحدة"
    )
    subtotal = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name="المجموع الجزئي"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "صنف مشتري"
        verbose_name_plural = "أصناف المشتريات"
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} في فاتورة شراء #{self.order.id}"

    def save(self, *args, **kwargs):
        """
        حساب المجموع الجزئي تلقائياً قبل الحفظ
        """
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)


# =============================================================================
# نموذج حركة المخزن (StockMovement)
# =============================================================================

class StockMovement(models.Model):
    """
    نموذج حركة المخزن
    يسجل جميع حركات الدخول والخروج للمنتجات في المخزن
    """
    MOVEMENT_TYPES = [
        ('in', 'إضافة/دخول'),
        ('out', 'خصم/خروج'),
        ('adjustment', 'تعديل يدوي'),
        ('return', 'مرتجع'),
    ]
    
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='stock_movements',
        verbose_name="المنتج"
    )
    quantity = models.IntegerField(verbose_name="الكمية")  # موجب للإضافة، سالب للخصم
    movement_type = models.CharField(
        max_length=20, 
        choices=MOVEMENT_TYPES, 
        verbose_name="نوع الحركة"
    )
    reference_type = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="نوع المرجع"
    )
    reference_id = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        verbose_name="رقم المرجع"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظة")
    movement_date = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الحركة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")

    class Meta:
        verbose_name = "حركة مخزن"
        verbose_name_plural = "حركات المخزن"
        ordering = ['-movement_date']
        indexes = [
            models.Index(fields=['product', 'movement_date']),
            models.Index(fields=['movement_type']),
        ]

    def __str__(self):
        type_label = dict(self.MOVEMENT_TYPES).get(self.movement_type, self.movement_type)
        sign = "+" if self.quantity > 0 else ""
        return f"{self.product.name}: {sign}{self.quantity} ({type_label}) - {self.movement_date.strftime('%Y-%m-%d')}"
