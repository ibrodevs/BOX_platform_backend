# 🚀 Backend готов к деплою на Render.com!

## Быстрый старт:

### 1. Загрузите код на GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push
```

### 2. Создайте Web Service на Render.com
- Dashboard → New + → Web Service
- Подключите GitHub репозиторий
- Root Directory: `backend`
- Build Command: `chmod +x build.sh && ./build.sh`
- Start Command: `gunicorn boxer_platform.wsgi:application`

### 3. Создайте PostgreSQL Database
- Dashboard → New + → PostgreSQL
- Имя: `boxer-platform-db`
- Скопируйте Internal Database URL

### 4. Настройте Environment Variables:
```
SECRET_KEY = [сгенерируйте на https://djecrety.ir/]
DEBUG = False
DATABASE_URL = [Internal Database URL из PostgreSQL]
ALLOWED_HOSTS = your-app.onrender.com
CORS_ALLOWED_ORIGINS = https://your-frontend.com
DJANGO_SUPERUSER_PASSWORD = 12345678
```

**Суперпользователь (логин: admin, email: admin@bivolboxing.com) будет создан автоматически!**

### 5. Deploy!
Render автоматически начнет деплой. Готово через 3-5 минут!

---

## 📚 Документация:
- **Полная инструкция по деплою:** `RENDER_DEPLOYMENT.md`
- **Настройка администратора:** `ADMIN_SETUP.md` 👨‍💼

## 🔧 Созданные файлы:
- ✅ `build.sh` - скрипт сборки
- ✅ `render.yaml` - конфигурация Render
- ✅ `runtime.txt` - версия Python
- ✅ `requirements.txt` - обновлен с production зависимостями
- ✅ `settings.py` - настроен для production

## 🎯 Ваш API будет доступен:
`https://your-app-name.onrender.com/api/`
