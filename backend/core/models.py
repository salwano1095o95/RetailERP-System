from django.db import models


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
