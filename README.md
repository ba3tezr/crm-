# نظام إدارة علاقات العملاء - CRM System

نظام CRM متكامل مبني بـ Django لإدارة التصاريح، الصيانة، الشكاوى، التسويق، الموارد البشرية، والمالية.

---

## المميزات - Features

- نظام مستخدمين متقدم مع صلاحيات مخصصة
- 6 مديولات رئيسية (التصاريح، الصيانة، الشكاوى، التسويق، HR، المالية)
- دعم كامل للعربية والإنجليزية
- نظام إشعارات متقدم
- نظام موافقات متعدد المستويات

---

## التثبيت - Installation

### 1. استنساخ المشروع
```bash
git clone https://github.com/ba3tezr/crm-.git
cd crm-
```

### 2. إنشاء بيئة افتراضية
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

### 3. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 4. إعداد ملف البيئة
```bash
cp .env.example .env
```

### 5. تطبيق Migrations
```bash
python manage.py migrate
```

### 6. إنشاء Superuser
```bash
python manage.py createsuperuser
```

### 7. تشغيل السيرفر
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## نظام الصلاحيات

1. افتح: `http://127.0.0.1:8000/admin/`
2. اذهب إلى **المستخدمون**
3. اختر المستخدم
4. أضف صلاحيات الأقسام

---

## التقنيات

- Django 5.0.14
- Bootstrap 5.3
- HTMX
- Font Awesome 6

---

**v1.0.0** - 2025-10-26
