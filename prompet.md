# 🎯 PROMPT الشامل لإنشاء نظام CRM متكامل

## 📋 نظرة عامة على المشروع

أنشئ نظام CRM (Customer Relationship Management) متكامل وشامل لإدارة العمليات التجارية والتشغيلية في مركز تجاري أو مجمع سكني/تجاري. النظام يجب أن يكون تطبيق ويب حديث وعالي الأداء.

---

## 🛠️ المتطلبات التقنية

### Backend Framework
- **Django 5.0+** (أحدث إصدار مستقر)
- **Django REST Framework** للـ API
- **SQLite** (للتطوير) → **PostgreSQL** (للإنتاج - سيتم التوسع لاحقاً)
- **Redis** للـ Caching والـ Background Tasks
- **Celery** للمهام الخلفية والإشعارات

### Frontend Framework
- **Bootstrap 5.3+** (أحدث إصدار - متجاوب تماماً)
- **HTMX 1.9+** للتفاعلية بدون JavaScript معقد
- **Alpine.js** (اختياري) للتفاعلات البسيطة
- **Django Templates** مع HTMX

### الأدوات والمكتبات الإضافية
- **django-crispy-forms** + **crispy-bootstrap5** للنماذج
- **django-filter** للفلترة المتقدمة
- **django-import-export** لاستيراد/تصدير البيانات (Excel)
- **openpyxl** + **xlsxwriter** للتعامل مع Excel
- **Pillow** لمعالجة الصور
- **python-decouple** لإدارة المتغيرات البيئية
- **django-allauth** للمصادقة المتقدمة
- **django-guardian** للصلاحيات على مستوى الكائنات
- **django-notifications-hq** للإشعارات
- **django-modeltranslation** للترجمة الثنائية (عربي/إنجليزي)
- **WeasyPrint** أو **ReportLab** لتوليد PDF
- **django-storages** + **boto3** للتخزين السحابي (اختياري)

---

## 🎨 متطلبات واجهة المستخدم (UI/UX) - إلزامية ومهمة جداً

### 1️⃣ القائمة الجانبية (Sidebar) - متطلبات إلزامية

**المواصفات الأساسية:**
- ✅ **قائمة جانبية ثابتة** على اليمين (للعربية) / اليسار (للإنجليزية)
- ✅ **إمكانية إخفاء/إظهار** القائمة بزر Toggle (☰)
- ✅ **عند الإخفاء**: توسيع المحتوى الرئيسي ليملأ الشاشة بالكامل (100% width)
- ✅ **عند الإظهار**: تصغير المحتوى ليتناسب مع القائمة (sidebar width: 250px)
- ✅ **أيقونات واضحة** لكل موديول مع نص توضيحي
- ✅ **تمييز القسم النشط** بلون مختلف (background + border)
- ✅ **قوائم منسدلة** للموديولات الفرعية (Collapsible Menus)
- ✅ **تثبيت القائمة** عند التمرير (Sticky Sidebar - position: fixed)
- ✅ **Smooth Transitions** عند الإخفاء/الإظهار (CSS transitions)

**الموديولات في القائمة الجانبية:**
```
📊 لوحة التحكم (Dashboard)
   └─ الإحصائيات العامة

🏢 لوحة المستأجر (Tenant Dashboard) - ✅ COMPLETED
   ├─ ملفي الشخصي (My Profile)
   ├─ فواتيري (My Invoices)
   └─ تصاريحي (My Permits)

📝 التصاريح (Permits) - ✅ COMPLETED
   ├─ تصاريح البضائع (Goods)
   ├─ تصاريح الصيانة (Maintenance)
   └─ تصاريح التسويق (Marketing)

🔧 الصيانة (Maintenance) - ✅ COMPLETED
   ├─ التذاكر (Tickets)
   ├─ الفنيين (Technicians)
   └─ تقارير الصيانة

💬 الشكاوى والاقتراحات (Complaints) - ✅ COMPLETED
   ├─ الشكاوى (Complaints)
   ├─ الإطراءات (Complements)
   └─ الاقتراحات (Suggestions)

🎉 التسويق (Marketing) - ✅ COMPLETED
   ├─ الفعاليات (Events)
   ├─ التنشيطات (Activations)
   └─ تقارير التسويق

👥 الموارد البشرية (HR) - ✅ COMPLETED
   ├─ الإجازات (Leave Requests)
   ├─ الموظفين (Employees)
   ├─ الحضور والانصراف
   └─ رصيد الإجازات

🏦 المالية (Finance) - ✅ COMPLETED
   ├─ الفواتير (Invoices)
   ├─ المدفوعات (Payments)
   └─ التقارير المالية

📊 التقارير (Reports) - ⏳ PENDING
   ├─ تقارير التصاريح
   ├─ تقارير الصيانة
   ├─ تقارير الشكاوى
   └─ تقارير الموارد البشرية

⚙️ الإعدادات (Settings) - ✅ COMPLETED
   ├─ إعدادات النظام (SystemSettings)
   ├─ إعدادات العملة (Currency Settings)
   ├─ إدارة المستخدمين
   └─ الصلاحيات
```

### 2️⃣ الهيدر (Header) - ثابت ومتطلبات إلزامية

**المواصفات:**
- ✅ **ثابت في الأعلى** عند التمرير (Sticky Header - position: fixed, top: 0)
- ✅ **شعار النظام** على اليمين (عربي) / اليسار (إنجليزي)
- ✅ **زر تبديل اللغة** (عربي ⇄ English) مع أيقونة علم 🇸🇦 🇬🇧
- ✅ **أيقونة الإشعارات** 🔔 مع عداد الإشعارات غير المقروءة
- ✅ **قائمة منسدلة للمستخدم** (الملف الشخصي، الإعدادات، تسجيل الخروج)
- ✅ **شريط بحث عام** (Global Search) للبحث في كل النظام
- ✅ **زر إخفاء/إظهار القائمة الجانبية** (☰ Hamburger Icon)
- ✅ **معلومات المستخدم الحالي** (الاسم، الصورة، القسم)

### 3️⃣ الفوتر (Footer) - ثابت

**المواصفات:**
- ✅ **ثابت في الأسفل** (Sticky Footer)
- ✅ **معلومات حقوق النشر** © 2025 CRM System
- ✅ **روابط سريعة** (الدعم الفني، الشروط والأحكام، سياسة الخصوصية)
- ✅ **معلومات الإصدار** (Version 1.0.0)
- ✅ **معلومات الاتصال** (البريد الإلكتروني، الهاتف)

### 4️⃣ المحتوى الرئيسي (Main Content Area) - مهم جداً

**متطلبات HTMX للتنقل السلس:**
- ✅ **لا يتم إعادة تحميل** الهيدر والفوتر والقائمة الجانبية عند التنقل
- ✅ **استخدام HTMX** لتحميل المحتوى ديناميكياً في منطقة المحتوى فقط
- ✅ **Smooth Transitions** عند التنقل بين الصفحات
- ✅ **Loading Indicator** (Spinner) عند تحميل البيانات
- ✅ **Breadcrumbs** للتنقل (الرئيسية > التصاريح > تصريح جديد)
- ✅ **Error Handling** لعرض الأخطاء بشكل واضح

**مثال على استخدام HTMX:**
```html
<!-- القائمة الجانبية -->
<a href="/permits/"
   hx-get="/permits/"
   hx-target="#main-content"
   hx-push-url="true"
   hx-indicator="#loading">
   📝 التصاريح
</a>

<!-- منطقة المحتوى -->
<div id="main-content">
   <!-- يتم تحميل المحتوى هنا -->
</div>

<!-- Loading Indicator -->
<div id="loading" class="htmx-indicator">
   <div class="spinner-border"></div>
</div>
```

---

## 📱 التوافق مع الأجهزة المحمولة - إلزامي ومهم جداً

### متطلبات Mobile-First Design

**اختبار على جميع أحجام الشاشات:**
- ✅ **Mobile Small**: 320px - 480px (iPhone SE, Galaxy S)
- ✅ **Mobile Medium**: 481px - 767px (iPhone 12, Pixel)
- ✅ **Tablet**: 768px - 1024px (iPad, Galaxy Tab)
- ✅ **Desktop**: 1025px - 1440px
- ✅ **Large Desktop**: 1441px+

**تصميم متجاوب للقائمة الجانبية:**
```css
/* Desktop: قائمة جانبية ثابتة */
@media (min-width: 1025px) {
    .sidebar { width: 250px; position: fixed; }
    .main-content { margin-right: 250px; } /* للعربية */
}

/* Mobile/Tablet: Hamburger Menu */
@media (max-width: 1024px) {
    .sidebar {
        transform: translateX(100%); /* مخفية افتراضياً */
        position: fixed;
        z-index: 1000;
    }
    .sidebar.active { transform: translateX(0); }
    .main-content { margin: 0; width: 100%; }
}
```

**متطلبات Mobile:**
- ✅ **القائمة الجانبية** تتحول إلى **Off-Canvas Menu** (تنزلق من الجانب)
- ✅ **الجداول** قابلة للتمرير أفقياً (Horizontal Scroll)
- ✅ **الأزرار** بحجم مناسب للمس (min-height: 44px)
- ✅ **النماذج** بحقول كبيرة وواضحة
- ✅ **الصور** محسّنة للشاشات الصغيرة (Responsive Images)
- ✅ **Font Size** مناسب للقراءة (min: 16px)

**اختبار على متصفحات الهاتف:**
- ✅ Chrome Mobile (Android)
- ✅ Safari iOS (iPhone/iPad)
- ✅ Samsung Internet
- ✅ Firefox Mobile

**تحسين الأداء للموبايل:**
- ✅ **Lazy Loading** للصور والمحتوى
- ✅ **Minified CSS/JS**
- ✅ **Compressed Images** (WebP format)
- ✅ **Service Workers** للتخزين المؤقت (اختياري)

---

## 🌍 ثنائية اللغة (Bilingual) - إلزامي من التأسيس

### 1️⃣ إعداد Django للترجمة الشاملة

**settings.py:**
```python
# اللغات المدعومة
LANGUAGE_CODE = 'ar'  # اللغة الافتراضية: العربية
LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
]

# مسارات ملفات الترجمة
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# تفعيل الترجمة
USE_I18N = True  # Internationalization
USE_L10N = True  # Localization
USE_TZ = True    # Timezone

# Middleware للترجمة
MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware',  # مهم جداً
    ...
]
```

### 2️⃣ ترجمة شاملة لكل شيء - إلزامي

**يجب ترجمة:**
- ✅ **جميع نصوص الواجهة** (UI Text)
- ✅ **القوائم والأزرار** (Menus & Buttons)
- ✅ **رسائل النظام** (System Messages)
- ✅ **رسائل الأخطاء** (Error Messages)
- ✅ **رسائل النجاح** (Success Messages)
- ✅ **تسميات النماذج** (Form Labels & Placeholders)
- ✅ **رسائل التحقق** (Validation Messages)
- ✅ **الإشعارات** (Notifications)
- ✅ **رسائل البريد الإلكتروني** (Email Templates)
- ✅ **التقارير** (Reports & PDFs)
- ✅ **نصوص المساعدة** (Help Text & Tooltips)

