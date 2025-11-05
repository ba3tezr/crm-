# نشر مشروع Django على Railway

## الخطوات الأساسية:

1. تأكد من وجود الملفات التالية في جذر المشروع:
   - requirements.txt (يحتوي جميع الحزم المطلوبة)
   - manage.py
   - config/settings.py (أو settings.py في جذر المشروع)
   - Procfile (لإخبار Railway بكيفية تشغيل التطبيق)

2. أضف ملف Procfile في جذر المشروع بهذا المحتوى:

```
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application
```

3. تأكد من وجود gunicorn في requirements.txt:

```
gunicorn>=21.2.0
```

4. ادفع جميع التغييرات إلى GitHub.

5. اربط مستودعك بحساب Railway (Import from GitHub).

6. أضف متغيرات البيئة من إعدادات Railway:
   - SECRET_KEY
   - DEBUG (اجعلها False)
   - ALLOWED_HOSTS (اجعلها *)
   - DATABASE_URL (يمكنك استخدام قاعدة بيانات PostgreSQL المجانية من Railway)

7. بعد النشر، افتح الرابط الذي توفره Railway للتحقق من عمل التطبيق.

## ملاحظات:
- Railway يدعم Django بشكل كامل (جلسات، قواعد بيانات، ملفات static/media).
- يمكنك إدارة قاعدة البيانات مباشرة من لوحة التحكم Railway.
- إذا ظهرت أي أخطاء أثناء البناء أو التشغيل، راجع سجل البناء (Build Logs) وأرسل لي رسالة الخطأ لأساعدك في حلها.
