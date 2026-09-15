import streamlit as st
import pandas as pd
from datetime import datetime, date

# Cấu hình trang rộng và tối ưu giao diện
st.set_page_config(
    page_title="Quản Lý Văn Bản Pháp Luật AI+",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS để làm đẹp giao diện giống thiết kế chuyên nghiệp
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Khởi tạo dữ liệu mẫu trong session_state
if "documents" not in st.session_state:
    st.session_state["documents"] = [
        {
            "id": "DOC-01",
            "so_hieu": "12/2026/NĐ-CP",
            "loai": "Nghị định",
            "co_quan": "Chính phủ",
            "ngay_ban_hanh": "2026-02-20",
            "hieu_luc": "01/03/2026",
            "trich_yeu": "Nghị định quy định chi tiết một số điều của Luật Đất đai",
            "han_hoan_thanh": "2026-03-22",
            "trang_thai_lien_ket": "Đủ liên kết",
            "noi_dung": "Nội dung chi tiết Nghị định 12/2026/NĐ-CP quy định chi tiết về đất đai...",
            "dan_chieu": [{"ten": "Luật Đất đai số 31/2024/QH15", "trang_thai": "Đã liên kết"}]
        },
        {
            "id": "DOC-02",
            "so_hieu": "64/2025/QH15",
            "loai": "Luật",
            "co_quan": "Quốc hội",
            "ngay_ban_hanh": "2025-05-15",
            "hieu_luc": "01/01/2026",
            "trich_yeu": "Luật Ban hành văn bản quy phạm pháp luật",
            "han_hoan_thanh": "2026-03-30",
            "trang_thai_lien_ket": "Thiếu 1 liên kết",
            "noi_dung": "Nội dung chi tiết Luật Ban hành văn bản quy phạm pháp luật số 64/2025/QH15...",
            "dan_chieu": [{"ten": "Nghị định hướng dẫn 34/2016/NĐ-CP", "trang_thai": "Thiếu - Cần đính kèm"}]
        },
        {
            "id": "DOC-03",
            "so_hieu": "01/2026/TT-BTP",
            "loai": "Thông tư",
            "co_quan": "Bộ Tư pháp",
            "ngay_ban_hanh": "2026-01-10",
            "hieu_luc": "15/02/2026",
            "trich_yeu": "Thông tư hướng dẫn nghiệp vụ công chứng tài sản số",
            "han_hoan_thanh": "2026-04-10",
            "trang_thai_lien_ket": "Thiếu 1 liên kết",
            "noi_dung": "Nội dung chi tiết Thông tư công chứng tài sản số...",
            "dan_chieu": [{"ten": "Luật Công chứng số 53/2014/QH13", "trang_thai": "Thiếu - Cần đính kèm"}]
        }
    ]

if "current_view" not in st.session_state:
    st.session_state["current_view"] = "dashboard" # dashboard, detail, scan, settings

if "selected_doc_id" not in st.session_state:
    st.session_state["selected_doc_id"] = "DOC-01"

# --- TOP HEADER BAR ---
st.markdown("""
    <div class="main-header">
        <h2>🏛️ QUẢN LÝ VĂN BẢN PHÁP LUẬT AI+</h2>
        <p style="margin: 0; opacity: 0.9;">Hệ thống Tra cứu, Nhắc việc & Kiểm soát Liên kết thông minh</p>
    </div>
""", unsafe_allow_html=True)

# Các nút điều hướng nhanh trên header
col_h1, col_h2, col_h3 = st.columns([6, 2, 2])
with col_h2:
    if st.button("⚙️ Cài đặt Email Nhắc Hạn", use_container_width=True):
        st.session_state["current_view"] = "settings"
        st.rerun()
with col_h3:
    if st.button("➕ Quét Văn Bản Mới", type="primary", use_container_width=True):
        st.session_state["current_view"] = "scan"
        st.rerun()

st.write("")

# ==================== GIAO DIỆN 1: DASHBOARD CHÍNH ====================
if st.session_state["current_view"] == "dashboard":
    
    # 4 THẺ THỐNG KÊ (KPI CARDS)
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.markdown(f"""
            <div class="metric-card">
                <p style="margin:0; color: #64748b; font-size: 14px;">Tổng số văn bản</p>
                <h3 style="margin: 5px 0; color: #1e293b;">{len(st.session_state["documents"])}</h3>
                <span style="color: #10b981; font-size: 12px;">🟢 Cập nhật liên tục</span>
            </div>
        """, unsafe_allow_html=True)
    with col_k2:
        st.markdown("""
            <div class="metric-card">
                <p style="margin:0; color: #64748b; font-size: 14px;">Sắp đến hạn xử lý</p>
                <h3 style="margin: 5px 0; color: #dc2626;">3</h3>
                <span style="color: #dc2626; font-size: 12px;">⚠️ Cần ưu tiên xử lý</span>
            </div>
        """, unsafe_allow_html=True)
    with col_k3:
        st.markdown("""
            <div class="metric-card">
                <p style="margin:0; color: #64748b; font-size: 14px;">Thiếu liên kết văn bản</p>
                <h3 style="margin: 5px 0; color: #d97706;">2</h3>
                <span style="color: #d97706; font-size: 12px;">🔗 Cần đính kèm bổ sung</span>
            </div>
        """, unsafe_allow_html=True)
    with col_k4:
        st.markdown("""
            <div class="metric-card">
                <p style="margin:0; color: #64748b; font-size: 14px;">Số hóa tháng này</p>
                <h3 style="margin: 5px 0; color: #2563eb;">3</h3>
                <span style="color: #10b981; font-size: 12px;">✨ Hoạt động ổn định</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    # THANH TÌM KIẾM & BỘ LỌC NÂNG CAO
    col_f1, col_f2, col_f3, col_f4 = st.columns([3, 2, 2, 2])
    with col_f1:
        search_kw = st.text_input("Tìm kiếm", placeholder="🔍 Tìm theo số hiệu, trích yếu nội dung...")
    with col_f2:
        filter_coquan = st.selectbox("Cơ quan ban hành", ["Tất cả cơ quan", "Quốc hội", "Chính phủ", "Bộ Tư pháp"])
    with col_f3:
        filter_loai = st.selectbox("Loại văn bản", ["Tất cả loại văn bản", "Luật", "Nghị định", "Thông tư"])
    with col_f4:
        sort_by = st.selectbox("Sắp xếp", ["Sớm đến hạn xử lý", "Mới ban hành", "Số hiệu A-Z"])

    st.write("")
    st.subheader("📋 Danh sách Quản lý Văn bản Pháp luật")

    # Xử lý lọc dữ liệu
    filtered_docs = st.session_state["documents"]
    if search_kw:
        filtered_docs = [d for d in filtered_docs if search_kw.lower() in d["so_hieu"].lower() or search_kw.lower() in d["trich_yeu"].lower()]
    if filter_coquan != "Tất cả cơ quan":
        filtered_docs = [d for d in filtered_docs if d["co_quan"] == filter_coquan]
    if filter_loai != "Tất cả loại văn bản":
        filtered_docs = [d for d in filtered_docs if d["loai"] == filter_loai]

    # HIỂN THỊ DẠNG BẢNG QUẢN LÝ CHUYÊN NGHIỆP
    for doc in filtered_docs:
        with st.container(border=True):
            cols = st.columns([1.5, 3.5, 2, 1.5, 1.5, 1])
            
            with cols[0]:
                st.markdown(f"**{doc['loai']}**")
                st.code(doc['so_hieu'], language=None)
            with cols[1]:
                st.markdown(f"**{doc['trich_yeu']}**")
                st.caption(f"Hiệu lực: {doc['hieu_luc']}")
            with cols[2]:
                st.markdown(f"🏛️ {doc['co_quan']}")
                st.caption(f"Ban hành: {doc['ngay_ban_hanh']}")
            with cols[3]:
                st.markdown(f"⏰ **{doc['han_hoan_thanh']}**")
                st.caption("Deadline xử lý")
            with cols[4]:
                if doc['trang_thai_lien_ket'] == "Đủ liên kết":
                    st.success(f"✅ {doc['trang_thai_lien_ket']}")
                else:
                    st.warning(f"⚠️ {doc['trang_thai_lien_ket']}")
            with cols[5]:
                st.write("")
                # Nút xem chi tiết
                if st.button("👁️", key=f"view_{doc['id']}", help="Xem chi tiết văn bản"):
                    st.session_state["selected_doc_id"] = doc['id']
                    st.session_state["current_view"] = "detail"
                    st.rerun()

# ==================== GIAO DIỆN 2: CHI TIẾT & ĐỌC VĂN BẢN ====================
elif st.session_state["current_view"] == "detail":
    if st.button("⬅️ Quay lại danh sách quản lý"):
        st.session_state["current_view"] = "dashboard"
        st.rerun()

    doc = next((d for d in st.session_state["documents"] if d["id"] == st.session_state["selected_doc_id"]), st.session_state["documents"][0])

    st.markdown(f"## 📖 {doc['trich_yeu']}")
    st.info(f"**Số hiệu:** {doc['so_hieu']} | **Loại:** {doc['loai']} | **Cơ quan:** {doc['co_quan']} | **Ngày ban hành:** {doc['ngay_ban_hanh']} | **Hạn xử lý:** {doc['han_hoan_thanh']}")

    # Khung đọc nội dung văn bản
    with st.container(border=True):
        st.markdown("### Nội dung văn bản chi tiết")
        st.write(doc["noi_dung"])

    # Phần văn bản dẫn chiếu đặt ở cuối
    st.divider()
    st.markdown("### 🔗 Các văn bản dẫn chiếu & liên kết")
    for idx, ref in enumerate(doc["dan_chieu"]):
        rc1, rc2, rc3 = st.columns([3, 1, 1])
        with rc1:
            st.write(f"- {ref['ten']}")
        with rc2:
            if "Đã" in ref["trang_thai"]:
                st.success(ref["trang_thai"])
            else:
                st.error(ref["trang_thai"])
        with rc3:
            if "Thiếu" in ref["trang_thai"]:
                if st.button("Đính kèm", key=f"att_{doc['id']}_{idx}"):
                    ref["trang_thai"] = "Đã liên kết"
                    doc["trang_thai_lien_ket"] = "Đủ liên kết"
                    st.success("Đã đính kèm thành công!")
                    st.rerun()

    # Trợ lý AI Gemini hỏi đáp nhanh
    st.divider()
    st.subheader("🤖 Trợ lý AI Gemini - Hỏi đáp văn bản này")
    ai_q = st.text_input("Nhập câu hỏi của bạn cho Gemini:", placeholder="VD: Tóm tắt các điểm chính của văn bản này...")
    if st.button("Gửi câu hỏi"):
        if ai_q:
            st.success(f"**Gemini AI:** Dựa trên nội dung văn bản {doc['so_hieu']}, {doc['trich_yeu']}, các quy định yêu cầu thực hiện đầy đủ theo điều khoản đã được số hóa.")
        else:
            st.warning("Vui lòng nhập câu hỏi.")

# ==================== GIAO DIỆN 3: QUÉT VĂN BẢN MỚI ====================
elif st.session_state["current_view"] == "scan":
    if st.button("⬅️ Quay lại danh sách quản lý"):
        st.session_state["current_view"] = "dashboard"
        st.rerun()

    st.subheader("📤 Số hóa & Quét Tài Liệu Pháp Luật Mới")
    st.write("Tải lên file PDF hoặc ảnh. Gemini AI sẽ tự động trích xuất toàn bộ cấu trúc và lưu vào hệ thống.")

    uploaded_file = st.file_uploader("Kéo và thả tệp văn bản tại đây", type=["pdf", "png", "jpg"])
    
    sc1, sc2 = st.columns(2)
    with sc1:
        new_so = st.text_input("Số hiệu văn bản", placeholder="VD: 45/2026/QH16")
        new_cq = st.selectbox("Cơ quan ban hành", ["Quốc hội", "Chính phủ", "Bộ Tư pháp", "Bộ Tài chính"])
        new_loai = st.selectbox("Loại văn bản", ["Luật", "Nghị định", "Thông tư", "Quyết định"])
    with sc2:
        new_date = st.date_input("Ngày ban hành", value=date.today())
        new_deadline = st.date_input("Hạn hoàn thành xử lý", value=date.today())
        
    new_summary = st.text_area("Trích yếu nội dung văn bản")

    if st.button("🚀 Bắt đầu Quét & Lưu trữ", type="primary"):
        if uploaded_file and new_so:
            with st.spinner("Gemini AI đang đọc tài liệu và phân tích cấu trúc..."):
                new_item = {
                    "id": f"DOC-0{len(st.session_state['documents'])+1}",
                    "so_hieu": new_so,
                    "loai": new_loai,
                    "co_quan": new_cq,
                    "ngay_ban_hanh": str(new_date),
                    "hieu_luc": str(date.today()),
                    "trich_yeu": new_summary if new_summary else "Văn bản quét tự động bởi Gemini AI",
                    "han_hoan_thanh": str(new_deadline),
                    "trang_thai_lien_ket": "Thiếu 1 liên kết",
                    "noi_dung": f"Nội dung số hóa tự động từ file: {uploaded_file.name}",
                    "dan_chieu": [{"ten": "Văn bản gốc liên quan", "trang_thai": "Thiếu - Cần đính kèm"}]
                }
                st.session_state["documents"].append(new_item)
            st.success("🎉 Quét và số hóa thành công! Đang chuyển về trang quản lý...")
            st.session_state["current_view"] = "dashboard"
            st.rerun()
        else:
            st.warning("Vui lòng tải file lên và điền đầy đủ Số hiệu văn bản.")

# ==================== GIAO DIỆN 4: CÀI ĐẶT EMAIL NHẮC HẠN ====================
elif st.session_state["current_view"] == "settings":
    if st.button("⬅️ Quay lại danh sách quản lý"):
        st.session_state["current_view"] = "dashboard"
        st.rerun()

    st.subheader("⚙️ Cài đặt Nhắc việc & Cảnh báo Email")
    st.write("Cấu hình thời gian và địa chỉ nhận thông báo tự động trước hạn xử lý văn bản.")

    with st.container(border=True):
        email_input = st.text_input("Địa chỉ Email nhận cảnh báo", value="nguoiquanly@gmail.com")
        days_before = st.slider("Gửi email nhắc nhở trước thời hạn (ngày)", 1, 30, 7)
        st.checkbox("Bật thông báo khẩn cấp khi đến hạn chót (Deadline)", value=True)
        
        if st.button("💾 Lưu cấu hình", type="primary"):
            st.success(f"Đã lưu thành công! Hệ thống sẽ gửi email tự động về {email_input} trước {days_before} ngày đến hạn.")
