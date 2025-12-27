from django import template
from khayyam import JalaliDate

register = template.Library()

@register.filter
def to_jalali(value):
    """
    تبدیل تاریخ میلادی به جلالی
    """
    if not value:
        return ""
    return JalaliDate(value).strftime("%Y/%m/%d")

@register.filter
def jalali_weekday(value):
    """
    نمایش نام روز هفته به جلالی
    """
    if not value:
        return ""
    return JalaliDate(value).strftime("%A")
