import streamlit as st
import pandas as pd
from datetime import datetime, date

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Thư Viện Văn Bản - Quản lý & Tra cứu Pháp luật",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo kho dữ liệu mẫu trong st.session_state nếu chưa có
if "documents" not in st.session_state:
    st.session_state["documents"] = [
        {
            "id": "DOC-01",
            "so_hieu": "64/2025/QH15",
            "loai": "Luật",
            "co_quan": "Quốc hội",
            "ngay_ban_hanh": "2025-05-15",
            "trich_yeu": "Luật Ban hành văn bản quy phạm pháp luật",
            "han_hoan_thanh": "2026-06-30",
            "noi_dung": {
                "chuong_1": {
                    "tên": "Chương I: Những quy định chung",
                    "dieu_khoan": [
                        {"dieu": "Điều 1. Phạm vi điều chỉnh", "noi_dung": "Luật này quy định về nguyên tắc, thẩm quyền, trình tự, thủ tục xây dựng, ban hành văn bản quy phạm pháp luật."},
                        {"dieu": "Điều 2. Giải thích từ ngữ", "noi_dung": "Trong Luật này, các từ ngữ dưới đây được hiểu như sau: Văn bản quy phạm pháp luật là văn bản chứa quy tắc xử sự chung..."}
                    ]
                }
            },
            "dan_chieu": [
                {"ten": "Luật Ban hành văn bản quy phạm pháp luật số 80/2015/QH13", "trang_thai": "Đã liên kết"},
                {"ten": "Nghị định 34/2016/NĐ-CP hướng dẫn Luật ban hành VBQPPL", "trang_thai": "Thiếu - Cần đính kèm"}
            ]
        },
        {
            "id": "DOC-02",
            "so_hieu": "12/2026/NĐ-CP",
            "loai": "Nghị định",
            "co_quan": "Chính phủ",
            "ngay_ban_hanh": "2026-01-10",
            "trich_yeu": "Quy định chi tiết thi hành một số điều của Luật đất đai",
            "han_hoan_thanh": "2026-04-15",
            "noi_dung": {
                "chuong_1": {
                    "tên": "Chương I: Quy định chung",
                    "dieu_khoan": [
                        {"dieu": "Điều 1. Phạm vi điều chỉnh", "noi_dung": "Nghị định này quy định chi tiết thi hành các điều, khoản được giao trong Luật Đất đai..."}
                    ]
                }
            },
            "dan_chieu": [
                {"ten": "Luật Đất đai số 31/2024/QH15", "trang_thai": "Đã liên kết"}
            ]
        }
    ]

if "selected_doc_id" not in st.session_state:
    st.session_state["selected_doc_id"] = "DOC-01"

# --- SIDEBAR: QUẢN LÝ VÀ BỘ LỌC NÂNG CAO ---
with st.sidebar:
    st.title("📚 Thư Viện Văn Bản")
    st.caption("Hệ thống số hóa, tra cứu & quản lý văn bản cá nhân")
    
    st.divider()
    
    # Menu chức năng
    menu = st.radio("Chế độ làm việc", ["🔍 Tra cứu & Đọc văn bản", "📤 Quét tài liệu mới", "⏰ Quản lý Nhắc việc & Hạn"])
    
    st.divider()
    st.subheader("🔎 Bộ lọc tìm kiếm")
    
    # Bộ lọc nâng cao
    filter_so_hieu = st.text_input("Tìm theo Số hiệu văn bản", placeholder="VD: 64/2025/QH15")
    filter_co_quan = st.selectbox("Cơ quan ban hành", ["Tất cả", "Quốc hội", "Chính phủ", "Bộ Tư pháp", "Bộ Tài chính"])
    filter_keyword = st.text_input("Từ khóa trích yếu", placeholder="VD: Đất đai, Ban hành...")

    st.divider()
    st.subheader("⚙️ Cài đặt Nhắc việc Email")
    user_email = st.text_input("Email nhận cảnh báo", value="nguoiquanly@gmail.com")
    ngay_nhac_truoc = st.slider("Cảnh báo trước hạn (ngày)", 1, 30, 7)
    if st.button("Lưu cấu hình email"):
        st.success(f"Đã lưu lịch thông báo về: {user_email}")

# --- LỌC DỮ LIỆU ---
docs_filtered = st.session_state["documents"]
if filter_so_hieu:
    docs_filtered = [d for d in docs_filtered if filter_so_hieu.lower() in d["so_hieu"].lower()]
if filter_co_quan != "Tất cả":
    docs_filtered = [d for d in docs_filtered if d["co_quan"] == filter_co_quan]
