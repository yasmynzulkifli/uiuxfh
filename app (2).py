import streamlit as st
from supabase import create_client
from datetime import datetime
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FindHouse Survey / Tinjauan FindHouse",
    page_icon="🏠",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Colour palette matching FindHouse brand */
    :root {
        --fh-primary: #E85D26;
        --fh-dark:    #1A1A2E;
        --fh-light:   #F8F4F0;
    }
    .fh-header {
        background: linear-gradient(135deg, #E85D26 0%, #C94B1A 100%);
        color: white;
        padding: 2rem 1.5rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .fh-header h1 { font-size: 1.8rem; margin: 0.3rem 0; }
    .fh-header p  { font-size: 0.95rem; opacity: 0.9; margin: 0; }
    .section-badge {
        background: #E85D26;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1A1A2E;
        margin-bottom: 1rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #F0E8E0;
    }
    .lang-note {
        font-size: 0.82rem;
        color: #888;
        font-style: italic;
    }
    .stRadio > label, .stSelectbox > label { font-weight: 500; }
    .success-box {
        background: #E8F5E9;
        border: 1px solid #4CAF50;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
    div[data-testid="stSlider"] { padding: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Supabase client ────────────────────────────────────────────────────────────
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# ── Language toggle ────────────────────────────────────────────────────────────
lang = st.radio("🌐 Language / Bahasa", ["English", "Bahasa Melayu"],
                horizontal=True, label_visibility="collapsed")
EN = lang == "English"

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="fh-header">
    <h1>🏠 FindHouse</h1>
    <h1>{'Website Experience Survey' if EN else 'Tinjauan Pengalaman Laman Web'}</h1>
    <p>{'Help us improve FindHouse! Your feedback takes about 5 minutes.' if EN
       else 'Bantu kami menambah baik FindHouse! Maklum balas anda mengambil masa kira-kira 5 minit.'}</p>
</div>
""", unsafe_allow_html=True)

# ── Helper: section header ─────────────────────────────────────────────────────
def section(badge, title_en, title_ms):
    st.markdown(f'<div class="section-badge">{badge}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{"🔹 " + title_en if EN else "🔹 " + title_ms}</div>',
                unsafe_allow_html=True)

def q(label_en, label_ms):
    return label_en if EN else label_ms

def scale_label():
    return ("1 = Strongly Disagree / Very Poor → 5 = Strongly Agree / Excellent"
            if EN else
            "1 = Sangat Tidak Setuju / Sangat Lemah → 5 = Sangat Setuju / Cemerlang")

# ── Form ───────────────────────────────────────────────────────────────────────
with st.form("survey_form", clear_on_submit=True):

    # ── SECTION 1: About You ──────────────────────────────────────────────────
    section("Section 1 / Bahagian 1",
            "About You", "Tentang Anda")

    role = st.selectbox(
        q("What best describes you?",
          "Apakah yang paling menggambarkan anda?"),
        [""] + (["First-time visitor", "Returning visitor",
                 "Property buyer / investor", "Property agent", "Just browsing"]
                if EN else
                ["Pelawat pertama kali", "Pelawat yang kembali",
                 "Pembeli / pelabur hartanah", "Ejen hartanah", "Sekadar melayari"]),
    )

    device = st.selectbox(
        q("What device did you use?", "Peranti apa yang anda gunakan?"),
        [""] + (["Desktop / Laptop", "Smartphone", "Tablet"]
                if EN else
                ["Desktop / Komputer riba", "Telefon pintar", "Tablet"]),
    )

    pages_visited = st.multiselect(
        q("Which part(s) of FindHouse did you visit today? (select all that apply)",
          "Bahagian mana FindHouse yang anda lawati hari ini? (pilih semua yang berkenaan)"),
        (["Property listings page (Buy/Rent/Auction)",
          "Individual property detail page",
          "News page",
          "Other"]
         if EN else
         ["Halaman senarai hartanah (Beli/Sewa/Lelongan)",
          "Halaman butiran hartanah",
          "Halaman berita",
          "Lain-lain"]),
    )

    st.divider()

    # ── SECTION 2: Listings Page ──────────────────────────────────────────────
    section("Section 2 / Bahagian 2",
            "Property Listings Page  (findhouse.com.my/properties/for-sale)",
            "Halaman Senarai Hartanah  (findhouse.com.my/properties/for-sale)")

    st.caption(scale_label())

    listings_clean = st.slider(
        q("The listings page was visually clean and easy to understand.",
          "Halaman senarai hartanah kelihatan kemas dan mudah difahami."),
        1, 5, 3)

    listings_filter_ease = st.slider(
        q("How easy was it to find properties using the filters (price, type, bedrooms, etc.)?",
          "Sejauh mana mudahnya mencari hartanah menggunakan penapis (harga, jenis, bilik, dll.)?"),
        1, 5, 3)

    listings_filter_sufficient = st.slider(
        q("The filter options were sufficient for my search needs.",
          "Pilihan penapis mencukupi untuk keperluan carian saya."),
        1, 5, 3)

    listings_missing_filter = ""
    if listings_filter_sufficient <= 3:
        listings_missing_filter = st.text_input(
            q("What filter(s) were missing or unhelpful?",
              "Penapis apa yang tiada atau tidak berguna?"))

    listings_card_info = st.slider(
        q("Each property card showed enough information at a glance (image, price, type, location).",
          "Setiap kad hartanah menunjukkan maklumat yang mencukupi (gambar, harga, jenis, lokasi)."),
        1, 5, 3)

    listings_location_clarity = st.radio(
        q("Were you able to tell where each property is located from the listing card?",
          "Adakah anda dapat mengenal pasti lokasi hartanah dari kad senarai?"),
        (["Yes, very clear", "Somewhat clear", "No, it was confusing"]
         if EN else
         ["Ya, sangat jelas", "Agak jelas", "Tidak, ia mengelirukan"]),
        index=0,
    )

    listings_speed = st.slider(
        q("The page loaded fast enough while browsing listings.",
          "Halaman dimuatkan dengan cukup pantas semasa melayari senarai."),
        1, 5, 3)

    st.divider()

    # ── SECTION 3: Property Detail Page ──────────────────────────────────────
    section("Section 3 / Bahagian 3",
            "Property Detail Page",
            "Halaman Butiran Hartanah")

    st.caption(scale_label())

    detail_photos = st.slider(
        q("The property photos were clear, sufficient in number, and easy to browse.",
          "Foto hartanah jelas, mencukupi bilangannya, dan mudah dilayari."),
        1, 5, 3)

    detail_specs = st.slider(
        q("The property details (size, rooms, tenure, furnishing) were complete and easy to read.",
          "Butiran hartanah (saiz, bilik, pegangan, perabot) lengkap dan mudah dibaca."),
        1, 5, 3)

    detail_description = st.slider(
        q("The property description gave me enough info to decide whether to enquire further.",
          "Penerangan hartanah memberikan maklumat yang cukup untuk saya membuat keputusan."),
        1, 5, 3)

    detail_amenities = st.slider(
        q("The amenities and nearby facilities section was useful.",
          "Bahagian kemudahan dan fasiliti berdekatan adalah berguna."),
        1, 5, 3)

    detail_loan_calc = st.radio(
        q("Did you use the Loan Calculator on the property page?",
          "Adakah anda menggunakan Kalkulator Pinjaman pada halaman hartanah?"),
        (["Yes — it was helpful", "Yes — but it was confusing",
          "No — I didn't notice it", "No — I don't need it"]
         if EN else
         ["Ya — ia sangat berguna", "Ya — tetapi ia mengelirukan",
          "Tidak — saya tidak perasan", "Tidak — saya tidak memerlukannya"]),
        index=2,
    )

    detail_agent_contact = st.slider(
        q("The agent's contact info (phone, WhatsApp, email) was easy to find and use.",
          "Maklumat hubungan ejen (telefon, WhatsApp, emel) mudah ditemui dan digunakan."),
        1, 5, 3)

    detail_share = st.slider(
        q("The share buttons (WhatsApp, Facebook, Telegram) were easy to find.",
          "Butang kongsi (WhatsApp, Facebook, Telegram) mudah ditemui."),
        1, 5, 3)

    detail_fraud_notice = st.radio(
        q("The fraud/safety disclaimer at the bottom made me feel more confident.",
          "Notis penafian penipuan/keselamatan di bahagian bawah membuat saya lebih yakin."),
        (["Yes, it builds trust", "Neutral", "No, not necessary", "I didn't notice it"]
         if EN else
         ["Ya, ia membina kepercayaan", "Neutral",
          "Tidak, tidak perlu", "Saya tidak perasan"]),
        index=0,
    )

    st.divider()

    # ── SECTION 4: News Page ──────────────────────────────────────────────────
    section("Section 4 / Bahagian 4",
            "News Page  (findhouse.com.my/news)",
            "Halaman Berita  (findhouse.com.my/news)")

    visited_news = st.radio(
        q("Did you visit the FindHouse News page?",
          "Adakah anda melawati halaman Berita FindHouse?"),
        (["Yes", "No"] if EN else ["Ya", "Tidak"]),
        index=1,
    )

    news_visited = (visited_news == "Yes") or (visited_news == "Ya")

    news_browse        = None
    news_lang_switch   = None
    news_relevance     = None
    news_readability   = None
    news_view_source   = None
    news_share         = None
    news_value         = None

    if news_visited:
        st.caption(scale_label())

        news_browse = st.slider(
            q("The news articles were easy to browse and find topics of interest.",
              "Artikel berita mudah dilayari dan dicari mengikut topik yang diminati."),
            1, 5, 3)

        news_lang_switch = st.slider(
            q("The language switcher (English / BM / 中文) was easy to notice and use.",
              "Penukar bahasa (English / BM / 中文) mudah dilihat dan digunakan."),
            1, 5, 3)

        news_relevance = st.slider(
            q("The news content (property updates, guides, tips) was relevant and useful.",
              "Kandungan berita (kemas kini pasaran, panduan, tip) relevan dan berguna."),
            1, 5, 3)

        news_readability = st.slider(
            q("The article page layout was comfortable to read.",
              "Susun atur halaman artikel selesa untuk dibaca."),
            1, 5, 3)

        news_view_source = st.radio(
            q("The 'View Source' link (to the original article) was a useful feature.",
              "Pautan 'Lihat Sumber' (ke artikel asal) adalah ciri yang berguna."),
            (["Yes, I used it", "Yes, but I didn't use it",
              "I didn't notice it", "Not sure what it's for"]
             if EN else
             ["Ya, saya gunakannya", "Ya, tetapi saya tidak gunakannya",
              "Saya tidak perasan", "Tidak pasti fungsinya"]),
            index=0,
        )

        news_share = st.slider(
            q("Share buttons on news articles were easy to find.",
              "Butang kongsi pada artikel berita mudah ditemui."),
            1, 5, 3)

        news_value = st.slider(
            q("Overall, the news section adds value to the FindHouse website.",
              "Secara keseluruhan, bahagian berita menambah nilai kepada laman web FindHouse."),
            1, 5, 3)

    st.divider()

    # ── SECTION 5: Overall ────────────────────────────────────────────────────
    section("Section 5 / Bahagian 5",
            "Overall Experience", "Pengalaman Keseluruhan")

    overall_satisfaction = st.slider(
        q("Overall, how satisfied are you with FindHouse? (1 = Very Dissatisfied, 5 = Very Satisfied)",
          "Secara keseluruhan, sejauh mana berpuashati anda dengan FindHouse? (1 = Sangat Tidak Puas, 5 = Sangat Puas)"),
        1, 5, 3)

    encountered_issues = st.radio(
        q("Did you encounter any issues or confusion during your visit?",
          "Adakah anda menghadapi sebarang masalah atau kekeliruan semasa melawat?"),
        (["Yes", "No"] if EN else ["Ya", "Tidak"]),
        index=1,
    )

    issue_description = ""
    if encountered_issues in ["Yes", "Ya"]:
        issue_description = st.text_area(
            q("Please describe the issue briefly.",
              "Sila terangkan masalah tersebut secara ringkas."),
            height=80)

    liked_most = st.text_area(
        q("What do you like most about FindHouse?",
          "Apa yang paling anda sukai tentang FindHouse?"),
        height=80)

    improve_suggestion = st.text_area(
        q("What would you most like to see improved?",
          "Apa yang paling anda ingin lihat diperbaiki?"),
        height=80)

    nps = st.select_slider(
        q("How likely are you to recommend FindHouse to others? (0 = Not at all, 10 = Extremely likely)",
          "Sejauh mana kemungkinan anda mengesyorkan FindHouse kepada orang lain? (0 = Langsung tidak, 10 = Sangat mungkin)"),
        options=list(range(11)),
        value=7,
    )

    st.divider()

    submitted = st.form_submit_button(
        "✅ Submit Survey / Hantar Tinjauan",
        use_container_width=True,
        type="primary",
    )

# ── On submit ──────────────────────────────────────────────────────────────────
if submitted:
    # Basic validation
    errors = []
    if not role:
        errors.append("Please select your role / Sila pilih peranan anda.")
    if not device:
        errors.append("Please select your device / Sila pilih peranti anda.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        try:
            supabase = get_supabase()
            data = {
                "submitted_at":             datetime.utcnow().isoformat(),
                "language":                 lang,
                "role":                     role,
                "device":                   device,
                "pages_visited":            ", ".join(pages_visited),
                # Section 2
                "listings_clean":           listings_clean,
                "listings_filter_ease":     listings_filter_ease,
                "listings_filter_sufficient": listings_filter_sufficient,
                "listings_missing_filter":  listings_missing_filter,
                "listings_card_info":       listings_card_info,
                "listings_location_clarity": listings_location_clarity,
                "listings_speed":           listings_speed,
                # Section 3
                "detail_photos":            detail_photos,
                "detail_specs":             detail_specs,
                "detail_description":       detail_description,
                "detail_amenities":         detail_amenities,
                "detail_loan_calc":         detail_loan_calc,
                "detail_agent_contact":     detail_agent_contact,
                "detail_share":             detail_share,
                "detail_fraud_notice":      detail_fraud_notice,
                # Section 4
                "news_visited":             news_visited,
                "news_browse":              news_browse,
                "news_lang_switch":         news_lang_switch,
                "news_relevance":           news_relevance,
                "news_readability":         news_readability,
                "news_view_source":         news_view_source,
                "news_share":               news_share,
                "news_value":               news_value,
                # Section 5
                "overall_satisfaction":     overall_satisfaction,
                "encountered_issues":       encountered_issues,
                "issue_description":        issue_description,
                "liked_most":               liked_most,
                "improve_suggestion":       improve_suggestion,
                "nps_score":                nps,
            }
            supabase.table("findhouse_survey").insert(data).execute()

            st.markdown("""
            <div class="success-box">
                <h2>🎉 Thank you! / Terima kasih!</h2>
                <p>Your feedback has been submitted successfully.<br>
                <em>Maklum balas anda telah berjaya dihantar.</em></p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()

        except Exception as e:
            st.error(f"Submission failed. Please try again. / Penghantaran gagal. Sila cuba lagi.\n\n`{e}`")
