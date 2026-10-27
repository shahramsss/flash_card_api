# templatetags/markdown_extras.py
from django import template
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    if not text:
        return ""
    # فعال‌سازی پشتیبانی از کدهای چندخطی، جداول و خط‌های جدید
    return markdown.markdown(
        text,
        extensions=[
            'fenced_code',  # پشتیبانی از
            'tables',       # پشتیبانی از جدول
            'nl2br'         # تبدیل اینتر به خط جدید
        ]
    )
