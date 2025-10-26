# دليل النشر والتشغيل - Deployment Guide

## التشغيل السريع مع رابط مؤقت - Quick Start with Temporary URL

### الطريقة 1: استخدام السكريبت الكامل (موصى به)

```bash
./run.sh
```

هذا السكريبت سيقوم بـ:
- ✅ تفعيل البيئة الافتراضية
- ✅ تثبيت المكتبات المطلوبة (إذا لم تكن مثبتة)
- ✅ تشغيل migrations
- ✅ جمع الملفات الثابتة
- ✅ تجميع الترجمات
- ✅ تشغيل خادم Django
- ✅ إنشاء رابط مؤقت عبر Cloudflare Tunnel
- ✅ عرض الرابط العام للتطبيق

### الطريقة 2: استخدام السكريبت البسيط

```bash
./start.sh
```

هذا السكريبت أبسط ويقوم فقط بـ:
- ✅ تشغيل خادم Django
- ✅ إنشاء رابط مؤقت عبر Cloudflare Tunnel

### الطريقة 3: التشغيل اليدوي

```bash
# 1. تفعيل البيئة الافتراضية
source venv/bin/activate

# 2. تشغيل خادم Django
python manage.py runserver 0.0.0.0:8000 &

# 3. إنشاء رابط مؤقت
cloudflared tunnel --url http://localhost:8000
```

---

## معلومات الدخول - Login Credentials

### حساب المدير - Admin Account
```
Username: admin
Password: admin123
URL: /admin/
```

### حساب مستأجر تجريبي - Test Tenant Account
```
Username: majed
Password: majed123
Tenant ID: TNT1004
```

### حسابات موظفين تجريبية - Test Staff Accounts
```
Username: ahmed
Password: ahmed123
Department: IT

Username: fatima
Password: fatima123
Department: Finance
```

---

## ملاحظات مهمة - Important Notes

### 🔒 الأمان - Security

⚠️ **تحذير**: هذا الإعداد للتطوير والاختبار فقط!

للإنتاج، يجب:
1. تغيير `SECRET_KEY` في `.env`
2. تعيين `DEBUG=False`
3. استخدام قاعدة بيانات PostgreSQL
4. إعداد HTTPS
5. تغيير جميع كلمات المرور الافتراضية

### 🌐 الرابط المؤقت - Temporary URL

- الرابط المؤقت من Cloudflare صالح فقط أثناء تشغيل السكريبت
- عند إيقاف السكريبت (Ctrl+C)، سيتوقف الرابط عن العمل
- في كل مرة تشغل السكريبت، ستحصل على رابط جديد
- الرابط يكون بصيغة: `https://xxxxx.trycloudflare.com`

### 📱 الوصول - Access

بعد تشغيل السكريبت، ستحصل على:
```
🌐 Public URL: https://xxxxx.trycloudflare.com

📋 Default Credentials:
   Username: admin
   Password: admin123

📋 Test Tenant:
   Username: majed
   Password: majed123
```

يمكنك مشاركة الرابط مع أي شخص للاختبار!

---

## إيقاف التطبيق - Stop Application

لإيقاف التطبيق، اضغط:
```
Ctrl + C
```

سيتم إيقاف:
- ✅ خادم Django
- ✅ Cloudflare Tunnel
- ✅ الرابط المؤقت

---

## استكشاف الأخطاء - Troubleshooting

### المشكلة: cloudflared غير مثبت

**الحل لـ Ubuntu/Debian:**
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

**الحل لـ macOS:**
```bash
brew install cloudflared
```

### المشكلة: المنفذ 8000 مستخدم

**الحل:**
```bash
# إيقاف العملية على المنفذ 8000
lsof -ti:8000 | xargs kill -9

# ثم أعد تشغيل السكريبت
./run.sh
```

### المشكلة: خطأ في الترجمات

**الحل:**
```bash
python manage.py compilemessages
```

### المشكلة: خطأ في قاعدة البيانات

**الحل:**
```bash
python manage.py migrate
```

---

## النشر على خادم حقيقي - Production Deployment

للنشر على خادم حقيقي، راجع:
- [دليل النشر على Heroku](https://devcenter.heroku.com/articles/django-app-configuration)
- [دليل النشر على DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu)
- [دليل النشر على AWS](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)

---

## الدعم - Support

للمساعدة أو الإبلاغ عن مشاكل:
- 📧 Email: support@example.com
- 🐛 GitHub Issues: https://github.com/ba3tezr/crm-/issues

---

## الترخيص - License

هذا المشروع مفتوح المصدر ومتاح للاستخدام الشخصي والتجاري.

