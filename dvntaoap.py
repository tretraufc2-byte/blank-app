import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Cấu hình giao diện trang web
st.set_page_config(page_title="Quản Lý Điểm Sinh Viên", layout="wide")

# Tiêu đề ứng dụng
st.markdown(
    "<h1 style='text-align: center; color: #1f77b4;'>QUẢN LÝ ĐIỂM SINH VIÊN</h1>",
    unsafe_allow_html=True,
)
st.write("---")

# Dữ liệu mẫu chuẩn theo tài liệu
data = {
    "Ho_va_ten": [
        "Nguyễn Văn An",
        "Trần Thị Bích",
        "Lê Hoàng Cường",
        "Phạm Thị Dung",
        "Hoàng Văn Em",
        "Vũ Thị Phương",
        "Đỗ Minh Giang",
        "Bùi Thị Hoa",
        "Ngô Văn Hùng",
        "Dương Thị Linh",
    ],
    "Chuyen_can": [8.5, 9.0, 7.5, 6.0, 8.0, 9.5, 4.5, 7.0, 8.5, 6.5],
    "Giua_ky": [7.0, 8.5, 6.0, 5.5, 7.5, 9.0, 4.0, 6.5, 8.0, 5.0],
    "Cuoi_ky": [8.0, 8.5, 7.0, 5.0, 7.5, 9.0, 4.5, 6.0, 8.5, 5.5],
}

df = pd.DataFrame(data)

# Tính tổng kết và xếp loại
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"] + 0.3 * df["Giua_ky"] + 0.5 * df["Cuoi_ky"]
).round(2)


def xep_loai(diem):
  if diem >= 8.5:
    return "Giỏi"
  elif diem >= 7.0:
    return "Khá"
  elif diem >= 5.0:
    return "Trung bình"
  else:
    return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 1. Hiển thị bảng điểm
st.subheader("📋 Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df, use_container_width=True)

# 2. Thống kê cơ bản
st.subheader("📊 Thống kê chung của lớp")
col1, col2, col3, col4 = st.columns(4)

dtb_lop = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5.0).sum()

with col1:
  st.metric(label="Điểm TB của lớp", value=f"{dtb_lop:.2f}")
with col2:
  st.metric(
      label="Điểm cao nhất",
      value=f"{sv_max['Tong_ket']}",
      delta=sv_max["Ho_va_ten"],
  )
with col3:
  st.metric(
      label="Điểm thấp nhất",
      value=f"{sv_min['Tong_ket']}",
      delta=sv_min["Ho_va_ten"],
      delta_color="inverse",
  )
with col4:
  st.metric(label="Số sinh viên đạt (>=5.0)", value=f"{so_sv_dat}/{len(df)}")

st.write("---")

# 3. Tra cứu thông tin từng sinh viên
st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên cần xem:", df["Ho_va_ten"])

student_info = df[df["Ho_va_ten"] == selected_student].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", student_info["Chuyen_can"])
c2.metric("Giữa kỳ", student_info["Giua_ky"])
c3.metric("Cuối kỳ", student_info["Cuoi_ky"])
c4.metric("Tổng kết", student_info["Tong_ket"])
c5.metric("Xếp loại", student_info["Xep_loai"])

st.write("---")

# 4. Trực quan hóa biểu đồ (Giống hệt phong cách tài liệu)
st.subheader("📈 Biểu đồ thể hiện điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(
    df["Ho_va_ten"],
    df["Tong_ket"],
    color="skyblue",
    edgecolor="darkblue",
    linewidth=1.2,
)
ax.set_title(
    "Biểu đồ thể hiện điểm tổng kết của 10 sinh viên",
    fontsize=14,
    fontweight="bold",
)
ax.set_xlabel("Họ và tên sinh viên", fontsize=12)
ax.set_ylabel("Điểm tổng kết", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.ylim(0, 10)
ax.grid(axis="y", linestyle="--", alpha=0.6)

for bar in bars:
  yval = bar.get_height()
  ax.text(
      bar.get_x() + bar.get_width() / 2.0,
      yval + 0.1,
      str(yval),
      ha="center",
      va="bottom",
      fontsize=9,
      fontweight="bold",
  )

plt.tight_layout()
st.pyplot(fig)

# 5. Thông tin người tạo
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: small;'>Người"
    " tạo: Dương Văn Ngân - MSSV: 067207006057</p>",
    unsafe_allow_html=True,
)