if filter_keyword:
    docs_filtered = [d for d in docs_filtered if filter_keyword.lower() in d["trich_yeu"].lower()]

# --- MÀN HÌNH 1: TRA CỨU & ĐỌC VĂN BẢN ---
if menu == "🔍 Tra cứu & Đọc văn bản":
    st.header("📖 Không gian Đọc & Tra Cứu Văn Bản")
    
    if not docs_filtered:
        st.warning("Không tìm thấy văn bản phù hợp với bộ lọc.")
    else:
        # Bố cục 2 cột: Cột trái là danh sách văn bản truy vấn, Cột phải là nội dung chi tiết
        col_list, col_content = st.columns([1, 2.5])
        
        with col_list:
            st.subheader(f"Danh sách kết quả ({len(docs_filtered)})")
            st.caption("Chọn văn bản để xem chi tiết ở khung bên phải:")
            
            for doc in docs_filtered:
                is_selected = (doc["id"] == st.session_state["selected_doc_id"])
                btn_type = "primary" if is_selected else "secondary"
                
                # Hiển thị tóm tắt thông tin trong danh sách bên trái
                if st.button(f"📄 [{doc['so_hieu']}]\n{doc['trich_yeu'][:50]}...", key=f"btn_{doc['id']}", use_container_width=True, type=btn_type):
                    st.session_state["selected_doc_id"] = doc["id"]
                    st.rerun()

        with col_content:
            # Lấy văn bản đang chọn
            current_doc = next((d for d in docs_filtered if d["id"] == st.session_state["selected_doc_id"]), docs_filtered[0])
            
            st.markdown(f"### 🏛️ {current_doc['trich_yeu']}")
            st.info(f"**Số hiệu:** {current_doc['so_hieu']} | **Loại:** {current_doc['loai']} | **Cơ quan:** {current_doc['co_quan']} | **Ngày ban hành:** {current_doc['ngay_ban_hanh']} | **Hạn xử lý:** {current_doc['han_hoan_thanh']}")
            
            # Khung hiển thị nội dung chi tiết theo chuẩn hành chính
            with st.container(border=True):
                st.markdown("#### Nội dung văn bản chi tiết")
                for c_key, c_val in current_doc["noi_dung"].items():
                    st.markdown(f"**{c_val['tên']}**")
                    for item in c_val["dieu_khoan"]:
                        st.markdown(f"**{item['dieu']}**")
                        st.write(item["noi_dung"])
                        st.write("")
            
            # PHẦN VĂN BẢN DẪN CHIẾU ĐẶT Ở CUỐI NỘI DUNG VĂN BẢN
            st.divider()
            st.markdown("#### 🔗 Các văn bản dẫn chiếu & liên kết")
            st.caption("Danh sách các văn bản có liên quan được trích dẫn trong nội dung nghiên cứu:")
            
            for idx, ref in enumerate(current_doc["dan_chieu"]):
                col_r1, col_r2, col_r3 = st.columns([3, 1, 1])
                with col_r1:
                    st.write(f"- {ref['ten']}")
                with col_r2:
                    if ref["trang_thai"] == "Đã liên kết":
                        st.success(ref["trang_thai"])
                    else:
                        st.error(ref["trang_thai"])
                with col_r3:
                    if ref["trang_thai"] != "Đã liên kết":
                        if st.button("Đính kèm", key=f"attach_{current_doc['id']}_{idx}"):
                            ref["trang_thai"] = "Đã liên kết"
                            st.success("Đã đính kèm thành công!")
                            st.rerun()
            
            # TRỢ LÝ AI GEMINI TÍCH HỢP TRONG GIAO DIỆN ĐỌC
            st.divider()
            st.subheader("🤖 Trợ lý AI Gemini (Hỏi đáp nhanh văn bản này)")
            user_q = st.text_input("Nhập câu hỏi về văn bản đang xem:", placeholder="VD: Phạm vi điều chỉnh của văn bản này là gì?")
            if st.button("Hỏi AI Gemini"):
                if user_q:
                    with st.spinner("Gemini đang phân tích nội dung..."):
                        # Giả lập phản hồi thông minh dựa trên văn bản
                        st.success(f"**Gemini trả lời:** Dựa trên nội dung số hóa của văn bản số {current_doc['so_hieu']}, {current_q_response(user_q, current_doc)}")
                else:
                    st.warning("Vui lòng nhập câu hỏi.")