**مثال على الترجمة في Templates:**
```django
{% load i18n %}

<!-- ترجمة نص -->
<h1>{% trans "Dashboard" %}</h1>

<!-- ترجمة مع متغيرات -->
<p>{% blocktrans with name=user.name %}Welcome, {{ name }}{% endblocktrans %}</p>

<!-- ترجمة في الأزرار -->
<button>{% trans "Save" %}</button>
<button>{% trans "Cancel" %}</button>
```

**مثال على الترجمة في Models:**
```python
from django.utils.translation import gettext_lazy as _

class Permit(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    status = models.CharField(_("Status"), max_length=20)

    class Meta:
        verbose_name = _("Permit")
        verbose_name_plural = _("Permits")
```

### 3️⃣ دعم RTL/LTR - إلزامي

**base.html:**
```html
<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}" dir="{% if LANGUAGE_CODE == 'ar' %}rtl{% else %}ltr{% endif %}">
<head>
    {% if LANGUAGE_CODE == 'ar' %}
        <link rel="stylesheet" href="{% static 'css/bootstrap.rtl.min.css' %}">
        <link rel="stylesheet" href="{% static 'css/style-rtl.css' %}">
    {% else %}
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
        <link rel="stylesheet" href="{% static 'css/style-ltr.css' %}">
    {% endif %}
</head>
```

**CSS للدعم الثنائي:**
```css
/* للعربية - RTL */
[dir="rtl"] {
    direction: rtl;
    text-align: right;
}

[dir="rtl"] .sidebar {
    right: 0;
    left: auto;
}

[dir="rtl"] .main-content {
    margin-right: 250px;
    margin-left: 0;
}

/* للإنجليزية - LTR */
[dir="ltr"] {
    direction: ltr;
    text-align: left;
}

[dir="ltr"] .sidebar {
    left: 0;
    right: auto;
}

[dir="ltr"] .main-content {
    margin-left: 250px;
    margin-right: 0;
}
```

### 4️⃣ تبديل اللغة - إلزامي

**في الهيدر:**
```html
<div class="language-switcher">
    <form action="{% url 'set_language' %}" method="post">
        {% csrf_token %}
        <input name="next" type="hidden" value="{{ request.path }}">
        <select name="language" onchange="this.form.submit()">
            <option value="ar" {% if LANGUAGE_CODE == 'ar' %}selected{% endif %}>
                🇸🇦 العربية
            </option>
            <option value="en" {% if LANGUAGE_CODE == 'en' %}selected{% endif %}>
                🇬🇧 English
            </option>
        </select>
    </form>
</div>
```

### 5️⃣ ملفات الترجمة - هيكلة إلزامية

**هيكل المجلدات:**
```
crm_project/
├── locale/
│   ├── ar/
│   │   └── LC_MESSAGES/
│   │       ├── django.po      # ملف الترجمة العربية
│   │       └── django.mo      # ملف مترجم
│   └── en/
│       └── LC_MESSAGES/
│           ├── django.po      # ملف الترجمة الإنجليزية
│           └── django.mo      # ملف مترجم
```

**أوامر إنشاء ملفات الترجمة:**
```bash
# إنشاء ملفات الترجمة
python manage.py makemessages -l ar
python manage.py makemessages -l en

# ترجمة الملفات (يدوياً في django.po)

# تجميع الترجمات
python manage.py compilemessages
```

---

## 📁 هيكلة الملفات والمجلدات - إلزامية وثابتة

### هيكل المشروع الكامل

**يجب اتباع هذا الهيكل بدقة:**

```
crm_project/
├── config/                          # إعدادات المشروع الرئيسية
│   ├── __init__.py
│   ├── settings.py                  # الإعدادات الرئيسية
│   ├── settings_dev.py              # إعدادات التطوير (SQLite)
│   ├── settings_prod.py             # إعدادات الإنتاج (PostgreSQL)
│   ├── urls.py                      # URLs الرئيسية
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py                    # إعدادات Celery
│
├── apps/                            # جميع التطبيقات
│   ├── __init__.py
│   │
│   ├── accounts/                    # نظام المستخدمين
│   │   ├── __init__.py
│   │   ├── models.py               # CustomUser, Department, TenantProfile
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── signals.py
│   │   ├── managers.py
│   │   ├── permissions.py
│   │   ├── templates/
│   │   │   └── accounts/
│   │   │       ├── login.html
│   │   │       ├── profile.html
│   │   │       ├── user_list.html
│   │   │       └── user_form.html
│   │   ├── migrations/
│   │   └── tests/
│   │
│   ├── permits/                     # نظام التصاريح
│   │   ├── __init__.py
│   │   ├── models.py               # Permit, PermitApproval
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── resources.py            # للاستيراد/التصدير
│   │   ├── workflows.py            # سير العمل
│   │   ├── templates/
│   │   │   └── permits/
│   │   │       ├── permit_list.html
│   │   │       ├── permit_detail.html
│   │   │       ├── permit_form.html
│   │   │       ├── permit_approve.html
│   │   │       └── partials/       # HTMX partials
│   │   ├── migrations/
│   │   └── tests/
│   │
│   ├── maintenance/                 # نظام الصيانة
│   │   ├── __init__.py
│   │   ├── models.py               # Ticket, TicketComment
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── resources.py
│   │   ├── templates/
│   │   │   └── maintenance/
│   │   │       ├── ticket_list.html
│   │   │       ├── ticket_detail.html
│   │   │       ├── ticket_form.html
│   │   │       └── partials/
│   │   ├── migrations/
│   │   └── tests/
│   │
│   ├── complaints/                  # نظام الشكاوى
│   │   ├── __init__.py
│   │   ├── models.py               # Case, CaseComment
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── resources.py
│   │   ├── templates/
│   │   │   └── complaints/
│   │   ├── migrations/
│   │   └── tests/
│   │
│   ├── marketing/                   # نظام التسويق
│   │   ├── __init__.py
│   │   ├── models.py               # MarketingPermit
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── resources.py
│   │   ├── templates/
│   │   │   └── marketing/
│   │   ├── migrations/
│   │   └── tests/
│   │
│   ├── hr/                          # الموارد البشرية
│   │   ├── __init__.py
│   │   ├── models.py               # LeaveRequest, LeaveBalance
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── resources.py
│   │   ├── templates/
│   │   │   └── hr/
│   │   ├── migrations/
│   │   └── tests/
│   │
│   ├── notifications/               # نظام الإشعارات
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── tasks.py                # Celery tasks
│   │   ├── templates/
│   │   │   └── notifications/
│   │   ├── migrations/
│   │   └── tests/
│   │
│   ├── reports/                     # نظام التقارير
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── generators.py           # PDF/Excel generators
│   │   ├── templates/
│   │   │   └── reports/
│   │   └── tests/
│   │
│   └── core/                        # الوظائف المشتركة
│       ├── __init__.py
│       ├── models.py               # BaseModel, TimeStampedModel
│       ├── mixins.py
│       ├── utils.py
│       ├── decorators.py
│       ├── middleware.py
│       └── templatetags/
│           ├── __init__.py
│           └── custom_tags.py
│
├── static/                          # الملفات الثابتة
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   ├── bootstrap.rtl.min.css   # Bootstrap RTL
│   │   ├── style.css               # الأنماط العامة
│   │   ├── style-rtl.css           # أنماط RTL
│   │   ├── style-ltr.css           # أنماط LTR
│   │   ├── sidebar.css             # أنماط القائمة الجانبية
│   │   └── mobile.css              # أنماط الموبايل
│   ├── js/
│   │   ├── bootstrap.bundle.min.js
│   │   ├── htmx.min.js             # HTMX
│   │   ├── alpine.min.js           # Alpine.js
│   │   ├── chart.min.js            # Chart.js
│   │   ├── main.js                 # JavaScript الرئيسي
│   │   ├── sidebar.js              # وظائف القائمة الجانبية
│   │   └── language-switcher.js    # تبديل اللغة
│   ├── images/
│   │   ├── logo.png
│   │   ├── logo-ar.png
│   │   ├── logo-en.png
│   │   └── icons/
│   ├── fonts/
│   │   ├── Cairo/                  # خط عربي
│   │   └── Roboto/                 # خط إنجليزي
│   └── vendor/                     # مكتبات خارجية
│
├── media/                           # الملفات المرفوعة
│   ├── permits/
│   ├── maintenance/
│   ├── complaints/
│   ├── marketing/
│   ├── profiles/
│   └── documents/
│
├── templates/                       # القوالب الرئيسية
│   ├── base.html                   # القالب الأساسي
│   ├── base_rtl.html               # قالب RTL
│   ├── base_ltr.html               # قالب LTR
│   ├── includes/
│   │   ├── header.html             # الهيدر الثابت
│   │   ├── sidebar.html            # القائمة الجانبية الثابتة
│   │   ├── footer.html             # الفوتر الثابت
│   │   ├── breadcrumbs.html
│   │   ├── messages.html
│   │   └── pagination.html
│   ├── partials/                   # HTMX partials
│   │   ├── loading.html
│   │   ├── error.html
│   │   └── success.html
│   ├── components/                 # مكونات قابلة لإعادة الاستخدام
│   │   ├── card.html
│   │   ├── table.html
│   │   ├── form.html
│   │   └── modal.html
│   ├── dashboard/
│   │   └── index.html
│   ├── auth/
│   │   ├── login.html
│   │   ├── logout.html
│   │   └── password_reset.html
│   └── errors/
│       ├── 404.html
│       ├── 500.html
│       └── 403.html
│
├── locale/                          # ملفات الترجمة
│   ├── ar/
│   │   └── LC_MESSAGES/
│   │       ├── django.po
│   │       └── django.mo
│   └── en/
│       └── LC_MESSAGES/
│           ├── django.po
│           └── django.mo
│
├── tests/                           # الاختبارات
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_forms.py
│   └── test_workflows.py
│
├── docs/                            # التوثيق
│   ├── README.md
│   ├── INSTALLATION.md
│   ├── API.md
│   └── USER_GUIDE.md
│
├── requirements/                    # المتطلبات
│   ├── base.txt                    # المتطلبات الأساسية
│   ├── development.txt             # للتطوير
│   └── production.txt              # للإنتاج
│
├── scripts/                         # سكريبتات مساعدة
│   ├── backup.sh
│   ├── deploy.sh
│   └── seed_data.py                # بيانات تجريبية
│
├── .env.example                     # مثال للمتغيرات البيئية
├── .gitignore
├── manage.py
├── README.md
├── requirements.txt
└── db.sqlite3                       # قاعدة البيانات (للتطوير)
```

