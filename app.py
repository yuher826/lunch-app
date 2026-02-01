import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10 Premium", layout="centered")

# 2. [디자인] 화면 분리형 전용 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* [핵심] 달력 화면일 때만 적용되는 강제 7등분 CSS */
    div[data-testid="column"] {
        flex: 1 1 0px !important;
        min-width: 0px !important;
        padding: 1px !important;
        margin: 0px !important;
    }
    
    /* 가로 줄바꿈 금지 */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0px !important;
    }

    /* 달력 숫자 버튼 스타일 (심플 위젯 스타일) */
    div.stButton > button {
        background-color: #1E1E1E;
        border: none;
        color: #E0E0E0;
        border-radius: 50%; /* 원형 버튼 느낌 */
        width: 100%;
        aspect-ratio: 1/1; /* 정사각형 비율 유지 */
        padding: 0px !important;
        font-size: 14px !important;
        font-weight: 600;
        margin: 0px auto;
    }
    div.stButton > button:hover { background-color: #333; color: #2979FF; }
    div.stButton > button:active { background-color: #2979FF; color: white; }

    /* 뒤로가기/주문하기 버튼은 길쭉하게 */
    .big-btn > button {
        border-radius: 8px !important;
        aspect-ratio: auto !important;
        height: 50px !important;
        width: 100% !important;
    }

    /* 요일 헤더 */
    .day-header { text-align: center; font-size: 12px; margin-bottom: 10px; color: #888; }
    .sun { color: #FF5252 !important; }
    .sat { color: #448AFF !important; }

    /* 상세 페이지 카드 */
    .detail-card {
        background-color: #1E1E1E;
        border-radius: 20px;
        padding: 20px;
        margin-top: 10px;
        border: 1px solid #333;
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
if 'view_mode' not in st.session_state: st.session_state.view_mode = "calendar" # 화면 상태 (calendar / detail)

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
        st.markdown('<div class="big-btn">', unsafe_allow_html=True) # 버튼 클래스 적용
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
# [화면 2] 메인 앱
# ==========================================
else:
    # 관리자는 바로 관리자 화면으로
    if st.session_state.user_role == "admin":
        st.markdown("### 📊 관리자 모드")
        df_ord = st.session_state.orders
        t1, t2 = st.tabs(["주문현황", "매출통계"])
        with t1: st.dataframe(df_ord, use_container_width=True)
        with t2: 
            if not df_ord.empty: st.bar_chart(df_ord.groupby('날짜')['합계'].sum())
            else: st.info("데이터 없음")
            
    # 사용자 (달력 <-> 상세화면 전환)
    elif st.session_state.user_role == "user":
        
        # ------------------------------------------------
        # [모드 1] 달력 화면 (오직 달력만 보임 -> 깔끔!)
        # ------------------------------------------------
        if st.session_state.view_mode == "calendar":
            c1, c2 = st.columns([4,1])
            with c1: st.markdown(f"### 📅 2026년 2월")
            with c2: 
                if st.button("나가기"): 
                    st.session_state.logged_in = False
                    st.rerun()
            
            st.markdown("---")
            
            # 요일 헤더
            cols = st.columns(7)
            days = ['일', '월', '화', '수', '목', '금', '토']
            css_cls = ['sun', '', '', '', '', '', 'sat']
            for i, d in enumerate(days):
                cols[i].markdown(f"<div class='day-header {css_cls[i]}'>{d}</div>", unsafe_allow_html=True)
            
            # 달력 본체 (숫자만!)
            cal = calendar.Calendar(firstweekday=6)
            month_days = cal.monthdayscalendar(2026, 2)
            
            for week in month_days:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    with cols[i]:
                        if day != 0:
                            # 버튼 누르면 -> 날짜 저장 & 화면을 'detail'로 변경
                            if st.button(f"{day}", key=f"d_{day}"):
                                st.session_state.selected_date = day
                                st.session_state.view_mode = "detail" # ★화면 전환 핵심★
                                st.rerun()
                        else:
                            st.write("") # 빈 칸
            
            st.markdown("<br><p style='text-align:center; color:#666; font-size:12px;'>날짜를 누르면 메뉴를 볼 수 있습니다.</p>", unsafe_allow_html=True)

        # ------------------------------------------------
        # [모드 2] 상세 주문 화면 (달력 없음 -> 넓게 씀!)
        # ------------------------------------------------
        elif st.session_state.view_mode == "detail":
            sel_day = st.session_state.selected_date
            menu = st.session_state.menu_db.get(sel_day)
            
            # 상단: 뒤로가기 버튼
            st.markdown('<div class="big-btn">', unsafe_allow_html=True)
            if st.button("← 달력으로 돌아가기"):
                st.session_state.view_mode = "calendar" # 다시 달력으로
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 상세 내용 카드
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
            
            st.markdown("---")
            
            # 주문 폼
            with st.form("order_form"):
                qty = st.number_input("수량", 1, 10, 1)
                loc = st.selectbox("수령 장소", ["스마트베이", "오비즈타워", "동일테크노"])
                
                st.markdown('<div class="big-btn">', unsafe_allow_html=True)
                if st.form_submit_button("장바구니 담기 & 결제", type="primary", use_container_width=True):
                    new_ord = {'날짜': f"2026-02-{sel_day}", '고객명': st.session_state.user_name, '메뉴': menu['name'], '수량': qty, '합계': qty*menu['price'], '거점': loc}
                    st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_ord])], ignore_index=True)
                    st.success("주문이 완료되었습니다!")
                st.markdown('</div>', unsafe_allow_html=True)
