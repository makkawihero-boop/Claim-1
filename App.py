import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مساعد المطالبات الذكي", page_icon="🚀", layout="centered")

# 2. تعديل اتجاه الصفحة ليدعم اللغة العربية (RTL)
st.markdown("""
    <style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp {
        direction: rtl;
    }
    .stSelectbox label, .stTextInput label {
        text-align: right;
        display: block;
        font-size: 1.1rem;
        font-weight: bold;
        color: #1e3a8a;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
        padding: 10px;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    </style>
""", unsafe_allow_html=True)

# 3. قاعدة البيانات المصغرة (القواعد التشغيلية المترجمة)
system_rules = {
    "حمى وارتفاع حرارة (كشف عام)": {"code": "R50.9", "allowed_services": ["كشف عيادة عامة", "أشعة صوتية (سونار)"]},
    "صداع نصفي": {"code": "R51", "allowed_services": ["كشف عيادة عامة"]},
    "تسوس أسنان / ألم في الضرس": {"code": "K02", "allowed_services": ["كشف عيادة عامة", "خلع ضرس"]},
    "متابعة حمل / ولادة": {"code": "O80", "gender": "أنثى", "allowed_services": ["كشف عيادة عامة", "أشعة صوتية (سونار)"]}
}

service_codes = {
    "كشف عيادة عامة": "99213",
    "أشعة رنين مغناطيسي (MRI)": "70551",
    "خلع ضرس": "71400",
    "أشعة صوتية (سونار)": "76805"
}

# 4. واجهة المستخدم
st.title("🚀 مساعد المطالبات الذكي للمستوصفات")
st.write("أدخل بيانات الزيارة ببساطة، وسيقوم النظام بتجهيز المطالبة فنياً للرفع على منصة نفيس.")
st.divider()

# الخطوة 1
st.subheader("👤 الخطوة 1: بيانات المريض")
col1, col2 = st.columns(2)
with col1:
    patient_id = st.text_input("رقم الهوية / الإقامة", placeholder="مثال: 10xxxxxxx")
with col2:
    patient_gender = st.selectbox("جنس المريض", ["ذكر", "أنثى"])

# الخطوة 2
st.subheader("🏥 الخطوة 2: ماذا قال الطبيب؟ (التشخيص)")
diagnosis_list = ["-- اختر من القائمة --"] + list(system_rules.keys())
diagnosis = st.selectbox("اختر التشخيص الأقرب لحالة المريض:", diagnosis_list)

# الخطوة 3
st.subheader("💉 الخطوة 3: ماذا قدم المستوصف للمريض؟ (الإجراء)")
service_list = ["-- اختر الخدمة --"] + list(service_codes.keys())
service = st.selectbox("اختر الخدمة المقدمة:", service_list)

st.write("") # مسافة فارغة

# 5. محرك القواعد (Rules Engine)
if st.button("🔍 افحص المطالبة الآن", use_container_width=True):
    if diagnosis == "-- اختر من القائمة --" or service == "-- اختر الخدمة --":
        st.warning("⚠️ الرجاء اختيار التشخيص والخدمة المقدمة أولاً!")
    else:
        rule = system_rules[diagnosis]
        errors = []

        # القاعدة 1: فحص التعارض الديموغرافي (الجنس)
        if "gender" in rule and rule["gender"] != patient_gender:
            errors.append(f"المريض مسجل كـ ({patient_gender})، لكن التشخيص المختار يخص ({rule['gender']}). هذا سيؤدي لرفض فوري من التأمين.")

        # القاعدة 2: فحص التغطية والمطابقة الطبية
        if service not in rule["allowed_services"]:
            if service == "أشعة رنين مغناطيسي (MRI)":
                errors.append("شركة التأمين لا تغطي (أشعة الرنين المغناطيسي) لحالة تشخيص بسيطة. يجب أخذ موافقة مسبقة أو إرفاق تقرير طبي معقد.")
            elif service == "خلع ضرس" and "أسنان" not in diagnosis:
                errors.append("لا يمكن طلب (خلع ضرس) بينما تشخيص المريض ليس له علاقة بالأسنان.")
            else:
                errors.append("الخدمة المقدمة غير متطابقة طبياً مع تشخيص الطبيب حسب قوانين مجلس الضمان الصحي.")

        # 6. عرض النتيجة النهائية
        st.divider()
        if len(errors) > 0:
            st.error("⛔ توقف! لا ترسل المطالبة")
            st.write("**المطالبة سُترفض بنسبة 100% للأسباب التالية، يرجى تعديلها:**")
            for err in errors:
                st.markdown(f"- ❌ **{err}**")
        else:
            st.success("✅ ممتاز! المطالبة جاهزة للإرسال بأمان")
            st.write("جميع البيانات متطابقة طبياً وتأمينياً. لا يوجد تعارض.")

        # إظهار الأكواد التقنية في الأسفل
        st.info(f"""
        **بيانات الإرسال لمنصة نفيس (الخلفية التقنية المخفية عن الموظف):**
        - كود المرض (ICD-10): `{rule['code']}`
        - كود الإجراء (CPT): `{service_codes[service]}`
        """)
