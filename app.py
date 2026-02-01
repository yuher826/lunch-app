import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

# 1. 페이지 설정 (다크 모드 감성)
st.set_page_config(page_title="12:10 든든밀 Pro", layout="mobile")

# 2. [디자인] 프리미엄 다크 모드 CSS (디자인 100% 분석 적용)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    /* 전체 배경: 딥 블랙 */
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* 입력창 디자인 (어두운 배경) */
    .stTextInput > div > div > input { color: white; background-color: #2C2C2C; border: none; }
    .stSelectbox > div > div > div { color: white; background-color: #2C2C2C; }
    
    /* 캘린더 날짜 버튼 스타일 */
    .date-btn {
        background-color: #2C2C2C;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        margin-bottom: 5px;
        cursor: pointer;
        transition: 0.3s;
    }
    .date-btn:hover { border-color: #2979FF; background-color: #1E1E1E; }
    
    /* 메인 카드 디자인 */
    .menu-card {
        background-color: #1E1E1E;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* [핵심] 포인트 버튼 (일렉트릭 블루) */
    div.stButton > button {
        background-color: #2979FF !important; 
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 800 !important;
        padding: 12px 0px !important;
        width: 100%;
        margin-top: 10px;
    }
    div.stButton > button:hover { opacity: 0.9; }
    
    /* 텍스트 컬러 정리 */
    h1, h2, h3 { color: #FFFFFF !important; }
    p, span, div { color: #E0E0E0; }
    .highlight { color: #2979FF; font-weight: bold; }
    .sub-text { font-size: 0.8rem; color: #888; }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1E1E1E; border-radius: 10px; color: white; border: none; }
    .stTabs [aria-selected="true"] { background-color: #2979FF !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 초기화
if 'menu_db' not in st.session_state:
    # 날짜별 메뉴 데이터 (2월 예시)
    st.session_state.menu_db = {
        1: {"name": "직화 제육볼", "img": "https://images.unsplash.com/photo-1626071466175-79aba923853e?w=400", "kcal": "650", "price": 7500},
        2: {"name": "연어 포케", "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400", "kcal": "480", "price": 8500},
        3: {"name": "스테이크 덮밥", "img": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=400", "kcal": "720", "price": 9000},
        4: {"name": "닭가슴살 샐러드", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", "kcal": "350", "price": 7000},
        5: {"name": "매콤 찜닭", "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=400", "kcal": "600", "price": 7500},
    }
    # 나머지 날짜는 랜덤 채우기
    for i in range(6, 32):
        st.session_state.menu_db[i] = {"name": "오늘의 셰프 특선", "img": "https://images.unsplash.com/photo-1544124499-58912cbddaad?w=400", "kcal": "500", "price": 7500}

if 'user_db' not in st.session_state: st.session_state.user_db = {"admin": "1234", "user": "1234"}
if 'orders' not in st.session_state: st.session_state.orders = pd.DataFrame()
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().day

# ==========================================
# [화면 1] 다크 모드 로그인
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2979FF;'>12:10</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Premium Lunch Service</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["LOG IN", "SIGN UP"])
        
        with tab1:
            id_in = st.text_input("Username", key="login_id")
            pw_in = st.text_input("Password", type="password", key="login_pw")
            if st.button("Sign In"):
                if id_in in st.session_state.user_db and st.session_state.user_db[id_in] == pw_in:
                    st.session_state.logged_in = True
                    st.session_state.user_name = id_in
                    st.session_state.user_role = "admin" if id_in == "admin" else "user"
                    st.rerun()
                else: st.error("Check ID/PW")
        
        with tab2:
            new_id = st.text_input("New ID")
            new_pw = st.text_input("New Password", type="password")
            if st.button("Create Account"):
                if new_id:
                    st.session_state.user_db[new_id] = new_pw
                    st.success("Account Created!")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# [화면 2] 메인 앱 (디자인 적용)
# ==========================================
else:
    # 상단 헤더 (앱 느낌)
    c1, c2 = st.columns([5, 1])
    with c1: st.markdown(f"### Hello, {st.session_state.user_name}")
    with c2: 
        if st.button("Exit"): 
            st.session_state.logged_in = False
            st.rerun()

    # [A] 사용자 화면: 캘린더 + 상세 주문
    if st.session_state.user_role == "user":
        
        # 1. 메인 배너 (오늘의 메뉴)
        today = datetime.now().day
        today_menu = st.session_state.menu_db[today]
        
        st.markdown(f"<div class='sub-text'>Today's Lunch</div>", unsafe_allow_html=True)
        st.markdown(f"<h2>{today_menu['name']}</h2>", unsafe_allow_html=True)
        st.image(today_menu['img'], use_container_width=True)
        
        st.markdown("---")
        
        # 2. 캘린더 뷰 (디자인의 달력 부분 구현)
        st.markdown("### 📅 February 2026")
        
        # 달력 그리기 (7열 그리드)
        cal = calendar.monthcalendar(2026, 2)
        days_header = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        
        # 요일 헤더
        cols = st.columns(7)
        for idx, day in enumerate(days_header):
            cols[idx].markdown(f"<div style='text-align:center; font-size:0.7rem; color:#888;'>{day}</div>", unsafe_allow_html=True)
            
        # 날짜 버튼
        for week in cal:
            cols = st.columns(7)
            for idx, day in enumerate(week):
                with cols[idx]:
                    if day != 0:
                        # 선택된 날짜는 파란색, 아니면 회색
                        btn_color = "primary" if day == st.session_state.selected_date else "secondary"
                        if st.button(f"{day}", key=f"d_{day}", type=btn_color):
                            st.session_state.selected_date = day
                            st.rerun()
        
        st.markdown("---")
        
        # 3. 선택한 날짜의 상세 메뉴 (하단 시트 느낌)
        sel_day = st.session_state.selected_date
        sel_menu = st.session_state.menu_db.get(sel_day, today_menu)
        
        st.markdown(f"<div class='menu-card'>", unsafe_allow_html=True)
        st.markdown(f"<span class='highlight'>{sel_day}일 메뉴</span>", unsafe_allow_html=True)
        st.markdown(f"<h3>{sel_menu['name']}</h3>", unsafe_allow_html=True)
        
        c_img, c_info = st.columns([1, 1.5])
        with c_img:
            st.image(sel_menu['img'], use_container_width=True)
        with c_info:
            st.markdown(f"""
            <div style='margin-left:10px;'>
                <p>🔥 {sel_menu['kcal']} kcal</p>
                <p>💰 {sel_menu['price']:,} KRW</p>
                <p style='color:#888; font-size:0.8rem;'>Fresh ingredients, <br>Daily cooked.</p>
            </div>
            """, unsafe_allow_html=True)
            
        # 주문 옵션
        qty = st.number_input("Quantity", 1, 10, 1)
        bld = st.selectbox("Office Location", ["Smart Bay", "O-Biz Tower", "Techno Valley"])
        
        if st.button("ADD TO CART & PAY"):
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

    # [B] 관리자 화면: 어두운 대시보드 (디자인의 Team Lunch Order 화면 구현)
    elif st.session_state.user_role == "admin":
        st.markdown("### 📊 Admin Dashboard")
        
        df = st.session_state.orders
        
        # 카드형 통계 (어두운 배경)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='menu-card' style='text-align:center;'>", unsafe_allow_html=True)
            total_sales = df['Total'].sum() if not df.empty else 0
            st.metric("Total Sales", f"{total_sales:,}")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='menu-card' style='text-align:center;'>", unsafe_allow_html=True)
            total_qty = df['Qty'].sum() if not df.empty else 0
            st.metric("Total Orders", f"{total_qty} Box")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 차트 (파란색 바 차트)
        st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
        st.markdown("#### Monthly Intake Stats")
        if not df.empty:
            chart_data = df.groupby('Date')['Total'].sum()
            st.bar_chart(chart_data, color="#2979FF") # 파란색 차트
        else:
            st.info("No orders yet.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 주문 리스트
        st.markdown("#### Recent Orders")
        st.dataframe(df, use_container_width=True)