---

## 📥📤 الاستيراد والتصدير من/إلى Excel - إلزامي لجميع الجداول

### متطلبات الاستيراد/التصدير

**يجب توفير إمكانية الاستيراد والتصدير لـ:**
- ✅ جميع جداول التصاريح (Permits)
- ✅ جميع جداول الصيانة (Maintenance Tickets)
- ✅ جميع جداول الشكاوى (Complaints)
- ✅ جميع جداول التسويق (Marketing)
- ✅ جميع جداول الموارد البشرية (HR)
- ✅ جداول المستخدمين (Users)
- ✅ جداول الأقسام (Departments)

### 1️⃣ إعداد django-import-export

**تثبيت المكتبة:**
```bash
pip install django-import-export openpyxl xlsxwriter
```

**settings.py:**
```python
INSTALLED_APPS = [
    ...
    'import_export',
]

# إعدادات الاستيراد/التصدير
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_SKIP_ADMIN_LOG = False
IMPORT_EXPORT_TMP_STORAGE_CLASS = 'import_export.tmp_storages.TempFolderStorage'
```

### 2️⃣ إنشاء Resources لكل Model

**مثال: permits/resources.py**
```python
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget
from .models import Permit
from apps.accounts.models import CustomUser

class PermitResource(resources.ModelResource):
    """Resource للاستيراد/التصدير لنموذج Permit"""

    # تخصيص الحقول
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email')
    )

    scheduled_date = fields.Field(
        column_name='scheduled_date',
        attribute='scheduled_date',
        widget=DateWidget(format='%Y-%m-%d')
    )

    class Meta:
        model = Permit
        fields = (
            'id', 'permit_number', 'permit_type', 'title',
            'description', 'status', 'scheduled_date',
            'scheduled_time', 'location', 'created_by',
            'created_at', 'updated_at'
        )
        export_order = fields
        import_id_fields = ['permit_number']  # المفتاح الفريد
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        """معالجة قبل الاستيراد"""
        # تحويل التواريخ، التحقق من البيانات، إلخ
        pass

    def after_import_row(self, row, row_result, **kwargs):
        """معالجة بعد الاستيراد"""
        # إرسال إشعارات، تحديث إحصائيات، إلخ
        pass
```

**مثال: maintenance/resources.py**
```python
from import_export import resources
from .models import Ticket

class TicketResource(resources.ModelResource):
    class Meta:
        model = Ticket
        fields = (
            'id', 'ticket_number', 'title', 'ticket_type',
            'priority', 'status', 'location', 'created_by',
            'assigned_to', 'created_at', 'closed_at'
        )
        export_order = fields
        import_id_fields = ['ticket_number']
```

### 3️⃣ إضافة الاستيراد/التصدير في Admin

**permits/admin.py:**
```python
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Permit
from .resources import PermitResource

@admin.register(Permit)
class PermitAdmin(ImportExportModelAdmin):
    resource_class = PermitResource
    list_display = ['permit_number', 'title', 'status', 'created_at']
    list_filter = ['status', 'permit_type', 'created_at']
    search_fields = ['permit_number', 'title', 'description']
```

### 4️⃣ إضافة الاستيراد/التصدير في Views

**permits/views.py:**
```python
from django.http import HttpResponse
from django.views.generic import View
from import_export.formats import base_formats
from .resources import PermitResource

class PermitExportView(View):
    """تصدير التصاريح إلى Excel"""

    def get(self, request, *args, **kwargs):
        # الحصول على البيانات المفلترة
        queryset = Permit.objects.filter(created_by=request.user)

        # إنشاء Resource
        permit_resource = PermitResource()
        dataset = permit_resource.export(queryset)

        # تصدير إلى Excel
        format = base_formats.XLSX()
        export_data = format.export_data(dataset)

        # إرجاع الملف
        response = HttpResponse(
            export_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="permits.xlsx"'
        return response

class PermitImportView(View):
    """استيراد التصاريح من Excel"""

    def post(self, request, *args, **kwargs):
        permit_resource = PermitResource()

        # الحصول على الملف المرفوع
        excel_file = request.FILES['file']

        # استيراد البيانات
        dataset = Dataset()
        imported_data = dataset.load(excel_file.read(), format='xlsx')

        # معالجة الاستيراد
        result = permit_resource.import_data(
            dataset,
            dry_run=True  # تجربة أولاً
        )

        if not result.has_errors():
            # الاستيراد الفعلي
            permit_resource.import_data(dataset, dry_run=False)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({
                'status': 'error',
                'errors': result.row_errors()
            })
```

### 5️⃣ إضافة أزرار الاستيراد/التصدير في Templates

**permits/permit_list.html:**
```html
{% load i18n %}

<div class="card">
    <div class="card-header d-flex justify-content-between">
        <h3>{% trans "Permits" %}</h3>
        <div class="btn-group">
            <!-- زر التصدير -->
            <a href="{% url 'permits:export' %}" class="btn btn-success">
                <i class="fas fa-file-excel"></i>
                {% trans "Export to Excel" %}
            </a>

            <!-- زر الاستيراد -->
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#importModal">
                <i class="fas fa-file-upload"></i>
                {% trans "Import from Excel" %}
            </button>
        </div>
    </div>

    <div class="card-body">
        <!-- الجدول -->
        <table class="table table-striped">
            ...
        </table>
    </div>
</div>

<!-- Modal للاستيراد -->
<div class="modal fade" id="importModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">{% trans "Import Permits from Excel" %}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form method="post" enctype="multipart/form-data"
                  hx-post="{% url 'permits:import' %}"
                  hx-target="#import-result">
                {% csrf_token %}
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="file" class="form-label">{% trans "Excel File" %}</label>
                        <input type="file" class="form-control" name="file" accept=".xlsx,.xls" required>
                    </div>
                    <div id="import-result"></div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        {% trans "Cancel" %}
                    </button>
                    <button type="submit" class="btn btn-primary">
                        {% trans "Import" %}
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
```

### 6️⃣ تنسيقات التصدير المدعومة

**يجب دعم:**
- ✅ **Excel (.xlsx)** - الأساسي
- ✅ **CSV (.csv)** - للبيانات البسيطة
- ✅ **JSON (.json)** - للـ API
- ✅ **PDF (.pdf)** - للتقارير

**مثال على تصدير متعدد الصيغ:**
```python
class PermitExportView(View):
    def get(self, request, format='xlsx'):
        queryset = Permit.objects.all()
        permit_resource = PermitResource()
        dataset = permit_resource.export(queryset)

        # اختيار الصيغة
        formats = {
            'xlsx': base_formats.XLSX(),
            'csv': base_formats.CSV(),
            'json': base_formats.JSON(),
        }

        format_obj = formats.get(format, base_formats.XLSX())
        export_data = format_obj.export_data(dataset)

        # تحديد Content-Type
        content_types = {
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'csv': 'text/csv',
            'json': 'application/json',
        }

        response = HttpResponse(
            export_data,
            content_type=content_types.get(format, 'application/octet-stream')
        )
        response['Content-Disposition'] = f'attachment; filename="permits.{format}"'
        return response
```

### 7️⃣ قالب Excel للاستيراد

**يجب توفير قالب Excel فارغ للتحميل:**
```python
class PermitTemplateView(View):
    """تحميل قالب Excel فارغ للاستيراد"""

    def get(self, request):
        # إنشاء dataset فارغ مع الأعمدة فقط
        permit_resource = PermitResource()
        headers = permit_resource.get_export_headers()

        # إنشاء ملف Excel
        dataset = Dataset(headers=headers)

        format = base_formats.XLSX()
        export_data = format.export_data(dataset)

        response = HttpResponse(
            export_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="permits_template.xlsx"'
        return response
```

---

## 📊 تحليل شامل لملف Excel - هيكل النظام

### 1️⃣ نظام الحسابات والمستخدمين (Accounts)

#### الأقسام الرئيسية (10 أقسام):
1. **Operations** - العمليات (8 مستخدمين)
2. **Technical** - الفني (6 مستخدمين)
3. **Marketing** - التسويق (3 مستخدمين)
4. **Finance** - المالية (1 مستخدم)
5. **HR** - الموارد البشرية (2 مستخدمين)
6. **Customer Services** - خدمة العملاء (7 مستخدمين)
7. **Maintenance** - الصيانة (4 مستخدمين)
8. **Security** - الأمن
9. **Tenant** - المستأجرين (80 مستخدم)
10. **Account** - الإدارة

#### حقول المستخدم المطلوبة:
- **الاسم الكامل** (Name)
- **البريد الإلكتروني** (E-mail) - للمصادقة
- **كود الموظف** (Employee Code) - فريد لكل موظف
- **رقم الجوال** (Mobile) - للمستأجرين
- **المدير المباشر** (Direct Line Manager)
- **مدير القسم** (Department Manager)
- **المسمى الوظيفي** (Title)
- **القسم** (Department)
- **الصلاحيات** (Permissions) - حسب القسم

#### حقول خاصة بالمستأجرين:
- **كود الوحدة** (Unit Code)
- **الرقم التسلسلي للوحدة** (Unit Serial No.)
- **العلامة التجارية** (Brand) - للمحلات التجارية
- **الشركة** (Company)
- **الفئة** (Category) - نوع النشاط التجاري
- **مساحة الوحدة** (Unit area) - داخلية/خارجية

---

### 2️⃣ نظام التصاريح (Permits)

#### أنواع التصاريح:
1. **Goods** - تصريح بضائع
2. **Maintenance** - تصريح صيانة
3. **MKG (Marketing)** - تصريح تسويقي

#### سير العمل (Workflow):

**المرسل → المستقبل:**
- **Tenant Interface** (واجهة المستأجر)
  - يرسل: Permit (تصريح)
  - نوع التصريح: Drop Down Menu (Goods, Maintenance, MKG)
  - إرفاق ملفات: Attach

**مسار الموافقة:**
1. **OPS (Operations)** - القسم الأول للمراجعة
   - Two Way Communication (تواصل ثنائي)
   - يمكن: Redirect (إعادة توجيه) / Approve (موافقة) / Not Approve (رفض)
   
2. **Maintenance** - للتصاريح الفنية
   - مراجعة فنية
   - Approved / Remarks / Rejected

3. **MKG (Marketing)** - للتصاريح التسويقية
   - مراجعة تسويقية
   - Approved / Remarks / Rejected

4. **Security** - الموافقة النهائية
   - Approved / Remarks
   - إصدار التصريح النهائي

#### الوثائق المرتبطة:
- **Memo** - مذكرات
- **Penalties** - غرامات
- **Announcement** - إعلانات
- **Invoices** - فواتير

#### التتبع:
- **Permit Cycle** - دورة التصريح الكاملة
- **Permit Log** - سجل جميع التصاريح
- **Status Tracking** - تتبع الحالة في كل مرحلة

---

