import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10 Premium", layout="centered")

# 2. [디자인] 구글/삼성 캘린더 위젯 스타일 (여백 완전 제거)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* [핵심 1] 가로 줄바꿈 금지 & 간격(Gap) 완전 삭제 */
    div[data-testid="stHorizontalBlock"] {
        gap: 0px !important;
        padding: 0px !important;
    }

    /* [핵심 2] 컬럼 너비 14.28% 강제 & 내부 여백(Padding) 삭제 */
    /* 이게 없어서 아까 띄엄띄엄 나온 겁니다 */
    div[data-testid="column"] {
        flex: 0 0 14.28% !important; /* 100% / 7 = 14.28% */
        width: 14.28% !important;
        min-width: 0px !important;
        padding: 0px !important; /* 옆구리 살 제거 */
        margin: 0px !important;
    }

    /* [핵심 3] 버튼 스타일: 위젯처럼 동그랗고 깔끔하게 */
    div.stButton > button {
        background-color: transparent; /* 배경 투명 (위젯 느낌) */
        border: none;
        color: #E0E0E0;
        border-radius: 50%; /* 원형 */
        width: 100%;
        aspect-ratio: 1 / 1; /* 정사각형 비율 유지 */
        padding: 0px !important;
        font-size: 14px !important;
        font-weight: 500;
        margin: 0px !important;
    }
    
    /* 선택된 날짜 & 호버 효과 */
    div.stButton > button:hover { background-color: #333; color: #2979FF; }
    div.stButton > button:active { background-color: #2979FF; color: white; }
    div.stButton > button:focus { box-shadow: none; border: 1px solid #2979FF; }

    /* 요일 헤더 */
    .day-header { text-align: center; font-size: 12px; margin-bottom: 5px; color: #888; }
    .sun { color: #FF5252 !important; }
    .sat { color: #448AFF !important; }

    /* 하단 상세 카드 (메뉴판) */
    .detail-card {
        background-color: #1E1E1E;
        border-radius: 20px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid #333;
    }
    
    .highlight { color: #2979FF; font-weight: bold; }
    .big-btn > button {
        background-color: #2979FF !important;
        color: white !important;
        border-radius: 8px !important;
        height: 50px !important;
        aspect-ratio: auto !important; /* 길쭉하게 복구 */
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 초기화
if 'menu_db' not in st.session_state:
    st.session_state.menu_db = {
        1: {"name": "직화 제육 정식", "img": "https://images.unsplash.com/photo-1626071466175-79aba923853e?w=400", "kcal": "650", "price": 7500},
        2: {"name": "생연어 포케볼", "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400", "kcal": "480", "price": 8500},
        3: {"name": "큐브 스테이크 덮밥", "img": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=400", "kcal": "720", "price": 9000},
        4: {"name": "수비드 닭가슴살", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", "kcal": "350", "price": 7000},
        5: {"name": "매콤 안동찜닭", "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=400", "kcal": "600", "price": 7500},
    }
    for i in range(6, 32):
        if i % 2 == 0: st.session_state.menu_db[i] = {"name": "오늘의 셰프 특선", "img": "https://images.unsplash.com/photo-1544124499-58912cbddaad?w=400", "kcal": "500", "price": 7500}
        else: st.session_state.menu_db[i] = {"name": "주말 스페셜 브런치", "img": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=400", "kcal": "900", "price": 8900}

if 'user_db' not in st.session_state: st.session_state.user_db = {"admin": "1234", "user": "1234"}
if 'orders' not in st.session_state: st.session_state.orders = pd.DataFrame()
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().day
if 'view_mode' not in st.session_state: st.session_state.view_mode = "calendar"

# ==========================================
# [화면 1] 로그인
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2979FF; font-size: 3rem;'>12:10</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='detail-card' style='text-align:center;'>", unsafe_allow_html=True)
        id_in = st.text_input("아이디", key="login_id")
        pw_in = st.text_input("비밀번호", type="password", key="login_pw")
        st.markdown('<div class="big-btn">', unsafe_allow_html=True)
        if st.button("로그인", type="primary", use_container_width=True):
            if id_in in st.session_state.user_db and st.session_state.user_db[id_in] == pw_in:
                st.session_state.logged_in = True
                st.session_state.user_name = id_in
                st.session_state.user_role = "admin" if id_in == "admin" else "user"
                st.rerun()
            else: st.error("정보 불일치")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# [화면 2] 메인 앱 (구글 캘린더 스타일)
# ==========================================
else:
    with st.sidebar:
        st.write(f"👋 **{st.session_state.user_name}**님")
        if st.button("로그아웃"): 
            st.session_state.logged_in = False
            st.rerun()

    if st.session_state.user_role == "user":
        
        # [모드 1] 달력 위젯 화면
        if st.session_state.view_mode == "calendar":
            c1, c2 = st.columns([4,1])
            with c1: st.markdown(f"### 📅 2026년 2월")
            with c2: 
                if st.button("나가기"): 
                    st.session_state.logged_in = False
                    st.rerun()
            
            st.markdown("---")
            
            # 요일 헤더 (일~토)
            cols = st.columns(7)
            days = ['일', '월', '화', '수', '목', '금', '토']
            classes = ['sun', '', '', '', '', '', 'sat']
            for i, (d, c) in enumerate(zip(days, classes)):
                cols[i].markdown(f"<div class='day-header {c}'>{d}</div>", unsafe_allow_html=True)
            
            # 달력 본체 (여백 0으로 딱 붙임)
            cal = calendar.Calendar(firstweekday=6)
            month_days = cal.monthdayscalendar(2026, 2)
            
            for week in month_days:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    with cols[i]:
                        if day != 0:
                            # 오늘 날짜나 선택된 날짜 표시 로직
                            btn_label = f"{day}"
                            # 클릭 시 상세화면으로 이동
                            if st.button(btn_label, key=f"d_{day}"):
                                st.session_state.selected_date = day
                                st.session_state.view_mode = "detail"
                                st.rerun()
                        else:
                            st.write("") # 빈 칸
            
            st.markdown("<br><p style='text-align:center; color:#666; font-size:12px;'>날짜를 누르면 메뉴를 볼 수 있습니다.</p>", unsafe_allow_html=True)

        # [모드 2] 상세 주문 화면
        elif st.session_state.view_mode == "detail":
            sel_day = st.session_state.selected_date
            menu = st.session_state.menu_db.get(sel_day)
            
            st.markdown('<div class="big-btn">', unsafe_allow_html=True)
            if st.button("← 달력으로 돌아가기"):
                st.session_state.view_mode = "calendar"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='detail-card'>
                <p style='color:#2979FF; margin-bottom:5px;'>2월 {sel_day}일의 점심</p>
                <h2 style='margin-top:0;'>{menu['name']}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.image(menu['img'], use_container_width=True)
            
            c1, c2 = st.columns(2)
            with c1: st.metric("칼로리", f"{menu['kcal']} kcal")
            with c2: st.metric("가격", f"{menu['price']:,} 원")
            
            with st.form("order_form"):
                qty = st.number_input("수량", 1, 10, 1)
                loc = st.selectbox("수령 장소", ["스마트베이", "오비즈타워", "동일테크노"])
                
                st.markdown('<div class="big-btn">', unsafe_allow_html=True)
                if st.form_submit_button("장바구니 담기 & 결제", type="primary", use_container_width=True):
                    new_ord = {'날짜': f"2026-02-{sel_day}", '고객명': st.session_state.user_name, '메뉴': menu['name'], '수량': qty, '합계': qty*menu['price'], '거점': loc}
                    st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_ord])], ignore_index=True)
                    st.success("주문이 완료되었습니다!")
                st.markdown('</div>', unsafe_allow_html=True)

    # 관리자 모드
    elif st.session_state.user_role == "admin":
        st.markdown("### 📊 관리자 모드")
        df_ord = st.session_state.orders
        t1, t2 = st.tabs(["주문현황", "매출통계"])
        with t1: st.dataframe(df_ord, use_container_width=True)
        with t2: 
            if not df_ord.empty: st.bar_chart(df_ord.groupby('날짜')['합계'].sum())
            else: st.info("데이터 없음")
