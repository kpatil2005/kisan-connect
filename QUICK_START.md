# 🚀 Quick Start - Language Switching

## ✅ What's Already Done:

1. Language modal is working
2. Hindi translations are compiled
3. Hero section has translation tags
4. URL routing is configured

## 🔧 Fix 404 Error & Test Language Switching:

### Step 1: Restart Server
```bash
# Stop current server (Ctrl+C)
python manage.py runserver
```

### Step 2: Test Language Switching
1. Visit: `http://127.0.0.1:8000/`
2. Click language button (shows "English")
3. Select "हिन्दी (Hindi)"
4. Hero text should change to Hindi!

## 📥 Install Gettext Tools (3 Easy Options):

### Option 1: Using Chocolatey (EASIEST - Recommended)

**Step 1:** Open PowerShell as Administrator

**Step 2:** Install Chocolatey (if not installed):
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

**Step 3:** Install gettext:
```powershell
choco install gettext -y
```

**Step 4:** Restart terminal and verify:
```bash
msgfmt --version
```

### Option 2: Manual Download (FAST)

1. Download: https://github.com/mlocati/gettext-iconv-windows/releases
2. Get: `gettext0.21-iconv1.16-static-64.exe`
3. Run installer
4. Add to PATH: `C:\Program Files\gettext-iconv\bin`
5. Restart terminal

### Option 3: Use Git Bash (If you have Git)

Git for Windows includes gettext!

Add to PATH: `C:\Program Files\Git\usr\bin`

## 🎯 After Installing Gettext:

### Generate translation files:
```bash
python manage.py makemessages -l hi -l ta -l te -l bn -l mr -l kn -l ml -l pa
```

### Compile translations:
```bash
python manage.py compilemessages
```

## 🔄 Without Gettext (Current Workaround):

You can still use the manual compiler:

```bash
python compile_translations_manual.py
```

## 📝 Add More Translations:

### 1. Edit translation file:
`locale/hi/LC_MESSAGES/django.po`

### 2. Add translations:
```po
msgid "Welcome"
msgstr "स्वागत है"

msgid "Products"
msgstr "उत्पाद"
```

### 3. Compile:
```bash
python compile_translations_manual.py
```

### 4. Restart server:
```bash
python manage.py runserver
```

## 🐛 Troubleshooting:

### 404 Error on Language Switch:
- ✅ Fixed! I updated the form action to `/i18n/setlang/`
- Restart your server

### Text Not Changing:
- Make sure text is wrapped in `{% trans "text" %}`
- Translation must exist in .po file
- Translations must be compiled (.mo file)
- Server must be restarted

### Language Button Not Showing:
- Clear browser cache (Ctrl+Shift+R)
- Check browser console for errors

## 📚 Files You Need to Know:

- `locale/hi/LC_MESSAGES/django.po` - Edit translations here
- `locale/hi/LC_MESSAGES/django.mo` - Compiled (auto-generated)
- `compile_translations_manual.py` - Manual compiler
- `install_gettext.bat` - Gettext installer

## 🎉 Test Now:

1. Restart server: `python manage.py runserver`
2. Visit: `http://127.0.0.1:8000/`
3. Click language button
4. Select Hindi
5. See translated text!

---

**Need help?** Check the browser console (F12) for specific error messages.
