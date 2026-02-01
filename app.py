import streamlit as st
import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt  # 히트맵 에러 방지용
from datetime import datetime

# 1. 페이지 설정 (에러 해결: layout="centered")
st.set_page_config(page_title="12:10 Premium", layout="centered")

# 2. [디자인] 프리미엄 다크 모드 CSS (전체 적용)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    /* 전체 배경: 딥 블랙 & 텍스트 화이트 */
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* 입력창 커스텀 (어두운 배경) */
    .stTextInput > div > div > input { color: white; background-color: #2C2C2C; border: none; }
    .stSelectbox > div > div > div { color: white; background-color: #2C2C2C; }
    .stNumberInput > div > div > input { color: white; background-color: #2C2C2C; }
    
    /* 캘린더 및 버튼 스타일 */
    div.stButton > button {
        background-color: #2C2C2C;
        border: 1px solid #333;
        color: white;
        border-radius: 10px;
        transition: 0.3s;
        width: 100%;
    }
    div.stButton > button:hover { border-color: #2979FF; color: #2979FF; }
    
    /* [핵심] 포인트 버튼 (주문/등록 등 주요 액션) */
    .primary-btn {
        background-color: #2979FF !important; 
        color: white !important;
        border: none !important;
        font-weight: 800 !important;
    }
    
    /* 카드 디자인 (메뉴, 통계 박스) */
    .menu-card {
        background-color: #1E1E1E;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        border: 1px solid #333;
    }
    
    /* 텍스트 컬러 강제 지정 */
    h1, h2, h3, h4 { color: #FFFFFF !important; }
    p, span, div, label { color: #E0E0E0; }
    .highlight { color: #2979FF; font-weight: bold; }
    .sub-text { font-size: 0.8rem; color: #888; }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1E1E1E; border-radius: 10px; color: white; border: none; }
    .stTabs [aria-selected="true"] { background-color: #2979FF !important; color: white !important; }
    
    /* 데이터프레임(표) 다크모드 대응 */
    [data-testid="stDataFrame"] { background-color: #1E1E1E; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 초기화 (모든 기능용 데이터)
if 'menu_db' not in st.session_state:
    st.session_state.menu_db = {
        1: {"name": "직화 제육볼", "img": "https://images.unsplash.com/photo-1626071466175-79aba923853e?w=400", "kcal": "650", "price": 7500},
        2: {"name": "연어 포케", "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400", "kcal": "480", "price": 8500},
        3: {"name": "스테이크 덮밥", "img": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=400", "kcal": "720", "price": 9000},
        4: {"name": "닭가슴살 샐러드", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", "kcal": "350", "price": 7000},
        5: {"name": "매콤 찜닭", "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=400", "kcal": "600", "price": 7500},
    }
    for i in range(6, 32):
        st.session_state.menu_db[i] = {"name": "셰프 특선 도시락", "img": "https://images.unsplash.com/photo-1544124499-58912cbddaad?w=400", "kcal": "500", "price": 7500}

if 'user_db' not in st.session_state: st.session_state.user_db = {"admin": "1234", "user": "1234"}
if 'orders' not in st.session_state: st.session_state.orders = pd.DataFrame()
if 'purchases' not in st.session_state: st.session_state.purchases = pd.DataFrame() # 지출 장부 (필수)
if 'history_df' not in st.session_state: # 보고서용 데이터 (필수)
    dates = pd.date_range(end=datetime.now(), periods=30)
    history_data = [{'날짜': d.strftime("%Y-%m-%d"), '총매출': np.random.randint(20,100)*7500, '총매입(원가)': np.random.randint(20,100)*4000} for d in dates]
    st.session_state.history_df = pd.DataFrame(history_data)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().day

# ==========================================
# [화면 1] 로그인 & 회원가입 (다크모드)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2979FF; font-size: 3rem;'>12:10</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Premium Lunch Service</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["LOG IN", "SIGN UP"])
        
        with tab1:
            id_in = st.text_input("Username", key="login_id")
            pw_in = st.text_input("Password", type="password", key="login_pw")
            if st.button("Sign In", type="primary", use_container_width=True):
                if id_in in st.session_state.user_db and st.session_state.user_db[id_in] == pw_in:
                    st.session_state.logged_in = True
                    st.session_state.user_name = id_in
                    st.session_state.user_role = "admin" if id_in == "admin" else "user"
                    st.rerun()
                else: st.error("Check ID/PW")
        
        with tab2:
            new_id = st.text_input("New ID")
            new_pw = st.text_input("New Password", type="password")
            if st.button("Create Account", use_container_width=True):
                if new_id:
                    st.session_state.user_db[new_id] = new_pw
                    st.success("Account Created!")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# [화면 2] 메인 앱
# ==========================================
else:
    c1, c2 = st.columns([5, 1])
    with c1: st.markdown(f"### Hello, {st.session_state.user_name}")
    with c2: 
        if st.button("Exit"): 
            st.session_state.logged_in = False
            st.rerun()

    # ----------------------------------
    # [A] 사용자 화면: 캘린더 + 주문
    # ----------------------------------
    if st.session_state.user_role == "user":
        
        # 1. 메인 배너
        today = datetime.now().day
        today_menu = st.session_state.menu_db[today]
        
        st.markdown(f"<div class='sub-text'>Today's Lunch</div>", unsafe_allow_html=True)
        st.markdown(f"<h2>{today_menu['name']}</h2>", unsafe_allow_html=True)
        st.image(today_menu['img'], use_container_width=True)
        
        st.markdown("---")
        
        # 2. 캘린더 뷰
        st.markdown("### 📅 February 2026")
        cal = calendar.monthcalendar(2026, 2)
        days_header = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        
        cols = st.columns(7)
        for idx, day in enumerate(days_header):
            cols[idx].markdown(f"<div style='text-align:center; font-size:0.7rem; color:#888;'>{day}</div>", unsafe_allow_html=True)
            
        for week in cal:
            cols = st.columns(7)
            for idx, day in enumerate(week):
                with cols[idx]:
                    if day != 0:
                        if st.button(f"{day}", key=f"d_{day}", use_container_width=True):
                            st.session_state.selected_date = day
                            st.rerun()
        
        st.markdown("---")
        
        # 3. 상세 메뉴 및 주문
        sel_day = st.session_state.selected_date
        sel_menu = st.session_state.menu_db.get(sel_day, today_menu)
        
        st.markdown(f"<div class='menu-card'>", unsafe_allow_html=True)
        st.markdown(f"<span class='highlight'>{sel_day}일 메뉴</span>", unsafe_allow_html=True)
        st.markdown(f"<h3>{sel_menu['name']}</h3>", unsafe_allow_html=True)
        
        c_img, c_info = st.columns([1, 1.5])
        with c_img: st.image(sel_menu['img'], use_container_width=True)
        with c_info:
            st.markdown(f"""
            <div style='margin-left:10px;'>
                <p>🔥 {sel_menu['kcal']} kcal</p>
                <p>💰 {sel_menu['price']:,} KRW</p>
                <p style='color:#888; font-size:0.8rem;'>Fresh ingredients, <br>Daily cooked.</p>
            </div>
            """, unsafe_allow_html=True)
            
        qty = st.number_input("Quantity", 1, 10, 1)
        bld = st.selectbox("Office Location", ["Smart Bay", "O-Biz Tower", "Techno Valley"])
        
        if st.button("ADD TO CART & PAY", type="primary", use_container_width=True):
            new_ord = {
                'Date': f"2026-02-{sel_day}",
                'User': st.session_state.user_name,
                'Menu': sel_menu['name'],
                'Qty': qty,
                'Total': qty * sel_menu['price'],
                'Location': bld
            }
            st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_ord])], ignore_index=True)
            st.success(f"Order Confirmed for Feb {sel_day}!")
        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------
    # [B] 관리자 화면: 풀옵션 (지출/분석/보고서 포함)
    # ----------------------------------
    elif st.session_state.user_role == "admin":
        st.markdown("### 📊 Admin HQ")
        
        df_ord = st.session_state.orders
        df_buy = st.session_state.purchases
        
        # 사장님이 원하시던 기능 탭으로 완전 분리
        adm_tab1, adm_tab2, adm_tab3, adm_tab4 = st.tabs(["Dashboard", "Orders & Heatmap", "Expenses", "Reports"])
        
        # [탭1] 대시보드
        with adm_tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("<div class='menu-card' style='text-align:center;'>", unsafe_allow_html=True)
                total_sales = df_ord['Total'].sum() if not df_ord.empty else 0
                st.metric("Total Sales", f"{total_sales:,}")
                st.markdown("</div>", unsafe_allow_html=True)
            with c2:
                st.markdown("<div class='menu-card' style='text-align:center;'>", unsafe_allow_html=True)
                total_qty = df_ord['Qty'].sum() if not df_ord.empty else 0
                st.metric("Total Boxes", f"{total_qty}")
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
            st.markdown("#### Sales Trend")
            if not df_ord.empty:
                st.bar_chart(df_ord.groupby('Date')['Total'].sum(), color="#2979FF")
            else: st.info("No sales yet.")
            st.markdown("</div>", unsafe_allow_html=True)

        # [탭2] 주문 및 히트맵 분석 (복구됨!)
        with adm_tab2:
            st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
            st.markdown("#### Real-time Orders")
            st.dataframe(df_ord, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
            st.markdown("#### Menu x Location Analysis")
            if not df_ord.empty:
                heatmap = pd.pivot_table(df_ord, values='Qty', index='Menu', columns='Location', aggfunc='sum', fill_value=0)
                st.dataframe(heatmap.style.background_gradient(cmap='Blues'), use_container_width=True)
            else: st.info("Data needed for analysis.")
            st.markdown("</div>", unsafe_allow_html=True)

        # [탭3] 지출 입력 (복구됨!)
        with adm_tab3:
            st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
            st.markdown("#### Register Expenses")
            with st.form("exp_form", clear_on_submit=True):
                ex_name = st.text_input("Item Name")
                ex_cost = st.number_input("Cost (KRW)", step=1000)
                if st.form_
