from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# =============================================================================
# نموذج تمديد المستخدم لإضافة الصلاحيات
# =============================================================================

class UserProfile(models.Model):
    """
    نموذج لتمديد مستخدم Django وإضافة حقل الصلاحية
    """
    ROLE_CHOICES = [
        ('admin', 'مدير النظام'),
        ('manager', 'مدير المحل'),
        ('cashier', 'كاشير'),
        ('storekeeper', 'أمين المخزن'),
        ('accountant', 'محاسب'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='المستخدم')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier', verbose_name='الصلاحية')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='رقم الهاتف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ آخر تحديث')
    
    class Meta:
        verbose_name = 'ملف المستخدم'
        verbose_name_plural = 'ملفات المستخدمين'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


# =============================================================================
# نموذج الموردين (Supplier)
# =============================================================================

class Supplier(models.Model):
    """
    نموذج لتخزين بيانات الموردين
    """
    name = models.CharField(max_length=200, verbose_name='اسم المورد')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    email = models.EmailField(blank=True, null=True, verbose_name='البريد الإلكتروني')
    address = models.TextField(blank=True, null=True, verbose_name='العنوان')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='الرصيد المستحق')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ آخر تحديث')
    
    class Meta:
        verbose_name = 'مورد'
        verbose_name_plural = 'الموردين'
        ordering = ['name']
    
    def __str__(self):
        return self.name


# =============================================================================
# نموذج العملاء (Customer)
# =============================================================================

class Customer(models.Model):
    """
    نموذج لتخزين بيانات العملاء
    """
    name = models.CharField(max_length=200, verbose_name='اسم العميل')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    email = models.EmailField(blank=True, null=True, verbose_name='البريد الإلكتروني')
    address = models.TextField(blank=True, null=True, verbose_name='العنوان')
    debt = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='الدين المستحق')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ آخر تحديث')
    
    class Meta:
        verbose_name = 'عميل'
        verbose_name_plural = 'العملاء'
        ordering = ['name']
    
    def __str__(self):
        return self.name


# =============================================================================
# نموذج الأصناف (Product)
# =============================================================================

class Product(models.Model):
    """
    نموذج لتخزين بيانات الأصناف والمنتجات
    """
    barcode = models.CharField(max_length=50, unique=True, verbose_name='الباركود')
    name = models.CharField(max_length=200, verbose_name='اسم الصنف')
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name='التصنيف')
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='سعر الشراء')
    selling_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='سعر البيع')
    stock_quantity = models.IntegerField(default=0, verbose_name='الكمية بالمخزن')
    alert_threshold = models.IntegerField(default=10, verbose_name='حد التنبيه')
    min_order_quantity = models.IntegerField(default=1, verbose_name='أقل كمية للطلب')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='products', verbose_name='المورد')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ آخر تحديث')
    
    class Meta:
        verbose_name = 'صنف'
        verbose_name_plural = 'الأصناف'
        ordering = ['name']
        indexes = [
            models.Index(fields=['barcode']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.barcode})"
    
    def clean(self):
        """تحقق من صحة البيانات"""
        if self.purchase_price < 0:
            raise ValidationError({'purchase_price': 'سعر الشراء لا يمكن أن يكون سالباً'})
        if self.selling_price < 0:
            raise ValidationError({'selling_price': 'سعر البيع لا يمكن أن يكون سالباً'})
        if self.stock_quantity < 0:
            raise ValidationError({'stock_quantity': 'الكمية لا يمكن أن تكون سالبة'})
    
    @property
    def profit_margin(self):
        """حساب هامش الربح"""
        if self.selling_price and self.purchase_price:
            return self.selling_price - self.purchase_price
        return 0
    
    @property
    def is_low_stock(self):
        """التحقق مما إذا كان الصنف قريباً من النفاد"""
        return self.stock_quantity <= self.alert_threshold


# =============================================================================
# نموذج فواتير الشراء (PurchaseOrder)
# =============================================================================

class PurchaseOrder(models.Model):
    """
    نموذج لفواتير شراء الأصناف من الموردين
    """
    STATUS_CHOICES = [
        ('draft', 'مسودة'),
        ('pending', 'قيد المعالجة'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغى'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True, verbose_name='رقم الفاتورة')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders', 
                                  verbose_name='المورد')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='الحالة')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='الإجمالي')
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='المدفوع')
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='الخصم')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الفاتورة')
    received_date = models.DateTimeField(null=True, blank=True, verbose_name='تاريخ الاستلام')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                    related_name='created_purchase_orders', verbose_name='أنشأ بواسطة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ آخر تحديث')
    
    class Meta:
        verbose_name = 'فاتورة شراء'
        verbose_name_plural = 'فواتير الشراء'
        ordering = ['-order_date']
    
    def __str__(self):
        return f"فاتورة شراء #{self.order_number} - {self.supplier.name}"
    
    @property
    def remaining_amount(self):
        """حساب المبلغ المتبقي"""
        return self.total_amount - self.paid_amount
    
    @property
    def is_paid(self):
        """التحقق مما إذا كانت الفاتورة مدفوعة بالكامل"""
        return self.remaining_amount <= 0