### 3️⃣ نظام الصيانة (Maintenance)

#### أنواع التذاكر (Ticket Types):
1. **Mechanical** - ميكانيكي
2. **Electrical** - كهربائي
3. **Plumbing** - سباكة
4. **Civil** - مدني
5. **Data** - بيانات/شبكات

#### سير العمل:

**Technical Interface** (واجهة الفني):
- **Send Ticket** - إرسال تذكرة
  - Drop Down Menu لاختيار النوع
  - Attach - إرفاق صور/ملفات
  - Description - وصف المشكلة
  - Location - الموقع
  - Date - التاريخ

**Maintenance Interface** (واجهة الصيانة):
- **Maintenance Manager** - مدير الصيانة
  - يستقبل التذكرة
  - يحدد الأولوية (Priority):
    - **P1** - عاجل جداً (حرج)
    - **P2** - عاجل
    - **P3** - متوسط
    - **P4** - منخفض
  - يوجه للقسم المختص

**الأقسام المتخصصة:**
- **Mechanical Department** - قسم الميكانيكا
- **Electrical Department** - قسم الكهرباء
- **Plumbing Department** - قسم السباكة

#### حالات التذكرة (Status):
1. **Received** - مستلمة
2. **Pending** - قيد الانتظار
3. **Closed** - مغلقة
4. **Return for Info** - إعادة للمعلومات

#### التتبع:
- **Ticket Log** - سجل التذاكر
- **Ticket Cycle** - دورة حياة التذكرة
- **Track Tickets** - تتبع التذاكر
- **Feedback** - تقييم الخدمة
- **Two way Communication** - تواصل ثنائي

---

### 4️⃣ نظام الشكاوى (Complaints)

#### أنواع الحالات (Case Types):
1. **Complement** - إطراء/مديح
2. **Complain** - شكوى
3. **Suggestion** - اقتراح

#### سير العمل:

**Customer Service Interface** (واجهة خدمة العملاء):
- **Send Case** - إرسال حالة
  - Drop Down Menu لاختيار النوع
  - Case Description - وصف الحالة
  - Date & Time - التاريخ والوقت
  - Location - الموقع
  - Name - اسم المشتكي
  - Mobile - رقم الجوال
  - Attach - إرفاق ملفات

**التوجيه للأقسام:**
- Drop Down Menu لاختيار القسم المعني:
  - **MKG** - التسويق
  - **Operations** - العمليات
  - **Technical** - الفني

**المعالجة:**
- **Two way Communication** - تواصل مع المشتكي
- **Operations** - معالجة الحالة

#### حالات القضية:
1. **Pending** - قيد المعالجة
2. **Closed** - مغلقة

#### التتبع:
- **Cases Log** - سجل الحالات
- **Complain Cycle** - دورة الشكوى

---

### 5️⃣ نظام التسويق (Marketing)

#### أنواع التصاريح التسويقية:
1. **Event** - فعالية
2. **Activation** - تنشيط
3. **Tenant Related Event** - فعالية خاصة بالمستأجر

#### سير العمل:

**Marketing Interface** (واجهة التسويق):
- **Send Permit** - إرسال تصريح
  - Drop Down Menu لاختيار النوع
  - Permit Description - وصف التصريح
  - Date & Time - التاريخ والوقت
  - Location - الموقع
  - Marketing Needs - احتياجات تسويقية
  - Suppliers Contacts - جهات اتصال الموردين
  - Attach - إرفاق ملفات

**مسار الموافقة:**
1. **Operations** - العمليات
   - Two way Communication
   - Approved / Remarks / Rejected

2. **Security** - الأمن
   - الموافقة النهائية
   - Attach - إرفاق موافقات

#### التتبع:
- **Permits Log** - سجل التصاريح
- **Marketing Permit Cycle** - دورة التصريح التسويقي

---

### 6️⃣ نظام الموارد البشرية (HR)

#### أنواع الطلبات:
1. **Sick Leave** - إجازة مرضية
2. **Annual Leave** - إجازة سنوية

#### سير العمل:

**Employee Interface** (واجهة الموظف):
- **Send Request** - إرسال طلب
  - Drop Down Menu لاختيار النوع
  - Request Description - وصف الطلب
  - Date - التاريخ
  - Leave Date (From - To) - تاريخ الإجازة (من - إلى)
  - Calendar - تقويم لاختيار التواريخ
  - Reason - السبب
  - Credit (Days) - الرصيد (الأيام)
  - Attach - إرفاق ملفات (شهادة طبية للإجازة المرضية)

**مسار الموافقة:**
1. **First Line Manager** - المدير المباشر
   - Two way Communication
   - Approved / Remarks / Rejected

2. **Second Line Manager** - مدير القسم
   - Approved / Remarks / Rejected
   - Attach - إرفاق موافقات

3. **HR** - الموارد البشرية
   - الموافقة النهائية
   - تحديث رصيد الإجازات

#### التتبع:
- **Requests Log** - سجل الطلبات
- **Request Cycle** - دورة الطلب
- **Leave Balance** - رصيد الإجازات

---

## 🏗️ البنية المعمارية للنظام

### Models (النماذج) المطلوبة:

#### 1. User Management
```python
- CustomUser (extends AbstractUser)
  - employee_code
  - mobile
  - department (FK)
  - direct_manager (FK to self)
  - department_manager (FK to self)
  - title
  - is_tenant
  - is_employee
  
- Department
  - name
  - code
  - manager (FK to User)
  - description
  
- TenantProfile
  - user (OneToOne)
  - unit_code
  - unit_serial_no
  - brand
  - company
  - category
  - unit_area
  - unit_type (indoor/outdoor)
```

#### 2. Permits System
```python
- Permit
  - permit_number (auto-generated)
  - permit_type (Goods/Maintenance/MKG)
  - tenant (FK)
  - description
  - created_at
  - status (Draft/Pending/Approved/Rejected)
  - current_stage
  
- PermitAttachment
  - permit (FK)
  - file
  - uploaded_at
  
- PermitApproval
  - permit (FK)
  - approver (FK to User)
  - stage (OPS/Maintenance/MKG/Security)
  - action (Approved/Rejected/Redirect/Remarks)
  - comments
  - approved_at
  
- Memo
- Penalty
- Announcement
- Invoice
```

#### 3. Maintenance System
```python
- MaintenanceTicket
  - ticket_number (auto-generated)
  - ticket_type (Mechanical/Electrical/Plumbing/Civil/Data)
  - requester (FK)
  - description
  - location
  - priority (P1/P2/P3/P4)
  - status (Received/Pending/Closed/Return for Info)
  - assigned_to (FK to User)
  - assigned_department (FK)
  - created_at
  - closed_at
  
- TicketAttachment
- TicketComment
- TicketFeedback
  - rating
  - comments
```

#### 4. Complaints System
```python
- Case
  - case_number (auto-generated)
  - case_type (Complement/Complain/Suggestion)
  - reporter_name
  - reporter_mobile
  - description
  - location
  - date_time
  - assigned_to_department (MKG/Operations/Technical)
  - status (Pending/Closed)
  - created_at
  
- CaseAttachment
- CaseComment
```

#### 5. Marketing System
```python
- MarketingPermit
  - permit_number (auto-generated)
  - permit_type (Event/Activation/Tenant Related Event)
  - description
  - date_time
  - location
  - marketing_needs
  - suppliers_contacts
  - status
  - created_at
  
- MarketingPermitAttachment
- MarketingPermitApproval
```

#### 6. HR System
```python
- LeaveRequest
  - request_number (auto-generated)
  - employee (FK)
  - leave_type (Sick Leave/Annual Leave)
  - description
  - leave_from
  - leave_to
  - days_count
  - reason
  - status (Pending/Approved/Rejected)
  - first_manager_approval
  - second_manager_approval
  - hr_approval
  - created_at
  
- LeaveRequestAttachment
- LeaveBalance
  - employee (FK)
  - year
  - annual_balance
  - sick_balance
  - used_annual
  - used_sick
```

---

## 🎨 واجهة المستخدم (UI/UX)

### التصميم العام:
- **Dashboard** رئيسي لكل نوع مستخدم
- **Sidebar Navigation** مع أيقونات
- **Top Navigation Bar** مع الإشعارات والملف الشخصي
- **Cards** لعرض الإحصائيات
- **Tables** مع فلترة وبحث متقدم
- **Forms** تفاعلية مع HTMX
- **Modals** للعمليات السريعة
- **Toast Notifications** للتنبيهات

### الألوان المقترحة:
- Primary: #0d6efd (Bootstrap Blue)
- Success: #198754 (Green)
- Warning: #ffc107 (Yellow)
- Danger: #dc3545 (Red)
- Info: #0dcaf0 (Cyan)

### الأيقونات:
- **Bootstrap Icons** أو **Font Awesome**

---

## ⚡ استخدام HTMX

### الميزات المطلوبة:
1. **Infinite Scroll** للجداول الطويلة
2. **Live Search** في الجداول
3. **Inline Editing** للحقول
4. **Dynamic Forms** - تحميل حقول ديناميكية
5. **Partial Updates** - تحديث أجزاء من الصفحة
6. **File Upload** مع Progress Bar
7. **Polling** للإشعارات الجديدة
8. **Lazy Loading** للمحتوى

### أمثلة:
```html
<!-- Live Search -->
<input type="search" 
       hx-get="/permits/search/" 
       hx-trigger="keyup changed delay:500ms" 
       hx-target="#results">

<!-- Inline Approval -->
<button hx-post="/permits/{{ permit.id }}/approve/" 
        hx-swap="outerHTML">
  Approve
</button>

<!-- Load More -->
<button hx-get="/tickets/?page=2" 
        hx-target="#ticket-list" 
        hx-swap="beforeend">
  Load More
</button>
```

---

## 🔐 الصلاحيات والأمان

### مستويات الصلاحيات:
1. **Super Admin** - صلاحيات كاملة
2. **Department Manager** - إدارة القسم
3. **Employee** - صلاحيات محدودة
4. **Tenant** - واجهة المستأجر فقط

### الصلاحيات حسب القسم:
- **Operations**: عرض وموافقة جميع التصاريح
- **Technical**: إدارة تذاكر الصيانة
- **Marketing**: إدارة التصاريح التسويقية
- **HR**: إدارة طلبات الإجازات
- **Customer Service**: إدارة الشكاوى
- **Security**: الموافقة النهائية على التصاريح
- **Tenant**: إنشاء تصاريح وتذاكر فقط

### الأمان:
- **CSRF Protection**
- **XSS Protection**
- **SQL Injection Protection**
- **Rate Limiting**
- **Two-Factor Authentication** (اختياري)
- **Audit Log** - سجل جميع العمليات

---

## 📱 الإشعارات

### أنواع الإشعارات:
1. **Email Notifications**
2. **In-App Notifications**
3. **SMS** (اختياري)