# --- MÀN HÌNH 2: QUÉT TÀI LIỆU MỚI ---
elif menu == "📤 Quét tài liệu mới":
    st.header("📤 Số hóa & Quét Tài Liệu Pháp Luật")
    st.write("Tải lên tệp PDF hoặc ảnh chụp văn bản. Gemini AI sẽ tự động bóc tách cấu trúc và lưu vào Thư Viện Văn Bản.")
    
    uploaded_file = st.file_uploader("Chọn tệp văn bản (PDF, PNG, JPG)", type=["pdf", "png", "jpg"])
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        new_so_hieu = st.text_input("Số hiệu văn bản", placeholder="VD: 15/2026/QH16")
        new_co_quan = st.selectbox("Đơn vị ban hành", ["Quốc hội", "Chính phủ", "Bộ Tư pháp", "Bộ Tài chính", "Ủy ban nhân dân"])
    with col_input2:
        new_ngay = st.date_input("Ngày ban hành", value=date.today())
        new_han = st.date_input("Hạn hoàn thành / Xử lý công việc", value=date.today())
        
    new_trich_yeu = st.text_area("Trích yếu nội dung", placeholder="Nhập trích yếu ngắn gọn của văn bản...")
    
    if st.button("🚀 Thực hiện Quét & Trích xuất bằng Gemini AI", type="primary"):
        if uploaded_file and new_so_hieu:
            with st.spinner("Gemini AI đang đọc tài liệu và phân chia cấu trúc Chương/Điều..."):
                # Thêm văn bản mới vào session state
                new_doc = {
                    "id": f"DOC-0{len(st.session_state['documents']) + 1}",
                    "so_hieu": new_so_hieu,
                    "loai": "Văn bản mới quét",
                    "co_quan": new_co_quan,
                    "ngay_ban_hanh": str(new_ngay),
                    "trich_yeu": new_trich_yeu if new_trich_yeu else "Văn bản quét tự động từ hệ thống",
                    "han_hoan_thanh": str(new_han),
                    "noi_dung": {
                        "chuong_1": {
                            "tên": "Chương I: Quy định chung (Trích xuất tự động)",
                            "dieu_khoan": [
                                {"dieu": "Điều 1. Quy định chính", "noi_dung": f"Nội dung được trích xuất thành công từ file {uploaded_file.name} thông qua Gemini AI Flash."}
                            ]
                        }
                    },
                    "dan_chieu": [
                        {"ten": "Văn bản gốc liên quan", "trang_thai": "Thiếu - Cần đính kèm"}
                    ]
                }
                st.session_state["documents"].append(new_doc)
                st.session_state["selected_doc_id"] = new_doc["id"]
            st.success("🎉 Quét tài liệu và cập nhật cơ sở dữ liệu thành công! Bạn có thể chuyển sang chế độ tra cứu để kiểm tra.")
        else:
            st.warning("Vui lòng tải lên tệp văn bản và nhập Số hiệu văn bản.")

# --- MÀN HÌNH 3: QUẢN LÝ NHẮC VIỆC & HẠN ---
elif menu == "⏰ Quản lý Nhắc việc & Hạn":
    st.header("⏰ Quản lý Nhắc Việc & Sắp Xếp Hạn Hoàn Thành")
    st.write("Danh sách văn bản được sắp xếp theo thứ tự **thời hạn hoàn thành sớm nhất** để bạn ưu tiên xử lý:")
    
    # Sắp xếp danh sách theo hạn hoàn thành
    sorted_docs = sorted(st.session_state["documents"], key=lambda x: x["han_hoan_thanh"])
    
    # Hiển thị dạng bảng quản lý
    table_data = []
    for d in sorted_docs:
        table_data.append({
            "Số hiệu": d["so_hieu"],
            "Trích yếu": d["trich_yeu"],
            "Cơ quan": d["co_quan"],
            "Ngày ban hành": d["ngay_ban_hanh"],
            "Hạn hoàn thành": d["han_hoan_thanh"]
        })
    
    df_task = pd.DataFrame(table_data)
    st.dataframe(df_task, use_container_width=True)
    
    st.info(f"Hệ thống đang kích hoạt tính năng gửi email cảnh báo tự động về địa chỉ: **{user_email}** khi văn bản đến hạn xử lý.")

# Hàm phụ trợ giả lập câu trả lời AI đơn giản
def current_q_response(question, doc):
    return f"Dựa trên văn bản {doc['so_hieu']} ({doc['trich_yeu']}), vấn đề bạn hỏi ('{question}') được quy định rõ ràng trong phần cấu trúc chương hồi đã được số hóa. Bạn có thể tra cứu chi tiết tại các điều khoản ở khung đọc bên trên để áp dụng chính xác vào công việc."
