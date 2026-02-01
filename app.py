import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10 Premium", layout="centered")

# 2. [디자인] 초강력 압축 CSS (간격 0, 최소너비 0)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* [핵심 1] 컬럼 사이 간격(Gap) 완전 제거 */
    div[data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }

    /* [핵심 2] 컬럼 강제 축소 (최소 너비 0 설정 -> 이게 있어야 폰에서 가로로 나옴) */
    div[data-testid="column"] {
        flex: 1 1 0px !important; /* 공간을 1/n로 공평하게 나눔 */
        min-width: 0px !important; /* ★제일 중요: 내용물이 커도 강제로 줄임 */
        padding: 1px !important;   /* 좌우 여백 1px만 남김 */
        margin: 0px !important;
    }

    /* 버튼 스타일 (작고 단단하게) */
    div.stButton > button {
        background-color: #2C2C2C;
        border: 1px solid #333;
        color: #E0E0E0;
        border-radius: 4px;
        width: 100%;
        height: 55px !important;
        padding: 0px !important;    /* 내부 여백 제거 */
        font-size: 11px !important; /* 글씨 작게 */
        white-space: pre-wrap !important; /* 줄바꿈 허용 */
        line-height: 1.2 !important;
    }
    div.stButton > button:hover { border-color: #2979FF; color: #2979FF; }
    
    /* 기타 디자인 */
    h1, h2, h3, h4 { color: #FFFFFF !important; }
    .menu-card { background-color: #1E1E1E; border-radius: 15px; padding: 15px; margin-bottom: 15px; border: 1px solid #333; }
    .highlight { color: #2979FF; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 초기화
if 'menu_db' not in st.session_state:
    st.session_state.menu_db = {
        1: {"name": "직화제육", "full_name": "직화 제육 정식", "img": "https://images.unsplash.com/photo-1626071466175-79aba923853e?w=400", "kcal": "650", "price": 7500},
        2: {"name": "연어포케", "full_name": "생연어 포케볼", "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400", "kcal": "480", "price": 8500},
        3: {"name": "스테이크", "full_name": "큐브 스테이크 덮밥", "img": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=400", "kcal": "720", "price": 9000},
        4: {"name": "닭가슴살", "full_name": "수비드 닭가슴살", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", "kcal": "350", "price": 7000},
        5: {"name": "안동찜닭", "full_name": "매콤 안동찜닭", "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=400", "kcal": "600", "price": 7500},
    }
    for i in range(6, 32):
        if i % 2 == 0: st.session_state.menu_db[i] = {"name": "셰프특선", "full_name": "오늘의 셰프 특선", "img": "https://images.unsplash.com/photo-1544124499-58912cbddaad?w=400", "kcal": "500", "price": 7500}
        else: st.session_state.menu_db[i] = {"name": "주말특식", "full_name": "주말 스페셜 브런치", "img": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=400", "kcal": "900", "price": 8900}

if 'user_db' not in st.session_state: st.session_state.user_db = {"admin": "1234", "user": "1234"}
if 'orders' not in st.session_state: st.session_state.orders = pd.DataFrame()
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().day
if 'page' not in st.session_state: st.session_state.page = "calendar"

def get_day_kor(year, month, day):
    return ["월", "화", "수", "목", "금", "토", "일"][calendar.weekday(year, month, day)]

# ==========================================
# [화면 1] 로그인
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2979FF; font-size: 3rem;'>12:10</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>직장인을 위한 점심 구독</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
        id_in = st.text_input("아이디", key="login_id")
        pw_in = st.text_input("비밀번호", type="password", key="login_pw")
        if st.button("로그인", type="primary", use_container_width=True):
            if id_in in st.session_state.user_db and st.session_state.user_db[id_in] == pw_in:
                st.session_state.logged_in = True
                st.session_state.user_name = id_in
                st.session_state.user_role = "admin" if id_in == "admin" else "user"
                st.rerun()
            else: st.error("정보를 확인해주세요.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# [화면 2] 메인 앱
# ==========================================
else:
    with st.sidebar:
        st.write(f"👋 **{st.session_state.user_name}**님")
        if st.button("로그아웃"): 
            st.session_state.logged_in = False
            st.rerun()

    if st.session_state.user_role == "user":
        if st.session_state.page == "calendar":
            st.markdown("<h3 style='text-align:center;'>2026년 2월</h3>", unsafe_allow_html=True)
            
            # 헤더: 월화수목금 (5칸 가로 정렬)
            days = ['월', '화', '수', '목', '금']
            cols = st.columns(5)
            for i, d in enumerate(days):
                cols[i].markdown(f"<div style='text-align:center; font-size:12px; color:#888;'>{d}</div>", unsafe_allow_html=True)
            
            cal = calendar.monthcalendar(2026, 2)
            
            for week in cal:
                # 1. 평일 (월~금) -> 5칸 강제 압축
                cols = st.columns(5)
                for i in range(5):
                    day = week[i]
                    with cols[i]:
                        if day != 0:
                            info = st.session_state.menu_db.get(day, {"name": ""})
                            day_str = get_day_kor(2026, 2, day)
                            # 버튼 내용: 날짜(요일) + 줄바꿈 + 메뉴명
                            btn_text = f"{day}({day_str})\n{info['name']}"
                            if st.button(btn_text, key=f"d_{day}"):
                                st.session_state.selected_date = day
                                st.session_state.page = "detail"
                                st.rerun()
                        else:
                            # 빈 공간도 칸 차지
                            st.write("")
