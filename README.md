# ✦ نيورا AI — مساعد ذكاء اصطناعي متكامل

تطبيق ويب يشبه ChatGPT مع دعم إنشاء صور واقعية / أنمي / أنيميشن.

## 🚀 التشغيل المحلي

```bash
# 1. استنساخ المشروع
git clone <your-repo-url>
cd ai-chat-app

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. إضافة مفتاح OpenAI
export OPENAI_API_KEY=sk-...

# 4. تشغيل التطبيق
python app.py
```

افتح المتصفح على: http://localhost:5000

## ☁️ النشر على Render

1. ارفع المشروع على GitHub
2. افتح [render.com](https://render.com) وأنشئ **Web Service** جديد
3. اربطه بمستودعك
4. أضف متغير البيئة: `OPENAI_API_KEY` = مفتاحك
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn app:app`

## 📁 هيكل الملفات

```
ai-chat-app/
├── app.py              # الخادم Flask
├── requirements.txt    # مكتبات Python
├── render.yaml         # إعدادات Render
├── .gitignore
├── README.md
└── templates/
    └── index.html      # واجهة المستخدم
```

## ✨ المميزات

- 💬 محادثة ذكية مع GPT-4o Mini
- 🖼️ إنشاء صور بـ DALL·E 3 HD
- 🎨 3 أنماط: واقعي / أنمي / أنيميشن
- 🌙 تصميم داكن أنيق
- 📱 متوافق مع الجوال
- 🔒 قراءة المفتاح من Environment Variable