### متى ترسل:
- تصريح جديد
- موافقة/رفض
- تذكرة صيانة جديدة
- تحديث حالة
- تذكير بالمواعيد

---

## 📊 التقارير والإحصائيات

### Dashboard للإدارة:
- عدد التصاريح (حسب النوع والحالة)
- عدد تذاكر الصيانة (حسب الأولوية)
- عدد الشكاوى (حسب النوع)
- متوسط وقت الاستجابة
- معدل الرضا

### التقارير:
- تقرير التصاريح (يومي/أسبوعي/شهري)
- تقرير الصيانة
- تقرير الشكاوى
- تقرير الإجازات
- تصدير Excel/PDF

---

## 🔐 شاشة تسجيل الدخول - إلزامي

### 1️⃣ متطلبات شاشة تسجيل الدخول

**المتطلبات الأساسية:**
- ✅ شاشة تسجيل دخول احترافية ومخصصة بالكامل
- ✅ **خلفية قابلة للتغيير** من لوحة تحكم مدير النظام
- ✅ دعم صورة خلفية أو لون خلفية
- ✅ شعار النظام (قابل للتغيير)
- ✅ نموذج تسجيل دخول بتصميم Bootstrap 5
- ✅ دعم ثنائية اللغة (عربي/إنجليزي)
- ✅ زر تبديل اللغة في شاشة تسجيل الدخول
- ✅ رابط "نسيت كلمة المرور"
- ✅ رسائل خطأ واضحة
- ✅ تصميم متجاوب (Mobile-First)

### 2️⃣ نموذج إعدادات النظام (System Settings Model)

**apps/core/models.py:**
```python
from django.db import models
from django.core.validators import FileExtensionValidator

class SystemSettings(models.Model):
    """
    إعدادات النظام العامة - Singleton Model
    """
    # معلومات النظام
    site_name_ar = models.CharField(max_length=100, default='نظام CRM')
    site_name_en = models.CharField(max_length=100, default='CRM System')

    # شعار النظام
    logo_ar = models.ImageField(
        upload_to='system/logos/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])],
        null=True,
        blank=True,
        help_text='شعار النظام للعربية'
    )
    logo_en = models.ImageField(
        upload_to='system/logos/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])],
        null=True,
        blank=True,
        help_text='شعار النظام للإنجليزية'
    )

    # خلفية شاشة تسجيل الدخول
    login_background_image = models.ImageField(
        upload_to='system/backgrounds/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        null=True,
        blank=True,
        help_text='صورة خلفية شاشة تسجيل الدخول'
    )
    login_background_color = models.CharField(
        max_length=7,
        default='#0d6efd',
        help_text='لون الخلفية (Hex Color) - يُستخدم إذا لم تكن هناك صورة'
    )
    use_background_image = models.BooleanField(
        default=True,
        help_text='استخدام صورة الخلفية بدلاً من اللون'
    )

    # إعدادات إضافية
    login_page_title_ar = models.CharField(max_length=200, default='مرحباً بك')
    login_page_title_en = models.CharField(max_length=200, default='Welcome')
    login_page_subtitle_ar = models.TextField(default='الرجاء تسجيل الدخول للمتابعة')
    login_page_subtitle_en = models.TextField(default='Please login to continue')

    # Footer
    footer_text_ar = models.CharField(max_length=200, default='جميع الحقوق محفوظة © 2025')
    footer_text_en = models.CharField(max_length=200, default='All Rights Reserved © 2025')

    # تواريخ
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='system_settings_updates'
    )

    class Meta:
        verbose_name = 'إعدادات النظام'
        verbose_name_plural = 'إعدادات النظام'

    def save(self, *args, **kwargs):
        # Singleton Pattern - سجل واحد فقط
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'إعدادات النظام'
```

### 3️⃣ قالب شاشة تسجيل الدخول

**templates/auth/login.html:**
```django
{% load static i18n %}
<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}" dir="{% if LANGUAGE_CODE == 'ar' %}rtl{% else %}ltr{% endif %}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% trans "Login" %} - {{ settings.site_name_ar }}</title>

    <!-- Bootstrap CSS -->
    {% if LANGUAGE_CODE == 'ar' %}
        <link rel="stylesheet" href="{% static 'css/bootstrap.rtl.min.css' %}">
    {% else %}
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
    {% endif %}

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
        body {
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            {% if settings.use_background_image and settings.login_background_image %}
                background-image: url('{{ settings.login_background_image.url }}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            {% else %}
                background: linear-gradient(135deg, {{ settings.login_background_color }} 0%, #0a58ca 100%);
            {% endif %}
            position: relative;
        }

        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.4);
            z-index: 1;
        }

        .login-container {
            position: relative;
            z-index: 2;
            max-width: 450px;
            width: 100%;
            padding: 20px;
        }

        .login-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 40px;
        }

        .logo-container {
            text-align: center;
            margin-bottom: 30px;
        }

        .logo-container img {
            max-height: 80px;
            max-width: 200px;
        }

        .login-title {
            text-align: center;
            margin-bottom: 10px;
            color: #333;
            font-weight: bold;
        }

        .login-subtitle {
            text-align: center;
            margin-bottom: 30px;
            color: #666;
            font-size: 14px;
        }

        .form-control {
            padding: 12px;
            border-radius: 8px;
        }

        .btn-login {
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
        }

        .language-switcher {
            position: absolute;
            top: 20px;
            {% if LANGUAGE_CODE == 'ar' %}
                left: 20px;
            {% else %}
                right: 20px;
            {% endif %}
            z-index: 3;
        }

        .footer-text {
            text-align: center;
            margin-top: 20px;
            color: white;
            font-size: 14px;
        }

        @media (max-width: 576px) {
            .login-card {
                padding: 30px 20px;
            }
        }
    </style>
</head>
<body>
    <!-- Language Switcher -->
    <div class="language-switcher">
        <form action="{% url 'set_language' %}" method="post">
            {% csrf_token %}
            <input name="next" type="hidden" value="{{ request.path }}">
            <select name="language" onchange="this.form.submit()" class="form-select form-select-sm">
                <option value="ar" {% if LANGUAGE_CODE == 'ar' %}selected{% endif %}>🇸🇦 العربية</option>
                <option value="en" {% if LANGUAGE_CODE == 'en' %}selected{% endif %}>🇬🇧 English</option>
            </select>
        </form>
    </div>

    <div class="login-container">
        <div class="login-card">
            <!-- Logo -->
            <div class="logo-container">
                {% if LANGUAGE_CODE == 'ar' and settings.logo_ar %}
                    <img src="{{ settings.logo_ar.url }}" alt="{{ settings.site_name_ar }}">
                {% elif LANGUAGE_CODE == 'en' and settings.logo_en %}
                    <img src="{{ settings.logo_en.url }}" alt="{{ settings.site_name_en }}">
                {% else %}
                    <h2>{{ settings.site_name_ar }}</h2>
                {% endif %}
            </div>

            <!-- Title -->
            <h3 class="login-title">
                {% if LANGUAGE_CODE == 'ar' %}
                    {{ settings.login_page_title_ar }}
                {% else %}
                    {{ settings.login_page_title_en }}
                {% endif %}
            </h3>
            <p class="login-subtitle">
                {% if LANGUAGE_CODE == 'ar' %}
                    {{ settings.login_page_subtitle_ar }}
                {% else %}
                    {{ settings.login_page_subtitle_en }}
                {% endif %}
            </p>

            <!-- Messages -->
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}

            <!-- Login Form -->
            <form method="post" action="{% url 'accounts:login' %}">
                {% csrf_token %}

                <div class="mb-3">
                    <label for="username" class="form-label">
                        <i class="fas fa-user"></i> {% trans "Username or Email" %}
                    </label>
                    <input type="text"
                           class="form-control"
                           id="username"
                           name="username"
                           required
                           autofocus
                           placeholder="{% trans 'Enter your username or email' %}">
                </div>

                <div class="mb-3">
                    <label for="password" class="form-label">
                        <i class="fas fa-lock"></i> {% trans "Password" %}
                    </label>
                    <input type="password"
                           class="form-control"
                           id="password"
                           name="password"
                           required
                           placeholder="{% trans 'Enter your password' %}">
                </div>

                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="remember" name="remember">
                    <label class="form-check-label" for="remember">
                        {% trans "Remember me" %}
                    </label>
                </div>

                <button type="submit" class="btn btn-primary btn-login w-100">
                    <i class="fas fa-sign-in-alt"></i> {% trans "Login" %}
                </button>

                <div class="text-center mt-3">
                    <a href="{% url 'accounts:password_reset' %}" class="text-decoration-none">
                        {% trans "Forgot password?" %}
                    </a>
                </div>
            </form>
        </div>

        <!-- Footer -->
        <p class="footer-text">
            {% if LANGUAGE_CODE == 'ar' %}
                {{ settings.footer_text_ar }}
            {% else %}
                {{ settings.footer_text_en }}
            {% endif %}
        </p>
    </div>

    <!-- Bootstrap JS -->
    <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
</body>
</html>
```

### 4️⃣ Context Processor لإعدادات النظام

**apps/core/context_processors.py:**
```python
from apps.core.models import SystemSettings

def system_settings(request):
    """
    إضافة إعدادات النظام لجميع القوالب
    """
    return {
        'settings': SystemSettings.load()
    }
```

**في config/settings.py:**
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'apps.core.context_processors.system_settings',  # إضافة هنا
            ],
        },
    },
]
```

### 5️⃣ لوحة تحكم مدير النظام لتغيير الإعدادات

**apps/core/admin.py:**
```python
from django.contrib import admin
from django.utils.html import format_html
from .models import SystemSettings

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('معلومات النظام', {
            'fields': ('site_name_ar', 'site_name_en')
        }),
        ('الشعارات', {
            'fields': ('logo_ar', 'logo_en', 'logo_preview')
        }),
        ('خلفية شاشة تسجيل الدخول', {
            'fields': (
                'use_background_image',
                'login_background_image',
                'login_background_color',
                'background_preview'
            ),
            'description': 'يمكنك اختيار صورة خلفية أو لون خلفية لشاشة تسجيل الدخول'
        }),
        ('نصوص شاشة تسجيل الدخول', {
            'fields': (
                'login_page_title_ar',
                'login_page_title_en',
                'login_page_subtitle_ar',
                'login_page_subtitle_en'
            )
        }),
        ('Footer', {
            'fields': ('footer_text_ar', 'footer_text_en')
        }),
    )

    readonly_fields = ('logo_preview', 'background_preview', 'updated_at', 'updated_by')

    def logo_preview(self, obj):
        html = '<div style="display: flex; gap: 20px;">'
        if obj.logo_ar:
            html += f'<div><p>الشعار العربي:</p><img src="{obj.logo_ar.url}" style="max-height: 100px;"></div>'
        if obj.logo_en:
            html += f'<div><p>الشعار الإنجليزي:</p><img src="{obj.logo_en.url}" style="max-height: 100px;"></div>'
        html += '</div>'
        return format_html(html)
    logo_preview.short_description = 'معاينة الشعارات'

    def background_preview(self, obj):
        if obj.use_background_image and obj.login_background_image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 200px; border-radius: 8px;">',
                obj.login_background_image.url
            )
        else:
            return format_html(
                '<div style="width: 200px; height: 100px; background: {}; border-radius: 8px;"></div>',
                obj.login_background_color
            )
    background_preview.short_description = 'معاينة الخلفية'

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        # منع إضافة سجلات جديدة (Singleton)
        return not SystemSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # منع الحذف
        return False
