# Multi-Language Setup Guide for Kisan Connect

## ✅ Configuration Complete

Django i18n is now configured with support for 12 Indian languages:
- English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese

## 🚀 Next Steps

### 1. Mark Strings for Translation in Templates

Add `{% load i18n %}` at the top of each template, then wrap text:

```django
{% load i18n %}

<!-- Simple text -->
<h1>{% trans "Welcome to Kisan Connect" %}</h1>

<!-- With variables -->
<p>{% blocktrans with price=product.price %}Price: ₹{{ price }}{% endblocktrans %}</p>

<!-- Buttons and links -->
<button>{% trans "Add to Cart" %}</button>
<a href="#">{% trans "View Products" %}</a>
```

### 2. Mark Strings in Python Code (views.py, models.py)

```python
from django.utils.translation import gettext_lazy as _

# In models
class Product(models.Model):
    name = models.CharField(_("Product Name"), max_length=100)
    
# In views
messages.success(request, _("Product added to cart successfully!"))

# In forms
class ContactForm(forms.Form):
    name = forms.CharField(label=_("Your Name"))
```

### 3. Generate Translation Files

Run this command to create .po files for all languages:

```bash
cd Plant_Disease_Dataset\Plant_Disease_Dataset\ec
python manage.py makemessages -l hi -l ta -l te -l bn -l mr -l gu -l kn -l ml -l pa -l or -l as
```

This creates: `locale/hi/LC_MESSAGES/django.po`, `locale/ta/LC_MESSAGES/django.po`, etc.

### 4. Translate the Strings

Open each `.po` file and add translations:

```po
# locale/hi/LC_MESSAGES/django.po
msgid "Welcome to Kisan Connect"
msgstr "किसान कनेक्ट में आपका स्वागत है"

msgid "Add to Cart"
msgstr "कार्ट में जोड़ें"

msgid "Buy Now"
msgstr "अभी खरीदें"
```

**PRO TIP**: Use Google Translate API or hire translators for accurate translations.

### 5. Compile Translations

After translating, compile the .po files:

```bash
python manage.py compilemessages
```

This creates `.mo` files that Django uses.

### 6. Add Language Switcher to Navbar

In `base.html`, add this inside the navbar (before user menu):

```django
{% include 'app/language_switcher.html' %}
```

### 7. Test Language Switching

1. Run server: `python manage.py runserver`
2. Visit: `http://127.0.0.1:8000/`
3. Click language dropdown in navbar
4. Select a language - URL will change to `/hi/`, `/ta/`, etc.

## 📁 File Structure

```
ec/
├── locale/                    # Translation files
│   ├── hi/
│   │   └── LC_MESSAGES/
│   │       ├── django.po      # Hindi translations (edit this)
│   │       └── django.mo      # Compiled (auto-generated)
│   ├── ta/
│   │   └── LC_MESSAGES/
│   │       ├── django.po      # Tamil translations
│   │       └── django.mo
│   └── ... (other languages)
├── app/
│   └── templates/
│       └── app/
│           ├── language_switcher.html  # Language dropdown
│           └── translation_examples.html  # Reference examples
└── manage.py
```

## 🎯 Quick Translation Workflow

1. **Mark strings**: Add `{% trans %}` in templates, `_()` in Python
2. **Extract**: `python manage.py makemessages -l hi`
3. **Translate**: Edit `locale/hi/LC_MESSAGES/django.po`
4. **Compile**: `python manage.py compilemessages`
5. **Test**: Switch language and verify

## 🌐 URL Structure

- English: `http://127.0.0.1:8000/en/`
- Hindi: `http://127.0.0.1:8000/hi/`
- Tamil: `http://127.0.0.1:8000/ta/`
- Telugu: `http://127.0.0.1:8000/te/`

Django automatically detects browser language or uses session preference.

## 💡 Best Practices

1. **Always use translation tags** - Never hardcode text
2. **Keep strings simple** - Easier to translate
3. **Use context**: `{% trans "Home" context "navigation" %}` vs `{% trans "Home" context "address" %}`
4. **Test all languages** - Ensure UI doesn't break with longer text
5. **Professional translations** - Use native speakers for quality

## 🔧 Common Commands

```bash
# Create/update translation files for specific language
python manage.py makemessages -l hi

# Create/update for all languages at once
python manage.py makemessages -a

# Compile all translations
python manage.py compilemessages

# Create translation files for JavaScript
python manage.py makemessages -d djangojs -l hi
```

## 📝 Translation Priority

Start with these high-impact areas:
1. ✅ Navigation menu (Home, Products, Cart, Profile)
2. ✅ Buttons (Add to Cart, Buy Now, Submit, Cancel)
3. ✅ Form labels (Name, Email, Phone, Address)
4. ✅ Error messages
5. ✅ Product categories
6. ✅ Government schemes titles
7. ✅ Weather information
8. ✅ Success/error notifications

## 🎨 Language Switcher Styling

The language switcher is already styled with Font Awesome icons and Bootstrap dropdown. It shows current language and allows instant switching.

## ⚡ Performance

- Translations are cached automatically
- .mo files are binary and fast to load
- No performance impact on production

## 🚨 Important Notes

- Run `makemessages` after adding new translatable strings
- Always run `compilemessages` before deploying
- Keep .po files in version control, .mo files are auto-generated
- Test with different languages to ensure UI layout works

---

**Ready to translate!** Start by adding `{% load i18n %}` and `{% trans %}` tags to your templates, then run `makemessages`.
