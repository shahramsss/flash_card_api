from django import template

register = template.Library()

EN_TO_FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gy > 1600:
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621

    gy2 = gy + 1 if gm > 2 else gy
    days = (
        365 * gy
        + (gy2 + 3) // 4
        - (gy2 + 99) // 100
        + (gy2 + 399) // 400
        - 80
        + gd
        + g_d_m[gm - 1]
    )

    jy += 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461

    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365

    jm = 1 + (days // 31) if days < 186 else 7 + ((days - 186) // 30)
    jd = 1 + (days % 31) if days < 186 else 1 + ((days - 186) % 30)

    return jy, jm, jd


@register.filter
def to_jalali(value):
    if not value:
        return ""

    try:
        jy, jm, jd = gregorian_to_jalali(value.year, value.month, value.day)
        jalali = f"{jy:04d}-{jm:02d}-{jd:02d}"
        return jalali.translate(EN_TO_FA_DIGITS)
    except Exception:
        return value