```

### 6️⃣ الوصول إلى لوحة تحكم مدير النظام

**في القائمة المنسدلة للمستخدم (Header):**

```django
<div class="dropdown">
    <a class="nav-link px-3 dropdown-toggle" href="#" id="userDropdown"
       data-bs-toggle="dropdown">
        <img src="{{ user.profile_image.url }}" alt="{{ user.get_full_name }}"
             class="rounded-circle" width="32" height="32">
        {{ user.get_full_name }}
    </a>
    <ul class="dropdown-menu dropdown-menu-end">
        <li><a class="dropdown-item" href="{% url 'accounts:profile' %}">
            <i class="fas fa-user"></i> {% trans "Profile" %}
        </a></li>
        <li><a class="dropdown-item" href="{% url 'accounts:settings' %}">
            <i class="fas fa-cog"></i> {% trans "Settings" %}
        </a></li>

        {% if user.is_superuser or user.is_staff %}
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="{% url 'admin:index' %}">
                <i class="fas fa-tools"></i> {% trans "Admin Panel" %}
            </a></li>
            <li><a class="dropdown-item" href="{% url 'admin:core_systemsettings_change' 1 %}">
                <i class="fas fa-palette"></i> {% trans "System Settings" %}
            </a></li>
        {% endif %}

        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="{% url 'accounts:logout' %}">
            <i class="fas fa-sign-out-alt"></i> {% trans "Logout" %}
        </a></li>
    </ul>
</div>
```

---

## 📝 إنشاء النماذج والقوالب المطلوبة - إلزامي

### 1️⃣ القالب الأساسي (Base Template)

**templates/base.html:**
```django
{% load static i18n %}
<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}" dir="{% if LANGUAGE_CODE == 'ar' %}rtl{% else %}ltr{% endif %}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% trans "CRM System" %}{% endblock %}</title>

    <!-- Bootstrap CSS -->
    {% if LANGUAGE_CODE == 'ar' %}
        <link rel="stylesheet" href="{% static 'css/bootstrap.rtl.min.css' %}">
        <link rel="stylesheet" href="{% static 'css/style-rtl.css' %}">
    {% else %}
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
        <link rel="stylesheet" href="{% static 'css/style-ltr.css' %}">
    {% endif %}

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'css/sidebar.css' %}">
    <link rel="stylesheet" href="{% static 'css/mobile.css' %}">

    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Header الثابت -->
    {% include 'includes/header.html' %}

    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar الثابت -->
            {% include 'includes/sidebar.html' %}

            <!-- Main Content -->
            <main id="main-content" class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                <!-- Breadcrumbs -->
                {% include 'includes/breadcrumbs.html' %}

                <!-- Messages -->
                {% include 'includes/messages.html' %}

                <!-- Loading Indicator -->
                <div id="loading" class="htmx-indicator">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">{% trans "Loading..." %}</span>
                    </div>
                </div>

                <!-- Page Content -->
                {% block content %}{% endblock %}
            </main>
        </div>
    </div>

    <!-- Footer الثابت -->
    {% include 'includes/footer.html' %}

    <!-- Bootstrap JS -->
    <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>

    <!-- HTMX -->
    <script src="{% static 'js/htmx.min.js' %}"></script>

    <!-- Alpine.js -->
    <script src="{% static 'js/alpine.min.js' %}" defer></script>

    <!-- Custom JS -->
    <script src="{% static 'js/main.js' %}"></script>
    <script src="{% static 'js/sidebar.js' %}"></script>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 2️⃣ الهيدر الثابت (Header)

**templates/includes/header.html:**
```django
{% load static i18n %}
<header class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow">
    <a class="navbar-brand col-md-3 col-lg-2 me-0 px-3" href="{% url 'dashboard' %}">
        {% if LANGUAGE_CODE == 'ar' %}
            <img src="{% static 'images/logo-ar.png' %}" alt="CRM" height="40">
        {% else %}
            <img src="{% static 'images/logo-en.png' %}" alt="CRM" height="40">
        {% endif %}
    </a>

    <!-- زر Toggle للقائمة الجانبية -->
    <button class="navbar-toggler position-absolute d-md-none collapsed"
            type="button"
            id="sidebarToggle"
            aria-label="{% trans 'Toggle navigation' %}">
        <span class="navbar-toggler-icon"></span>
    </button>

    <!-- شريط البحث -->
    <input class="form-control form-control-dark w-100"
           type="text"
           placeholder="{% trans 'Search...' %}"
           aria-label="{% trans 'Search' %}"
           hx-get="{% url 'search' %}"
           hx-trigger="keyup changed delay:500ms"
           hx-target="#search-results">

    <div class="navbar-nav">
        <div class="nav-item text-nowrap">
            <!-- تبديل اللغة -->
            <form action="{% url 'set_language' %}" method="post" class="d-inline">
                {% csrf_token %}
                <input name="next" type="hidden" value="{{ request.path }}">
                <select name="language" onchange="this.form.submit()" class="form-select form-select-sm">
                    <option value="ar" {% if LANGUAGE_CODE == 'ar' %}selected{% endif %}>🇸🇦 العربية</option>
                    <option value="en" {% if LANGUAGE_CODE == 'en' %}selected{% endif %}>🇬🇧 English</option>
                </select>
            </form>

            <!-- الإشعارات -->
            <a class="nav-link px-3" href="{% url 'notifications:list' %}">
                <i class="fas fa-bell"></i>
                <span class="badge bg-danger">{{ unread_notifications_count }}</span>
            </a>

            <!-- قائمة المستخدم -->
            <div class="dropdown">
                <a class="nav-link px-3 dropdown-toggle" href="#" id="userDropdown"
                   data-bs-toggle="dropdown">
                    <img src="{{ user.profile_image.url }}" alt="{{ user.get_full_name }}"
                         class="rounded-circle" width="32" height="32">
                    {{ user.get_full_name }}
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="{% url 'accounts:profile' %}">
                        <i class="fas fa-user"></i> {% trans "Profile" %}
                    </a></li>
                    <li><a class="dropdown-item" href="{% url 'accounts:settings' %}">
                        <i class="fas fa-cog"></i> {% trans "Settings" %}
                    </a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="{% url 'accounts:logout' %}">
                        <i class="fas fa-sign-out-alt"></i> {% trans "Logout" %}
                    </a></li>
                </ul>
            </div>
        </div>
    </div>
</header>
```

### 3️⃣ القائمة الجانبية الثابتة (Sidebar)

**templates/includes/sidebar.html:**
```django
{% load static i18n %}
<nav id="sidebar" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
    <div class="position-sticky pt-3">
        <ul class="nav flex-column">
            <!-- Dashboard -->
            <li class="nav-item">
                <a class="nav-link {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}"
                   href="{% url 'dashboard' %}"
                   hx-get="{% url 'dashboard' %}"
                   hx-target="#main-content"
                   hx-push-url="true">
                    <i class="fas fa-tachometer-alt"></i>
                    {% trans "Dashboard" %}
                </a>
            </li>

            <!-- التصاريح -->
            <li class="nav-item">
                <a class="nav-link" data-bs-toggle="collapse" href="#permitsMenu">
                    <i class="fas fa-file-alt"></i>
                    {% trans "Permits" %}
                    <i class="fas fa-chevron-down float-end"></i>
                </a>
                <div class="collapse" id="permitsMenu">
                    <ul class="nav flex-column ms-3">
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'permits:list' %}"
                               hx-get="{% url 'permits:list' %}"
                               hx-target="#main-content"
                               hx-push-url="true">
                                {% trans "All Permits" %}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'permits:create' %}">
                                {% trans "New Permit" %}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'permits:goods' %}">
                                {% trans "Goods Permits" %}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'permits:maintenance' %}">
                                {% trans "Maintenance Permits" %}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'permits:marketing' %}">
                                {% trans "Marketing Permits" %}
                            </a>
                        </li>
                    </ul>
                </div>
            </li>

            <!-- الصيانة -->
            <li class="nav-item">
                <a class="nav-link" data-bs-toggle="collapse" href="#maintenanceMenu">
                    <i class="fas fa-tools"></i>
                    {% trans "Maintenance" %}
                    <i class="fas fa-chevron-down float-end"></i>
                </a>
                <div class="collapse" id="maintenanceMenu">
                    <ul class="nav flex-column ms-3">
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'maintenance:tickets' %}">
                                {% trans "Tickets" %}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'maintenance:create' %}">
                                {% trans "New Ticket" %}
                            </a>
                        </li>
                    </ul>
                </div>
            </li>

            <!-- الشكاوى -->
            <li class="nav-item">
                <a class="nav-link" href="{% url 'complaints:list' %}"
                   hx-get="{% url 'complaints:list' %}"
                   hx-target="#main-content"
                   hx-push-url="true">
                    <i class="fas fa-comments"></i>
                    {% trans "Complaints" %}
                </a>
            </li>

            <!-- التسويق -->
            <li class="nav-item">
                <a class="nav-link" href="{% url 'marketing:list' %}">
                    <i class="fas fa-bullhorn"></i>
                    {% trans "Marketing" %}
                </a>
            </li>

            <!-- الموارد البشرية -->
            <li class="nav-item">
                <a class="nav-link" data-bs-toggle="collapse" href="#hrMenu">
                    <i class="fas fa-users"></i>
                    {% trans "HR" %}
                    <i class="fas fa-chevron-down float-end"></i>
                </a>
                <div class="collapse" id="hrMenu">
                    <ul class="nav flex-column ms-3">
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'hr:leave_requests' %}">
                                {% trans "Leave Requests" %}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'hr:employees' %}">
                                {% trans "Employees" %}
                            </a>
                        </li>
                    </ul>
                </div>
            </li>

            <!-- التقارير -->
            <li class="nav-item">
                <a class="nav-link" href="{% url 'reports:index' %}">
                    <i class="fas fa-chart-bar"></i>
                    {% trans "Reports" %}
                </a>
            </li>

            <!-- الإعدادات -->
            <li class="nav-item">
                <a class="nav-link" href="{% url 'settings:index' %}">
                    <i class="fas fa-cog"></i>
                    {% trans "Settings" %}
                </a>
            </li>
        </ul>
    </div>
</nav>
```

### 4️⃣ الفوتر الثابت (Footer)