# =============================================================================
# نموذج عناصر فاتورة الشراء (PurchaseItem)
# =============================================================================

class PurchaseItem(models.Model):
    """
    نموذج لعناصر فاتورة الشراء (الصنف الواحد داخل الفاتورة)
    """
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items', 
                                        verbose_name='فاتورة الشراء')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='purchase_items', 
                                 verbose_name='الصنف')
    quantity = models.IntegerField(verbose_name='الكمية')
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='سعر الوحدة')
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='الإجمالي الجزئي')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    
    class Meta:
        verbose_name = 'عنصر شراء'
        verbose_name_plural = 'عناصر الشراء'
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    def clean(self):
        """تحقق من صحة البيانات"""
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'الكمية يجب أن تكون أكبر من صفر'})
        if self.unit_price < 0:
            raise ValidationError({'unit_price': 'سعر الوحدة لا يمكن أن يكون سالباً'})
    
    def save(self, *args, **kwargs):
        """حساب الإجمالي الجزئي تلقائياً قبل الحفظ"""
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)


# =============================================================================
# نموذج فواتير البيع (SalesOrder)
# =============================================================================

class SalesOrder(models.Model):
    """
    نموذج لفواتير بيع الأصناف للعملاء
    """
    STATUS_CHOICES = [
        ('draft', 'مسودة'),
        ('pending', 'قيد المعالجة'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغى'),
        ('returned', 'مرتجع'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'مدفوع'),
        ('partial', 'مدفوع جزئياً'),
        ('unpaid', 'غير مدفوع'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True, verbose_name='رقم الفاتورة')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales_orders', 
                                  verbose_name='العميل', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name='الحالة')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='paid', 
                                       verbose_name='حالة الدفع')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='الإجمالي')
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='المدفوع')
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='الخصم')
    tax = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='الضريبة')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الفاتورة')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                    related_name='created_sales_orders', verbose_name='أنشأ بواسطة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ آخر تحديث')
    
    class Meta:
        verbose_name = 'فاتورة بيع'
        verbose_name_plural = 'فواتير البيع'
        ordering = ['-order_date']
    
    def __str__(self):
        customer_name = self.customer.name if self.customer else 'عميل نقدي'
        return f"فاتورة بيع #{self.order_number} - {customer_name}"
    
    @property
    def remaining_amount(self):
        """حساب المبلغ المتبقي"""
        return self.total_amount - self.paid_amount
    
    @property
    def is_paid(self):
        """التحقق مما إذا كانت الفاتورة مدفوعة بالكامل"""
        return self.remaining_amount <= 0
    
    @property
    def profit(self):
        """حساب الربح الإجمالي للفاتورة"""
        total_cost = sum(item.product.purchase_price * item.quantity for item in self.items.all())
        return self.total_amount - total_cost


# =============================================================================
# نموذج عناصر فاتورة البيع (SalesItem)
# =============================================================================

class SalesItem(models.Model):
    """
    نموذج لعناصر فاتورة البيع (الصنف الواحد داخل الفاتورة)
    """
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items', 
                                     verbose_name='فاتورة البيع')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sales_items', 
                                 verbose_name='الصنف')
    quantity = models.IntegerField(verbose_name='الكمية')
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='سعر الوحدة')
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='الإجمالي الجزئي')
    cost_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='سعر التكلفة')
    profit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='الربح')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    
    class Meta:
        verbose_name = 'عنصر بيع'
        verbose_name_plural = 'عناصر البيع'
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    def clean(self):
        """تحقق من صحة البيانات"""
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'الكمية يجب أن تكون أكبر من صفر'})
        if self.unit_price < 0:
            raise ValidationError({'unit_price': 'سعر الوحدة لا يمكن أن يكون سالباً'})
    
    def save(self, *args, **kwargs):
        """حساب الإجمالي الجزئي والربح تلقائياً قبل الحفظ"""
        self.subtotal = self.quantity * self.unit_price
        self.cost_price = self.product.purchase_price * self.quantity
        self.profit = self.subtotal - self.cost_price
        super().save(*args, **kwargs)


# =============================================================================
# نموذج حركات المخزن (StockMovement) - لتتبع حركة الأصناف
# =============================================================================

class StockMovement(models.Model):
    """
    نموذج لتتبع حركات المخزن (إضافات وسحوبات)
    """
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'إضافة للمخزن'),
        ('out', 'سحب من المخزن'),
        ('adjustment', 'تعديل مخزن'),
        ('return', 'مرتجع'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements', 
                                 verbose_name='الصنف')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES, verbose_name='نوع الحركة')
    quantity = models.IntegerField(verbose_name='الكمية')
    reference_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='نوع المرجع')
    reference_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='رقم المرجع')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                    related_name='stock_movements', verbose_name='أنشأ بواسطة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الحركة')
    
    class Meta:
        verbose_name = 'حركة مخزن'
        verbose_name_plural = 'حركات المخزن'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} - {self.quantity}"
