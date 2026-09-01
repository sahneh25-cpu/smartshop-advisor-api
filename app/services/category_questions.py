"""Category-aware question and brand catalogs.

Core stays generic: new product families can be added here without touching
store adapters. Unknown products fall back to a generic spec-gathering set.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


Question = Dict[str, Any]


def _opt(*labels: str) -> List[str]:
    return list(labels)


def _q(
    key: str,
    text: str,
    options: Optional[Sequence[str]] = None,
    qtype: str = "choice",
    help_text: Optional[str] = None,
) -> Question:
    opts = list(options or [])
    return {
        "id": key,
        "key": key,
        "text": text,
        "label": text,
        "type": qtype if opts or qtype != "choice" else "text",
        "options": [{"id": o, "text": o, "value": o, "label": o} for o in opts],
        "help_text": help_text,
    }


# Keywords -> canonical category id
_KEYWORD_CATEGORY: List[Tuple[Tuple[str, ...], str]] = [
    (("موتورسیکلت", "motorcycle", "scooter", "موتور سیکلت", "بایک"), "motorcycle"),
    (("ماشین", "خودرو", "اتومبیل", "car", "vehicle", "sedan", "suv"), "car"),
    (("لپ تاپ", "لپ‌تاپ", "laptop", "notebook", "مک‌بوک", "macbook"), "laptop"),
    (("موبایل", "گوشی", "phone", "smartphone", "آیفون", "iphone"), "phone"),
    (("یخچال", "فریزر", "refrigerator", "fridge", "freezer"), "fridge"),
    (("خازن", "capacitor"), "capacitor"),
    (("دیود", "diode"), "diode"),
    (("مقاومت", "resistor"), "resistor"),
    (("ترانزیستور", "transistor"), "transistor"),
    (("تلویزیون", "تلوزیون", "tv", "television"), "tv"),
]

CATEGORY_LABELS_FA = {
    "car": "خودرو",
    "motorcycle": "موتورسیکلت",
    "laptop": "لپ تاپ",
    "phone": "گوشی موبایل",
    "fridge": "یخچال",
    "capacitor": "خازن",
    "diode": "دیود",
    "resistor": "مقاومت",
    "transistor": "ترانزیستور",
    "tv": "تلویزیون",
    "generic": "کالا",
}

BRANDS: Dict[str, List[str]] = {
    "car": [
        "Toyota", "Hyundai", "Kia", "BMW", "Mercedes-Benz", "Audi",
        "Volkswagen", "Peugeot", "Renault", "Iran Khodro", "Saipa",
        "Ford", "Honda", "Nissan", "Tesla",
    ],
    "motorcycle": [
        "Honda", "Yamaha", "Suzuki", "Kawasaki", "KTM", "BMW Motorrad",
        "Ducati", "Bajaj", "Hero", "TVS",
    ],
    "laptop": [
        "ASUS", "Lenovo", "HP", "Dell", "Apple", "Acer", "MSI",
        "Samsung", "Huawei", "Microsoft",
    ],
    "phone": [
        "Samsung", "Apple", "Xiaomi", "Google", "Nothing", "OnePlus",
        "Huawei", "Honor", "Sony", "Nokia", "Motorola",
    ],
    "fridge": [
        "LG", "Samsung", "Bosch", "Siemens", "Whirlpool", "Electrolux",
        "Haier", "Beko", "Emersun", "Snowa",
    ],
    "tv": ["Samsung", "LG", "Sony", "TCL", "Hisense", "Panasonic", "Xiaomi"],
    "capacitor": ["Murata", "TDK", "Kemet", "Nichicon", "Rubycon", "Vishay", "Samsung Electro-Mechanics"],
    "diode": ["ON Semiconductor", "Vishay", "Nexperia", "STMicroelectronics", "Infineon", "Diodes Inc"],
    "resistor": ["Yageo", "Vishay", "Panasonic", "KOA", "Bourns", "TE Connectivity"],
    "transistor": ["Infineon", "ON Semiconductor", "STMicroelectronics", "NXP", "Toshiba", "Fairchild"],
    "generic": [],
}


def detect_category(text: str) -> str:
    lowered = (text or "").lower()
    for keys, cat in _KEYWORD_CATEGORY:
        if any(k.lower() in lowered for k in keys):
            return cat
    return "generic"


def product_type_label(text: str) -> str:
    cat = detect_category(text)
    if cat == "generic":
        cleaned = (text or "").strip()
        return cleaned or "کالا"
    return CATEGORY_LABELS_FA.get(cat, text)


def _car_questions(answers: Dict[str, Any]) -> List[Question]:
    qs = [
        _q("usage", "برای چه جور استفاده‌ای می‌خوای؟", _opt(
            "شهری روزمره", "سفر جاده‌ای", "خانوادگی", "آفرود", "تجاری/بار", "اسپرت",
        )),
        _q("weight_class", "سبک باشه یا سنگین؟", _opt("سبک", "متوسط", "سنگین")),
        _q("engine_size", "حجم موتور؟", _opt(
            "زیر ۱۲۰۰ سی‌سی", "۱۲۰۰ تا ۱۶۰۰", "۱۶۰۰ تا ۲۰۰۰", "۲۰۰۰ تا ۳۰۰۰", "بالای ۳۰۰۰",
        )),
        _q("horsepower", "اسب بخار حدودی؟", _opt(
            "زیر ۱۰۰", "۱۰۰ تا ۱۵۰", "۱۵۰ تا ۲۰۰", "۲۰۰ تا ۳۰۰", "بالای ۳۰۰",
        )),
        _q("torque", "گشتاور برایت مهم است؟", _opt(
            "عادی کافی است", "گشتاور بالا برای سربالایی/بار", "حداکثر ممکن",
        )),
        _q("fuel", "نوع سوخت؟", _opt("بنزین", "دیزل", "هیبرید", "برقی", "فرقی ندارد")),
        _q("transmission", "گیربکس؟", _opt("اتوماتیک", "دستی", "فرقی ندارد")),
    ]
    return qs


def _moto_questions(answers: Dict[str, Any]) -> List[Question]:
    return [
        _q("usage", "برای چه جور استفاده‌ای می‌خوای؟", _opt(
            "شهری", "جاده", "آفرود", "اسپرت", "تحویل کالا",
        )),
        _q("weight_class", "سبک باشه یا سنگین؟", _opt("سبک", "متوسط", "سنگین")),
        _q("engine_size", "حجم موتور؟", _opt(
            "تا ۱۲۵ سی‌سی", "۱۲۵ تا ۲۵۰", "۲۵۰ تا ۶۰۰", "بالای ۶۰۰",
        )),
        _q("horsepower", "اسب بخار؟", _opt("پایین", "متوسط", "بالا")),
        _q("torque", "گشتاور؟", _opt("عادی", "زیاد")),
    ]


def _computer_questions(kind: str) -> List[Question]:
    usage = _opt(
        "روزمره و وب", "کار اداری", "برنامه‌نویسی", "گرافیک و ویدیو",
        "بازی", "عکاسی", "آموزش",
    ) if kind == "laptop" else _opt(
        "مکالمه و پیام", "عکاسی و فیلم", "بازی", "کار اداری", "سفر",
    )
    extra = []
    if kind == "laptop":
        extra = [
            _q("gpu", "کارت گرافیک جدا می‌خوای؟", _opt("بله", "خیر", "فرقی ندارد")),
            _q("weight", "وزن؟", _opt("خیلی سبک", "متوسط", "فرقی ندارد")),
        ]
    else:
        extra = [
            _q("storage", "حافظه داخلی؟", _opt("۱۲۸ گیگ", "۲۵۶ گیگ", "۵۱۲ گیگ", "۱ ترابایت یا بیشتر")),
            _q("camera", "کیفیت دوربین؟", _opt("خیلی مهم", "متوسط", "کم‌اهمیت")),
        ]
    return [
        _q("usage", "برای چه جور استفاده‌ای می‌خوای؟", usage),
        _q("ram", "رم چقدر باشه؟", _opt("۴ گیگ", "۸ گیگ", "۱۶ گیگ", "۳۲ گیگ یا بیشتر")),
        _q("cpu_brand", "سی‌پی‌یو چه برندی؟", _opt("Intel", "AMD", "Apple", "Qualcomm", "MediaTek", "فرقی ندارد")),
        _q("cpu_cores", "سی‌پی‌یو چند هسته‌ای؟", _opt("۴ هسته", "۶ هسته", "۸ هسته", "۸ هسته به بالا")),
        _q("screen_size", "اندازه صفحه؟", _opt(
            "کوچک (تا ۱۳ اینچ / تا ۶ اینچ)",
            "متوسط",
            "بزرگ",
        )),
        _q("os", "سیستم عامل؟", _opt("Windows", "macOS", "Linux", "Android", "iOS", "فرقی ندارد")),
        *extra,
    ]


def _fridge_questions(answers: Dict[str, Any]) -> List[Question]:
    qs = [
        _q("place", "برای خانه می‌خوای یا مغازه؟", _opt("خانه", "مغازه")),
    ]
    place = str(answers.get("place") or "")
    if place == "خانه":
        qs.extend([
            _q("household", "چند نفره؟", _opt("۱–۲ نفر", "۳–۴ نفر", "۵ نفر یا بیشتر")),
            _q("doors", "نوع یخچال خانگی؟", _opt("تک‌درب", "دو درب", "ساید بای ساید", "چهار درب")),
            _q("energy", "مصرف انرژی چقدر مهم است؟", _opt("خیلی مهم", "متوسط", "کم‌اهمیت")),
            _q("freezer", "فریزر جدا می‌خوای؟", _opt("بله، بالا", "بله، پایین", "ساید", "نه")),
        ])
    elif place == "مغازه":
        qs.extend([
            _q("shop_type", "نوع یخچال فروشگاهی؟", _opt(
                "ویترینی نوشیدنی", "ایستاده فروشگاهی", "خوابیده/جزیره‌ای", "صنعتی بزرگ",
            )),
            _q("capacity", "ظرفیت حدودی؟", _opt("زیر ۴۰۰ لیتر", "۴۰۰ تا ۸۰۰", "بالای ۸۰۰")),
            _q("temp", "دمای کاری؟", _opt("بالای صفر", "زیر صفر", "هر دو")),
            _q("power", "برق سه‌فاز لازم است؟", _opt("تک‌فاز کافی است", "سه‌فاز", "نمی‌دانم")),
        ])
    return qs


def _part_questions(part: str) -> List[Question]:
    common = [
        _q("package", "دیپ باشه یا اس‌ام‌دی؟", _opt("DIP", "SMD", "هر دو")),
        _q("power", "توانش؟", _opt("۱/۸ وات", "۱/۴ وات", "۱/۲ وات", "۱ وات", "بالاتر", "نمی‌دانم")),
    ]
    if part == "capacitor":
        common.append(_q("capacitance", "ظرفیتش؟", qtype="text", help_text="مثلاً ۱۰µF یا ۱۰۰nF"))
        common.append(_q("voltage", "ولتاژ کار؟", _opt("۱۶ ولت", "۲۵ ولت", "۵۰ ولت", "۱۰۰ ولت", "بالاتر")))
        common.append(_q("cap_type", "نوع خازن؟", _opt("الکترولیت", "سرامیک", "تانتال", "فیلم", "نمی‌دانم")))
    elif part == "diode":
        common.append(_q("diode_type", "نوع دیود؟", _opt("یکسوساز", "زینر", "شاتکی", "LED", "نمی‌دانم")))
        common.append(_q("current", "جریان؟", qtype="text"))
    elif part == "resistor":
        common.append(_q("resistance", "مقدار مقاومت؟", qtype="text", help_text="مثلاً ۱۰kΩ"))
        common.append(_q("tolerance", "تلرانس؟", _opt("۱٪", "۵٪", "۱۰٪", "فرقی ندارد")))
    elif part == "transistor":
        common.append(_q("tr_type", "نوع؟", _opt("BJT NPN", "BJT PNP", "N-MOSFET", "P-MOSFET", "نمی‌دانم")))
        common.append(_q("current", "جریان کلکتور/درین؟", qtype="text"))
    return common


def _tv_questions() -> List[Question]:
    return [
        _q("screen_size", "چه سایزی برای تلویزیون مدنظر دارید؟", _opt(
            "32 اینچ", "43 اینچ", "50 اینچ", "55 اینچ", "65 اینچ", "75 اینچ",
        ), help_text="برای اتاق کوچک 32 تا 43، پذیرایی متوسط 50 تا 55 و سالن بزرگ 65 اینچ به بالا مناسب‌تر است."),
        _q("resolution", "کیفیت تصویر موردنظرتان چیست؟", _opt("Full HD", "4K", "8K"),
           help_text="برای خرید معمولی، 4K انتخاب رایج و مناسب‌تری است."),
        _q("budget", "بودجه تقریبی شما چقدر است؟", qtype="text",
           help_text="بودجه کمک می‌کند گزینه‌های نامرتبط حذف شوند."),
    ]


def _generic_questions() -> List[Question]:
    return [
        _q("usage", "برای چه جور استفاده‌ای می‌خوای؟", qtype="text"),
        _q("must_have", "چه ویژگی‌هایی حتماً باید داشته باشد؟", qtype="text"),
        _q("size_or_capacity", "اندازه، ظرفیت یا مدل خاصی مد نظر است؟", qtype="text"),
        _q("condition", "نو می‌خوای یا کارکرده هم قبول است؟", _opt("فقط نو", "کارکرده هم باشد", "فرقی ندارد")),
    ]


def all_questions_for(user_query: str, answers: Optional[Dict[str, Any]] = None) -> List[Question]:
    answers = answers or {}
    cat = detect_category(user_query)
    if cat == "car":
        return _car_questions(answers)
    if cat == "motorcycle":
        return _moto_questions(answers)
    if cat == "laptop":
        return _computer_questions("laptop")
    if cat == "phone":
        return _computer_questions("phone")
    if cat == "fridge":
        return _fridge_questions(answers)
    if cat in {"capacitor", "diode", "resistor", "transistor"}:
        return _part_questions(cat)
    if cat == "tv":
        return _tv_questions()
    return _generic_questions()


def unanswered_questions(
    user_query: str,
    answers: Optional[Dict[str, Any]] = None,
    skip_keys: Optional[Iterable[str]] = None,
) -> List[Question]:
    answers = answers or {}
    skip = set(skip_keys or [])
    result = []
    for q in all_questions_for(user_query, answers):
        key = q["key"]
        if key in skip:
            continue
        if key in answers and answers[key] not in (None, "", "انتخاب کنید"):
            continue
        result.append(q)
    return result


def brands_for(user_query: str) -> List[str]:
    cat = detect_category(user_query)
    brands = list(BRANDS.get(cat) or [])
    if not brands:
        brands = [
            "Samsung", "LG", "Sony", "Apple", "Bosch", "Philips",
            "Generic / OEM", "Local brand",
        ]
    return brands
