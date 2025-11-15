from django import template
from khayyam import JalaliDate

register = template.Library()

# نگاشت اعداد انگلیسی به فارسی
EN_TO_FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

@register.filter
def to_jalali(value):
    """
    تبدیل تاریخ میلادی به جلالی با اعداد فارسی
    """
    if not value:
        return ""
    try:
        jalali_date = JalaliDate(value).strftime("%Y-%m-%d")
        return jalali_date.translate(EN_TO_FA_DIGITS)
    except Exception:
        return value
