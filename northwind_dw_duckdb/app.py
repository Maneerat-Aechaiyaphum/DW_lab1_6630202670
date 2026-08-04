Python
import streamlit as st
import duckdb
import pandas as pd

# 1. Page config
st.set_page_config(
    page_title="Northwind DW Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Connect to database
DB_PATH = "northwindDW_duckdb2/dev.duckdb"

@st.cache_resource
def get_connection():
    return duckdb.connect(DB_PATH, read_only=True)

conn = get_connection()

# Helper function สั่งรัน SQL ปลอดภัย
def run_query(query):
    return conn.execute(query).df()

# ---------------------------------------------------------
# ส่วนโค้ดที่จะอยู่ต่อจากในภาพ (ส่วนการทำ UI & Dashboard)
# ---------------------------------------------------------

st.title("📊 Northwind DW Explorer")

# สร้าง Sidebar สำหรับเลือกดูตาราง หรือฟิลเตอร์ข้อมูล
st.sidebar.header("Navigation")
menu_choice = st.sidebar.radio(
    "เลือกเมนู", 
    ["Overview / KPI", "Sales Analysis", "Custom SQL Query"]
)

# --- หน้าที่ 1: สรุปภาพรวม (Overview / KPI) ---
if menu_choice == "Overview / KPI":
    st.subheader("ภาพรวมยอดขาย")
    
    # ดึงยอดขายรวม ตัวอย่างการ Query จาก DuckDB
    sales_df = run_query("""
        SELECT 
            COUNT(DISTINCT order_id) AS total_orders,
            SUM(net_amount) AS total_revenue
        FROM fct_orders  -- ตัวอย่าง table สรุปยอดขาย
    """)
    
    # แสดงตัวเลข KPI
    col1, col2 = st.columns(2)
    col1.metric("จำนวนคำสั่งซื้อทั้งหมด", f"{sales_df['total_orders'][0]:,}")
    col2.metric("รายได้รวม (USD)", f"${sales_df['total_revenue'][0]:,.2f}")

# --- หน้าที่ 2: วิเคราะห์ยอดขาย (Sales Analysis) ---
elif menu_choice == "Sales Analysis":
    st.subheader("ยอดขายแยกตามหมวดหมู่สินค้า")
    
    cat_df = run_query("""
        SELECT category_name, SUM(net_amount) as total_sales
        FROM dim_products p
        JOIN fct_orders o ON p.product_id = o.product_id
        GROUP BY category_name
        ORDER BY total_sales DESC
    """)
    
    # แสดงกราฟแท่ง
    st.bar_chart(cat_df.set_index("category_name"))
    
    # แสดงตารางข้อมูลเพิ่มเติม
    with st.expander("ดูตารางข้อมูลรายละเอียด"):
        st.dataframe(cat_df, use_container_width=True)

# --- หน้าที่ 3: รัน SQL แบบกำหนดเอง (Custom Query) ---
elif menu_choice == "Custom SQL Query":
    st.subheader("ทดสอบเขียน SQL ควบคุมเอง")
    
    default_sql = "SELECT * FROM information_schema.tables LIMIT 10;"
    user_query = st.text_area("กรอก SQL Query:", value=default_sql, height=120)
    
    if st.button("Run Query"):
        try:
            result_df = run_query(user_query)
            st.write(f"ผลลัพธ์ทั้งหมด {len(result_df)} แถว:")
            st.dataframe(result_df)
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในระบบ SQL: {e}")