import streamlit as st
import requests
from typing import Optional

# ===================== تنظیمات اولیه =====================
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="SmartShop Advisor",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== استایل CSS =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700&display=swap');

* {
    font-family: 'Vazirmatn', sans-serif !important;
    direction: rtl;
}

.stApp {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
}

.main-title {
    text-align: center;
    color: #ffffff;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
}

.subtitle {
    text-align: center;
    color: #e0e7ff;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stTextArea > div > div > textarea {
    background-color: rgba(255, 255, 255, 0.95) !important;
    color: #1f2937 !important;
    border: 2px solid #6366f1 !important;
    border-radius: 12px !important;
    padding: 12px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > select:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    width: 100%;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
}

.stRadio > label {
    color: #ffffff !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    margin-bottom: 8px !important;
}

.stRadio > div {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 12px;
    border-radius: 10px;
}

.product-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
}

.rank-badge {
    display: inline-block;
    font-size: 2.5rem;
    margin-bottom: 10px;
}

.product-title {
    color: #1f2937;
    font-size: 1.3rem;
    font-weight: 700;
    margin: 12px 0;
    line-height: 1.4;
}

.price-tag {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 1.3rem;
    font-weight: 700;
    display: inline-block;
    margin: 12px 0;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.feature-row {
    background-color: #f9fafb;
    padding: 10px 14px;
    margin: 6px 0;
    border-radius: 8px;
    border-right: 4px solid #6366f1;
}

.feature-label {
    color: #6366f1;
    font-weight: 600;
    font-size: 0.95rem;
}

.feature-value {
    color: #374151;
    font-weight: 500;
    font-size: 0.95rem;
}

.provider-badge {
    background-color: #dbeafe;
    color: #1e40af;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    display: inline-block;
    margin: 8px 0;
}

.purchase-link {
    display: inline-block;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white !important;
    text-decoration: none !important;
    padding: 10px 24px;
    border-radius: 10px;
    font-weight: 600;
    margin-top: 12px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.purchase-link:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(245, 158, 11, 0.5);
}

.ai-insight-box {
    background: linear-gradient(145deg, #fef3c7 0%, #fde68a 100%);
    border: 2px solid #f59e0b;
    border-radius: 16px;
    padding: 24px;
    margin: 20px 0;
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.2);
}

.ai-insight-title {
    color: #92400e;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.ai-insight-content {
    color: #78350f;
    font-size: 1.05rem;
    line-height: 1.8;
}

.smart-question-box {
    background-color: rgba(255, 255, 255, 0.15);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
}

.section-title {
    color: #ffffff;
    font-size: 1.3rem;
    font-weight: 600;
    margin: 20px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

.no-result-card {
    background: linear-gradient(145deg, #fef2f2 0%, #fee2e2 100%);
    border: 2px solid #ef4444;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    color: #991b1b;
    font-size: 1.2rem;
    font-weight: 600;
}

.loading-spinner {
    text-align: center;
    color: #ffffff;
    font-size: 1.1rem;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===================== دیکشنری ویژگی‌های دسته‌بندی =====================
CATEGORY_FEATURES = {
    "گوشی موبایل": [
        "برند", "مدل", "حافظه داخلی", "رم", "دوربین اصلی",
        "دوربین سلفی", "باتری", "صفحه‌نمایش", "پردازنده", "سیستم‌عامل"
    ],
    "لپ‌تاپ": [
        "برند", "مدل", "پردازنده", "رم", "حافظه",
        "کارت گرافیک", "صفحه‌نمایش", "وزن", "سیستم‌عامل", "باتری"
    ],
    "یخچال": [
        "برند", "مدل", "حجم کل", "تعداد درب", "رنگ",
        "نوع یخچال", "مصرف انرژی", "ابعاد", "گارانتی", "ویژگی‌های خاص"
    ],
    "تلویزیون": [
        "برند", "مدل", "سایز", "کیفیت تصویر", "نوع پنل",
        "سیستم‌عامل", "پورت‌ها", "صدا", "HDR", "وای‌فای"
    ],
    "مولتی‌متر": [
        "برند", "مدل", "دقت", "محدوده ولتاژ DC", "محدوده ولتاژ AC",
        "محدوده جریان", "مقاومت", "ظرفیت خازن", "فرکانس", "نمایشگر"
    ],
    "خودرو": [
        "برند", "مدل", "سال ساخت", "رنگ", "کارکرد",
        "نوع سوخت", "گیربکس", "حجم موتور", "وضعیت بدنه", "قیمت"
    ],
    "صندلی اداری": [
        "برند", "مدل", "جنس", "رنگ", "ارتفاع قابل تنظیم",
        "دسته قابل تنظیم", "پشتی", "چرخ", "گارانتی", "حداکثر وزن"
    ],
    "سایر": [
        "برند", "مدل", "ویژگی ۱", "ویژگی ۲", "ویژگی ۳",
        "ویژگی ۴", "ویژگی ۵", "ویژگی ۶", "ویژگی ۷", "ویژگی ۸"
    ]
}

# ===================== سوالات هوشمند =====================
SMART_QUESTIONS = {
    "گوشی موبایل": [
        ("استفاده اصلی شما از گوشی چیست?", "st.selectbox", 
         ["انتخاب کنید", "عکاسی و فیلمبرداری", "بازی", "کار اداری و اپلیکیشن", "مکالمه و پیام"]),
        ("حافظه مورد نیاز شما چقدر است?", "st.radio", 
         ["۶۴ گیگابایت", "۱۲۸ گیگابایت", "۲۵۶ گیگابایت", "۵۱۲ گیگابایت یا بیشتر"]),
        ("کیفیت دوربین برای شما مهم است?", "st.radio", 
         ["بله، بسیار مهم", "متوسط", "خیر، اهمیتی ندارد"]),
    ],
    "لپ‌تاپ": [
        ("استفاده اصلی از لپ‌تاپ چیست?", "st.selectbox",
         ["انتخاب کنید", "برنامه‌نویسی", "گرافیک و ویرایش ویدیو", "گیمینگ", "کار اداری", "آموزش آنلاین"]),
        ("قابلیت حمل برای شما مهم است?", "st.radio",
         ["بله، باید سبک باشد", "خیر، عملکرد مهم‌تر است"]),
        ("نیاز به کارت گرافیک قوی دارید?", "st.radio",
         ["بله، حتماً", "خیر"]),
    ],
    "یخچال": [
        ("چند نفره استفاده می‌کنید?", "st.selectbox",
         ["انتخاب کنید", "۱ تا ۲ نفر", "۳ تا ۴ نفر", "۵ نفر یا بیشتر"]),
        ("نوع یخچال مورد نظر شما چیست?", "st.radio",
         ["دو درب", "ساید بای ساید", "چهار درب", "تک درب"]),
        ("مصرف انرژی برای شما مهم است?", "st.radio",
         ["بله، بسیار مهم", "متوسط", "خیر"]),
    ],
    "تلویزیون": [
        ("سایز مورد نظر شما چیست?", "st.selectbox",
         ["انتخاب کنید", "کمتر از ۴۳ اینچ", "۴۳ تا ۵۰ اینچ", "۵۵ تا ۶۵ اینچ", "بیشتر از ۶۵ اینچ"]),
        ("استفاده اصلی شما چیست?", "st.radio",
         ["تماشای فیلم و سریال", "بازی", "برنامه‌های تلویزیونی", "همه موارد"]),
        ("کیفیت تصویر ۴K ضروری است?", "st.radio",
         ["بله", "خیر"]),
    ],
    "مولتی‌متر": [
        ("کاربرد اصلی شما چیست?", "st.selectbox",
         ["انتخاب کنید", "استفاده خانگی", "تعمیرات صنعتی", "آزمایشگاه", "الکترونیک دیجیتال"]),
        ("نیاز به دقت بالا دارید?", "st.radio",
         ["بله، حرفه‌ای", "خیر، عادی کافی است"]),
        ("نوع نمایشگر ترجیحی شما?", "st.radio",
         ["دیجیتال", "آنالوگ", "فرقی ندارد"]),
    ],
    "صندلی اداری": [
        ("چند ساعت در روز از صندلی استفاده می‌کنید?", "st.selectbox",
         ["انتخاب کنید", "کمتر از ۴ ساعت", "۴ تا ۸ ساعت", "بیشتر از ۸ ساعت"]),
        ("آیا مشکل کمردرد دارید?", "st.radio",
         ["بله", "خیر"]),
        ("پشتی سر ضروری است?", "st.radio",
         ["بله", "خیر", "فرقی ندارد"]),
    ],
}

# ===================== نقشه کلمات کلیدی =====================
KEYWORD_MAP = {
    "گوشی": "گوشی موبایل", "موبایل": "گوشی موبایل", "phone": "گوشی موبایل",
    "samsung": "گوشی موبایل", "iphone": "گوشی موبایل", "شیائومی": "گوشی موبایل",
    "اندروید": "گوشی موبایل", "آیفون": "گوشی موبایل",
    
    "لپتاپ": "لپ‌تاپ", "laptop": "لپ‌تاپ", "نوت‌بوک": "لپ‌تاپ",
    "notebook": "لپ‌تاپ", "مک": "لپ‌تاپ", "ایسوس": "لپ‌تاپ",
    
    "یخچال": "یخچال", "فریزر": "یخچال", "refrigerator": "یخچال",
    
    "تلویزیون": "تلویزیون", "tv": "تلویزیون", "تی‌وی": "تلویزیون",
    "تلوزیون": "تلویزیون",
    
    "مولتی‌متر": "مولتی‌متر", "مولتیمتر": "مولتی‌متر", "multimeter": "مولتی‌متر",
    "ولت‌متر": "مولتی‌متر", "آوومتر": "مولتی‌متر",
    
    "ماشین": "خودرو", "car": "خودرو", "اتومبیل": "خودرو",
    "خودرو": "خودرو",
    
    "صندلی": "صندلی اداری", "chair": "صندلی اداری",
}

KNOWN_CATEGORIES = list(CATEGORY_FEATURES.keys())

# ===================== تشخیص دسته‌بندی =====================
def detect_category(text: str) -> str:
    text_lower = text.lower().strip()
    
    for keyword, category in KEYWORD_MAP.items():
        if keyword in text_lower:
            return category
    
    for cat in KNOWN_CATEGORIES:
        if cat in text_lower:
            return cat
    
    return "سایر"

# ===================== رندر جدول مقایسه =====================
def render_comparison_table(results: list, category: str) -> None:
    if not results:
        return
    
    feature_list = CATEGORY_FEATURES.get(category, CATEGORY_FEATURES["سایر"])
    rank_labels = ["🥇", "🥈", "🥉"]
    
    cols = st.columns(len(results))
    
    for idx, product in enumerate(results):
        with cols[idx]:
            rank_badge = rank_labels[idx] if idx < 3 else f"#{idx+1}"
            
            st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="rank-badge">{rank_badge}</div>', unsafe_allow_html=True)
            
            img_url = product.get("image") or product.get("image_url")
            if img_url:
                try:
                    st.image(img_url, use_container_width=True)
                except:
                    st.info("🖼️ تصویر موجود نیست")
            
            title = product.get("title", "بدون عنوان")
            st.markdown(f'<div class="product-title">{title}</div>', unsafe_allow_html=True)
            
            price = product.get("price")
            if price:
                price_str = f"{int(price):,}" if isinstance(price, (int, float)) else str(price)
                st.markdown(f'<div class="price-tag">{price_str} تومان</div>', unsafe_allow_html=True)
            
            provider = product.get("provider", "نامشخص")
            st.markdown(f'<div class="provider-badge">🏪 {provider}</div>', unsafe_allow_html=True)
            
            specs = product.get("specs") or product.get("attributes") or {}
            for feature in feature_list:
                value = specs.get(feature, "—")
                st.markdown(
                    f'<div class="feature-row">'
                    f'<span class="feature-label">{feature}:</span> '
                    f'<span class="feature-value">{value}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            link = product.get("url") or product.get("link")
            if link:
                st.markdown(
                    f'<a href="{link}" target="_blank" class="purchase-link">🛒 مشاهده و خرید</a>',
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

# ===================== رندر بینش هوش مصنوعی =====================
def render_ai_insights(results: list, category: str, budget: Optional[int], 
                       use_case: str, smart_answers: dict) -> None:
    if not results:
        return
    
    best_product = results[0]
    best_title = best_product.get("title", "محصول")
    best_price = best_product.get("price")
    
    result_count = len(results)
    prices = [r.get("price") for r in results if r.get("price")]
    avg_price = sum(prices) / len(prices) if prices else 0
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    
    budget_note = ""
    if budget and avg_price:
        if avg_price < budget * 0.7:
            budget_note = "💰 محصولات پیشنهادی به‌طور قابل‌توجهی زیر بودجه شما هستند."
        elif avg_price < budget:
            budget_note = "✅ محصولات پیشنهادی در محدوده بودجه شما قرار دارند."
        elif avg_price <= budget * 1.1:
            budget_note = "⚖️ قیمت محصولات تقریباً برابر با بودجه شماست."
        else:
            budget_note = "⚠️ قیمت محصولات بالاتر از بودجه شماست."
    
    st.markdown('<div class="ai-insight-box">', unsafe_allow_html=True)
    st.markdown('<div class="ai-insight-title">🤖 تحلیل هوشمند</div>', unsafe_allow_html=True)
    
    insights_text = f"""
    <div class="ai-insight-content">
    <strong>✨ بهترین انتخاب:</strong> {best_title}<br>
    """
    
    if best_price:
        best_price_str = f"{int(best_price):,}" if isinstance(best_price, (int, float)) else str(best_price)
        insights_text += f"<strong>💵 قیمت:</strong> {best_price_str} تومان<br>"
    
    if budget_note:
        insights_text += f"<br>{budget_note}<br>"
    
    if prices:
        insights_text += f"<br><strong>📊 بازه قیمت محصولات:</strong> {int(min_price):,} تا {int(max_price):,} تومان<br>"
    
    if use_case:
        insights_text += f"<br><strong>🎯 کاربرد شما:</strong> {use_case}<br>"
    
    if smart_answers:
        insights_text += "<br><strong>📝 ترجیحات شما:</strong><ul>"
        for q, a in smart_answers.items():
            if a and a != "انتخاب کنید":
                insights_text += f"<li>{q}: <strong>{a}</strong></li>"
        insights_text += "</ul>"
    
    insights_text += f"""
    <br><strong>🏆 توصیه نهایی:</strong> بر اساس جستجوی شما، محصول اول بهترین تطابق را با نیاز شما دارد.
    </div>
    """
    
    st.markdown(insights_text, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== تابع اصلی =====================
def main():
    st.markdown('<h1 class="main-title">🛒 SmartShop Advisor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">مشاور هوشمند خرید شما</p>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.markdown('<div class="section-title">🔍 جستجوی هوشمند</div>', unsafe_allow_html=True)
        
        product_name = st.text_input(
            "نام محصول مورد نظر خود را وارد کنید:",
            placeholder="مثلاً: گوشی سامسونگ، لپ‌تاپ ایسوس، یخچال"
        )
        
        active_category = detect_category(product_name) if product_name else "سایر"
        
        if product_name:
            st.info(f"📂 دسته‌بندی شناسایی‌شده: **{active_category}**")
        
        st.markdown('<div class="section-title">💡 اطلاعات تکمیلی</div>', unsafe_allow_html=True)
        
        use_case = st.text_area(
            "کاربرد اصلی شما از این محصول چیست؟",
            placeholder="مثلاً: برای کار اداری، بازی، عکاسی حرفه‌ای، ...",
            height=100
        )
        
        smart_answers = {}
        if active_category in SMART_QUESTIONS and product_name:
            st.markdown('<div class="section-title">❓ سوالات تخصصی</div>', unsafe_allow_html=True)
            
            for question_label, widget_type, options in SMART_QUESTIONS[active_category]:
                st.markdown(f'<div class="smart-question-box">', unsafe_allow_html=True)
                
                if widget_type == "st.selectbox":
                    answer = st.selectbox(question_label, options, key=f"q_{question_label}")
                elif widget_type == "st.radio":
                    answer = st.radio(question_label, options, key=f"q_{question_label}")
                else:
                    answer = None
                
                if answer and answer != "انتخاب کنید":
                    smart_answers[question_label] = answer
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-title">⚙️ تنظیمات پیشرفته</div>', unsafe_allow_html=True)
        
        if active_category in CATEGORY_FEATURES:
            feature_list = CATEGORY_FEATURES[active_category]
            priorities = st.multiselect(
                "اولویت‌های شما در انتخاب محصول:",
                feature_list,
                help="ویژگی‌هایی که برای شما اهمیت دارند را انتخاب کنید"
            )
        else:
            priorities = []
        
        budget = st.number_input(
            "حداکثر بودجه (تومان):",
            min_value=0,
            step=100000,
            format="%d",
            help="حداکثر قیمتی که می‌خواهید پرداخت کنید"
        )
        
        if budget > 0:
            st.success(f"💰 بودجه: {budget:,} تومان")
        
        search_clicked = st.button("🔎 جستجو و تحلیل هوشمند", use_container_width=True)
    
    with col_right:
        if product_name and len(product_name.strip()) >= 3:
            trigger_search = search_clicked
        else:
            trigger_search = False
        
        if trigger_search:
            query = product_name.strip() or active_category.strip()
            
            if not query or active_category == "سایر":
                st.warning("⚠️ لطفاً نام محصول را دقیق‌تر وارد کنید.")
            else:
                try:
                    st.markdown('<div class="loading-spinner">⏳ در حال جستجو و تحلیل...</div>', 
                              unsafe_allow_html=True)
                    
                    payload = {
                        "query": query,
                        "max_price": budget if budget else None,
                        "use_case": use_case if use_case else None,
                        "priorities": priorities if priorities else [],
                        "smart_answers": smart_answers if smart_answers else {},
                    }
                    
                    resp = requests.post(
                        f"{API_BASE}/api/v1/advise/",
                        json=payload,
                        timeout=30,
                    )
                    
                    resp.raise_for_status()
                    data = resp.json()
                    
                    if isinstance(data, list):
                        results = data
                    elif isinstance(data, dict):
                        results = data.get("items") or data.get("results") or data.get("data") or []
                    else:
                        results = []
                    
                    if results:
                        st.success(f"🎉 {len(results)} محصول یافت شد")
                        
                        st.markdown('<div class="section-title">📊 مقایسه محصولات</div>', unsafe_allow_html=True)
                        render_comparison_table(results, active_category)
                        
                        render_ai_insights(results, active_category, budget, use_case, smart_answers)
                    
                    else:
                        st.markdown(
                            '<div class="no-result-card">❌ متأسفانه محصولی یافت نشد. لطفاً جستجوی خود را تغییر دهید.</div>',
                            unsafe_allow_html=True
                        )
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ خطا در اتصال به سرور. لطفاً مطمئن شوید که Backend در حال اجرا است.")
                except requests.exceptions.Timeout:
                    st.error("⏱️ زمان درخواست به پایان رسید. لطفاً دوباره تلاش کنید.")
                except requests.exceptions.HTTPError as e:
                    st.error(f"❌ خطای HTTP: {e}")
                except Exception as e:
                    st.error(f"❌ خطای غیرمنتظره: {str(e)}")

if __name__ == "__main__":
    main()