**templates/includes/footer.html:**
```django
{% load static i18n %}
<footer class="footer mt-auto py-3 bg-light">
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-6">
                <span class="text-muted">
                    © 2025 {% trans "CRM System" %} - {% trans "All Rights Reserved" %}
                </span>
            </div>
            <div class="col-md-6 text-end">
                <a href="{% url 'support' %}" class="text-muted me-3">{% trans "Support" %}</a>
                <a href="{% url 'terms' %}" class="text-muted me-3">{% trans "Terms" %}</a>
                <a href="{% url 'privacy' %}" class="text-muted me-3">{% trans "Privacy" %}</a>
                <span class="text-muted">{% trans "Version" %} 1.0.0</span>
            </div>
        </div>
    </div>
</footer>
```

### 5️⃣ نموذج قائمة التصاريح (Permits List)

**templates/permits/permit_list.html:**
```django
{% extends 'base.html' %}
{% load static i18n %}

{% block title %}{% trans "Permits" %}{% endblock %}

{% block content %}
<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">{% trans "Permits" %}</h1>
    <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group me-2">
            <a href="{% url 'permits:export' %}" class="btn btn-sm btn-success">
                <i class="fas fa-file-excel"></i> {% trans "Export" %}
            </a>
            <button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#importModal">
                <i class="fas fa-file-upload"></i> {% trans "Import" %}
            </button>
        </div>
        <a href="{% url 'permits:create' %}" class="btn btn-sm btn-primary">
            <i class="fas fa-plus"></i> {% trans "New Permit" %}
        </a>
    </div>
</div>

<!-- Filters -->
<div class="card mb-3">
    <div class="card-body">
        <form method="get" hx-get="{% url 'permits:list' %}" hx-target="#permits-table" hx-trigger="change">
            <div class="row">
                <div class="col-md-3">
                    <label>{% trans "Status" %}</label>
                    <select name="status" class="form-select">
                        <option value="">{% trans "All" %}</option>
                        <option value="pending">{% trans "Pending" %}</option>
                        <option value="approved">{% trans "Approved" %}</option>
                        <option value="rejected">{% trans "Rejected" %}</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label>{% trans "Type" %}</label>
                    <select name="permit_type" class="form-select">
                        <option value="">{% trans "All" %}</option>
                        <option value="goods">{% trans "Goods" %}</option>
                        <option value="maintenance">{% trans "Maintenance" %}</option>
                        <option value="marketing">{% trans "Marketing" %}</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label>{% trans "From Date" %}</label>
                    <input type="date" name="date_from" class="form-control">
                </div>
                <div class="col-md-3">
                    <label>{% trans "To Date" %}</label>
                    <input type="date" name="date_to" class="form-control">
                </div>
            </div>
        </form>
    </div>
</div>

<!-- Table -->
<div id="permits-table">
    {% include 'permits/partials/permits_table.html' %}
</div>
{% endblock %}
```

### 6️⃣ نموذج إنشاء تصريح (Permit Form)

**templates/permits/permit_form.html:**
```django
{% extends 'base.html' %}
{% load static i18n crispy_forms_tags %}

{% block title %}{% trans "New Permit" %}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8 offset-md-2">
        <div class="card">
            <div class="card-header">
                <h3>{% trans "Create New Permit" %}</h3>
            </div>
            <div class="card-body">
                <form method="post" enctype="multipart/form-data"
                      hx-post="{% url 'permits:create' %}"
                      hx-target="#form-result">
                    {% csrf_token %}

                    {{ form|crispy }}

                    <div id="form-result"></div>

                    <div class="mt-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save"></i> {% trans "Save" %}
                        </button>
                        <a href="{% url 'permits:list' %}" class="btn btn-secondary">
                            <i class="fas fa-times"></i> {% trans "Cancel" %}
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## �️ إعدادات قاعدة البيانات - SQLite للتطوير / PostgreSQL للإنتاج

### 1️⃣ إعداد SQLite للتطوير

**config/settings_dev.py:**
```python
from .settings import *

DEBUG = True

# قاعدة بيانات SQLite للتطوير
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# تعطيل HTTPS للتطوير
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# إعدادات البريد الإلكتروني للتطوير (Console Backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 2️⃣ إعداد PostgreSQL للإنتاج

**config/settings_prod.py:**
```python
from .settings import *
import dj_database_url

DEBUG = False

# قاعدة بيانات PostgreSQL للإنتاج
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://crm_user:password@localhost:5432/crm_db',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# إعدادات الأمان للإنتاج
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# إعدادات البريد الإلكتروني للإنتاج
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
```

### 3️⃣ الإعدادات الأساسية المشتركة

**config/settings.py:**
```python
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Applications
INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    'import_export',
    'guardian',
    'notifications',

    # Custom Apps
    'apps.accounts',
    'apps.permits',
    'apps.maintenance',
    'apps.complaints',
    'apps.marketing',
    'apps.hr',
    'apps.notifications',
    'apps.reports',
    'apps.core',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # للترجمة
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Internationalization (ثنائية اللغة)
LANGUAGE_CODE = 'ar'
LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Asia/Riyadh'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # للترجمة
            ],
        },
    },
]

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Redis Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://127.0.0.1:6379/1')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://127.0.0.1:6379/1')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
```

### 4️⃣ ملف المتغيرات البيئية

**.env.example:**
```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (للتطوير - SQLite)
# لا حاجة لإعدادات قاعدة البيانات مع SQLite

# Database (للإنتاج - PostgreSQL)
# DATABASE_URL=postgresql://crm_user:password@localhost:5432/crm_db

# Redis
REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/1
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Language
LANGUAGE_CODE=ar
```

### 5️⃣ أوامر التشغيل

**للتطوير (SQLite):**
```bash
# تفعيل البيئة الافتراضية
source venv/bin/activate

# تطبيق الهجرات
python manage.py migrate

# إنشاء مستخدم إداري
python manage.py createsuperuser

# تشغيل الخادم
python manage.py runserver --settings=config.settings_dev
```

**للإنتاج (PostgreSQL):**
```bash
# إنشاء قاعدة البيانات
createdb crm_db

# تطبيق الهجرات
python manage.py migrate --settings=config.settings_prod

# جمع الملفات الثابتة
python manage.py collectstatic --noinput --settings=config.settings_prod

# تشغيل مع Gunicorn
gunicorn config.wsgi:application --settings=config.settings_prod
```

### 6️⃣ سكريبت الانتقال من SQLite إلى PostgreSQL

**scripts/migrate_to_postgres.py:**
```python
"""
سكريبت للانتقال من SQLite إلى PostgreSQL
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_dev')
django.setup()

from django.core.management import call_command

def migrate_to_postgres():
    print("1. تصدير البيانات من SQLite...")
    call_command('dumpdata', '--natural-foreign', '--natural-primary',
                 '--exclude=contenttypes', '--exclude=auth.permission',
                 '--output=data_backup.json')

    print("2. تغيير الإعدادات إلى PostgreSQL...")
    print("   يرجى تحديث DJANGO_SETTINGS_MODULE إلى config.settings_prod")

    print("3. تطبيق الهجرات على PostgreSQL...")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_prod'
    call_command('migrate')

    print("4. استيراد البيانات إلى PostgreSQL...")
    call_command('loaddata', 'data_backup.json')

    print("✅ تم الانتقال بنجاح!")

if __name__ == '__main__':
    migrate_to_postgres()
```

---

## 🚀 متطلبات الأداء

### 1️⃣ Caching مع Redis
```python
# في views.py
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@cache_page(60 * 15)  # Cache لمدة 15 دقيقة
def permit_list(request):
    permits = cache.get('permits_list')
    if not permits:
        permits = Permit.objects.all()
        cache.set('permits_list', permits, 60 * 15)
    return render(request, 'permits/list.html', {'permits': permits})
```

### 2️⃣ Database Indexing
```python
# في models.py
class Permit(models.Model):
    permit_number = models.CharField(max_length=50, unique=True, db_index=True)
    status = models.CharField(max_length=20, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['permit_type', 'status']),
        ]
```

### 3️⃣ Query Optimization
```python
# استخدام select_related و prefetch_related
permits = Permit.objects.select_related('created_by', 'department').prefetch_related('approvals')

# استخدام only و defer
permits = Permit.objects.only('id', 'permit_number', 'title', 'status')
```

### 4️⃣ Lazy Loading للصور
```html
<!-- في templates -->
<img src="{{ permit.image.url }}" loading="lazy" alt="{{ permit.title }}">
```

### 5️⃣ Compression للاستجابات
```python
# في settings.py
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',  # إضافة في البداية
    ...
]
```

### 6️⃣ CDN للملفات الثابتة (اختياري)
```python
# في settings_prod.py
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

---

## 📝 الخطوات التنفيذية

### المرحلة 1: الإعداد
1. إنشاء مشروع Django
2. تثبيت جميع المكتبات
3. إعداد قاعدة البيانات
4. إعداد Bootstrap + HTMX

### المرحلة 2: نظام المستخدمين
1. Custom User Model
2. الأقسام
3. الصلاحيات
4. المصادقة

### المرحلة 3: الأنظمة الفرعية
1. نظام التصاريح
2. نظام الصيانة
3. نظام الشكاوى
4. نظام التسويق
5. نظام الموارد البشرية

### المرحلة 4: الواجهات
1. Dashboard
2. Forms مع HTMX
3. Tables مع Filtering
4. Notifications

### المرحلة 5: التقارير والتحسينات
1. التقارير
2. الإحصائيات
3. التحسينات
4. الاختبارات

---

## 🎯 الخلاصة

هذا النظام يجب أن يكون:
- ✅ **شامل** - يغطي جميع العمليات
- ✅ **سريع** - أداء عالي مع HTMX
- ✅ **آمن** - حماية كاملة
- ✅ **سهل الاستخدام** - واجهة بديهية
- ✅ **قابل للتوسع** - معماري جيد
- ✅ **موثق** - توثيق كامل

---

## 📋 التطابق مع ملف SYSTEM_ARCHITECTURE.md - إلزامي

### ⚠️ تعليمات مهمة جداً:

يجب أن يتطابق المشروع المُنشأ **بشكل كامل** مع المعمارية الموضحة في ملف:
```
/home/zakee/crm/SYSTEM_ARCHITECTURE.md
```

### 1️⃣ هيكل المشروع

يجب أن يتطابق هيكل المجلدات والملفات **تماماً** مع الهيكل الموضح في SYSTEM_ARCHITECTURE.md

### 2️⃣ تدفق البيانات (Data Flow)

يجب تطبيق تدفق البيانات الموضح في SYSTEM_ARCHITECTURE.md:

**طلب المستخدم:**
```
User Browser → NGINX → Gunicorn → Django → View → Model → PostgreSQL
```

**استجابة HTMX:**
```
User Action → HTMX Request → Django View → Partial Template → HTML Fragment → HTMX Swap
```

**المهام الخلفية:**
```
User Action → Django View → Celery Task → Redis → Celery Worker → Execute Task
```

### 3️⃣ قاعدة البيانات

يجب إنشاء جميع الجداول الموضحة في SYSTEM_ARCHITECTURE.md:

**Users & Authentication:**
- accounts_customuser
- accounts_department
- accounts_tenantprofile

**Permits:**
- permits_permit
- permits_permitattachment
- permits_permitapproval
- permits_memo
- permits_penalty
- permits_announcement
- permits_invoice

**Maintenance:**
- maintenance_ticket
- maintenance_ticketattachment
- maintenance_ticketcomment
- maintenance_ticketfeedback

**Complaints:**
- complaints_case
- complaints_caseattachment
- complaints_casecomment

**Marketing:**
- marketing_permit
- marketing_permitattachment
- marketing_permitapproval

**HR:**
- hr_leaverequest
- hr_leaverequestattachment
- hr_leavebalance

**Notifications:**
- notifications_notification
- notifications_emaillog

### 4️⃣ طبقة الأمان

يجب تطبيق جميع متطلبات الأمان الموضحة في SYSTEM_ARCHITECTURE.md:

- ✅ Django's built-in authentication
- ✅ Session-based authentication
- ✅ Django Permissions + Django Guardian
- ✅ CSRF Protection
- ✅ XSS Protection
- ✅ SQL Injection Protection
- ✅ Secure Password Hashing (PBKDF2)
- ✅ File Upload Security

### 5️⃣ طبقة التخزين المؤقت (Caching)

يجب تطبيق استراتيجية Caching الموضحة في SYSTEM_ARCHITECTURE.md

### 6️⃣ API Layer

يجب تطبيق API Layer الموضح في SYSTEM_ARCHITECTURE.md:

- ✅ Django REST Framework
- ✅ Token Authentication
- ✅ Serializers لجميع Models
- ✅ ViewSets
- ✅ Pagination
- ✅ Filtering & Search
- ✅ API Documentation (Swagger/ReDoc)

### 7️⃣ Background Tasks

يجب تطبيق Celery Tasks الموضحة في SYSTEM_ARCHITECTURE.md

### 8️⃣ Deployment Architecture

يجب اتباع معمارية النشر الموضحة في SYSTEM_ARCHITECTURE.md:

**Production Stack:**
```
Internet → NGINX → Gunicorn → Django → PostgreSQL + Redis + Celery Workers
```

### 9️⃣ Monitoring & Logging

يجب تطبيق Monitoring & Logging الموضح في SYSTEM_ARCHITECTURE.md

### 🔟 Testing Strategy

يجب اتباع استراتيجية الاختبار الموضحة في SYSTEM_ARCHITECTURE.md:

- ✅ Unit Tests لجميع Models
- ✅ Integration Tests لجميع Views
- ✅ API Tests لجميع Endpoints
- ✅ Coverage > 80%

### ✅ قائمة التحقق النهائية

قبل اعتبار المشروع مكتملاً، تأكد من:

- [ ] هيكل المجلدات يطابق SYSTEM_ARCHITECTURE.md بنسبة 100%
- [ ] جميع Models المذكورة في SYSTEM_ARCHITECTURE.md تم إنشاؤها
- [ ] تدفق البيانات يطابق المخططات في SYSTEM_ARCHITECTURE.md
- [ ] طبقة الأمان مطبقة بالكامل
- [ ] Caching Strategy مطبقة
- [ ] API Layer مطبق بالكامل
- [ ] Celery Tasks مطبقة
- [ ] Deployment Architecture جاهزة
- [ ] Monitoring & Logging مطبق
- [ ] Tests مكتوبة ونسبة التغطية > 80%
- [ ] شاشة تسجيل الدخول المخصصة مع خلفية قابلة للتغيير ✅
- [ ] لوحة تحكم مدير النظام للإعدادات ✅
- [ ] ثنائية اللغة مطبقة بالكامل ✅
- [ ] واجهة متجاوبة 100% ✅
- [ ] استيراد/تصدير Excel لجميع الجداول ✅

---

**ملاحظة**: هذا البرومبت يعتمد على التحليل الشامل لملف Excel المرفق ويغطي جميع الوحدات والعمليات المطلوبة **ويتطابق بشكل كامل مع SYSTEM_ARCHITECTURE.md**.

**ملاحظات مهمة:**
- ✅ استخدم **SQLite** للتطوير السريع
- ✅ جهّز للانتقال إلى **PostgreSQL** للإنتاج
- ✅ اتبع **Best Practices** في Django
- ✅ اكتب **Tests** لكل وظيفة
- ✅ وثّق الكود بشكل جيد
- ✅ استخدم **Git** لإدارة الإصدارات
- ✅ **تطابق كامل مع SYSTEM_ARCHITECTURE.md**
- ✅ شاشة تسجيل دخول احترافية مع خلفية قابلة للتغيير
- ✅ لوحة تحكم مدير النظام متاحة من القائمة المنسدلة للمستخدم

---

**تاريخ الإنشاء**: 2025-10-20
**آخر تحديث**: 2025-10-25
**الإصدار**: 2.0.0
**الحالة**: ✅ جاهز للتنفيذ
**التطابق مع SYSTEM_ARCHITECTURE.md**: ✅ مؤكد
**شاشة تسجيل الدخول المخصصة**: ✅ مؤكد
**لوحة تحكم مدير النظام**: ✅ مؤكد

---

## 📊 حالة التنفيذ - Implementation Status

### ✅ الميزات المكتملة (Completed Features)

#### 1. البنية الأساسية (Core Infrastructure) - 100%
- ✅ Django 5.0.14 + Python 3.13.7
- ✅ 8 تطبيقات Django (core, accounts, permits, maintenance, complaints, marketing, hr, finance)
- ✅ 21 نموذج بيانات (Models)
- ✅ SQLite Database مع Migrations
- ✅ Bootstrap 5.3 + HTMX 1.9
- ✅ نظام الترجمة الثنائي (عربي/إنجليزي) - 600+ ترجمة

#### 2. نظام المستخدمين (User Management) - 100%
- ✅ CustomUser Model
- ✅ Department Model (10 أقسام)
- ✅ TenantProfile Model (معلومات المستأجر الكاملة)
- ✅ django-allauth للمصادقة
- ✅ 26 مستخدم افتراضي (19 موظف + 5 مستأجرين + 2 إداريين)

#### 3. واجهة المستأجر (Tenant Interface) - 100%
- ✅ لوحة تحكم مخصصة (`/tenant/dashboard/`)
- ✅ صفحة الملف الشخصي (`/tenant/profile/`)
- ✅ عرض الفواتير (`/tenant/invoices/`)
- ✅ عرض التصاريح (`/tenant/permits/`)
- ✅ إحصائيات شاملة (تصاريح، تذاكر، فواتير، شكاوى)
- ✅ إجراءات سريعة (تصريح جديد، طلب صيانة، شكوى جديدة)

#### 4. القسم المالي (Finance Module) - 100%
- ✅ Invoice Model (5 أنواع، 6 حالات)
- ✅ InvoiceItem Model (بنود الفاتورة)
- ✅ Payment Model (6 طرق دفع)
- ✅ حساب تلقائي للضرائب والخصومات
- ✅ Admin interface مع inline editing
- ✅ جميع المبالغ بالدولار (USD)

#### 5. نظام العملة والتاريخ (Currency & Date System) - 100%
- ✅ SystemSettings Model مع إعدادات العملة
- ✅ 5 عملات مدعومة (USD, EUR, GBP, SAR, AED)
- ✅ رموز العملة دائماً بالإنجليزية ($, €, £, etc.)
- ✅ التاريخ دائماً ميلادي بالإنجليزية (MM/DD/YYYY)
- ✅ Template Filters (`{{ amount|currency }}`, `{{ amount|currency_code }}`)
- ✅ Context Processor للوصول العام

#### 6. نظام التصاريح (Permits Module) - 100%
- ✅ Permit Model (3 أنواع، 3 اتجاهات، 5 حالات)
- ✅ PermitApproval Model (نظام الموافقات)
- ✅ Forms + Views + Templates
- ✅ Excel Import/Export
- ✅ ترجمة كاملة

#### 7. نظام الصيانة (Maintenance Module) - 100%
- ✅ Ticket Model (5 فئات، 3 أولويات، 5 حالات)
- ✅ Forms + Views + Templates
- ✅ Excel Import/Export
- ✅ ترجمة كاملة

#### 8. نظام الشكاوى (Complaints Module) - 100%
- ✅ Case Model (3 أنواع، 3 أولويات، 4 حالات)
- ✅ Forms + Views + Templates
- ✅ Excel Import/Export
- ✅ ترجمة كاملة

#### 9. نظام التسويق (Marketing Module) - 100%
- ✅ Event Model (3 أنواع، 4 حالات)
- ✅ Forms + Views + Templates
- ✅ Excel Import/Export
- ✅ ترجمة كاملة

#### 10. نظام الموارد البشرية (HR Module) - 100%
- ✅ LeaveRequest Model (6 أنواع، 3 حالات)
- ✅ Forms + Views + Templates
- ✅ Excel Import/Export
- ✅ ترجمة كاملة

### ⏳ الميزات قيد التطوير (In Progress)

#### 1. نظام الموافقات (Approval Workflow) - 30%
- ✅ PermitApproval Model موجود
- ❌ Workflow Logic (workflows.py)
- ❌ Multi-stage Approval Views
- ❌ Approval Templates
- ❌ Email Notifications

#### 2. نظام الإشعارات (Notifications System) - 0%
- ❌ Notification Model
- ❌ Email Notifications
- ❌ In-App Notifications
- ❌ Real-time Updates

#### 3. نظام التقارير (Reports System) - 20%
- ✅ Excel Export موجود
- ❌ PDF Export
- ❌ Custom Reports
- ❌ Charts & Analytics
- ❌ Dashboard Analytics

### 📈 الإحصائيات

- **إجمالي الملفات**: 150+
- **إجمالي الأسطر البرمجية**: 15,000+
- **Models**: 21
- **Views**: 32
- **Templates**: 28
- **Forms**: 15
- **URLs**: 8 apps
- **Translations**: 600+ pairs
- **Users**: 26 (sample data)
- **Departments**: 10

### 🎯 الخطوات التالية (Next Steps)

1. **إكمال نظام الموافقات** (High Priority)
   - إنشاء workflows.py
   - إضافة views للموافقة/الرفض
   - إنشاء templates للموافقات
   - تفعيل الإشعارات

2. **نظام الإشعارات** (Medium Priority)
   - تثبيت django-notifications-hq
   - إنشاء Notification Model
   - إضافة Email Notifications
   - إضافة In-App Notifications

3. **نظام التقارير المتقدم** (Low Priority)
   - PDF Export
   - Custom Reports
   - Charts & Analytics
   - Dashboard Widgets

---

