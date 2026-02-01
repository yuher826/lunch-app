import streamlit as st
import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10 Premium", layout="centered")

# 2. [디자인] 5칸 기준 + 줄바꿈 최적화 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    /* 전체 배경: 딥 블랙 */
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* [핵심] 5등분 기준 (20% 너비) */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        width: 20% !important; 
        flex: 1 1 20% !important;
        min-width: 0px !important;
        padding: 0px 1px !important;
    }

    /* 입력창 스타일 */
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput > div > div > input {
        color: white; background-color: #2C2C2C; border: none;
    }
    
    /* 날짜 버튼 디자인 (넓고 시원하게) */
    div.stButton > button {
        background-color: #2C2C2C;
        border: 1px solid #333;
        color: #E0E0E0;
        border-radius: 8px;
        width: 100%;
        padding: 2px 0px !important;
        font-size: 0.75rem !important;
        height: 60px !important;
        white-space: pre-wrap !important;
        line-height: 1.3 !important;
        margin-bottom: 4px !important;
    }
    div.stButton > button:hover { border-color: #2979FF; color: #2979FF; }
    
    /* 주요 버튼 */
    .primary-btn { background-color: #2979FF !important; color: white !important; font-weight: 800 !important; }
    
    /* 카드 디자인 */
    .menu-card {
        background-color: #1E1E1E; border-radius: 15px; padding: 15px;
        margin-bottom: 15px; border: 1px solid #333;
    }
    
    /* 텍스트 컬러 */
    h1, h2, h3, h4 { color: #FFFFFF !important; }
    p, span, div, label { color: #E0E0E0; }
    .highlight { color: #2979FF; font-weight: bold; }
    
    /* 주말 구분선 */
    .weekend-divider { border-top: 1px dashed #333; margin: 5px 0; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 5px; }
    .stTabs [data-baseweb="tab"] { background-color: #1E1E1E; border-radius: 8px; color: white; font-size: 0.8rem; }
    .stTabs [aria-selected="true"] { background-color: #2979FF !important; color: white !important; }
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
        if i % 2 == 0:
             st.session_state.menu_db[i] = {"name": "셰프특선", "full_name": "오늘의 셰프 특선", "img": "https://images.unsplash.com/photo-1544124499-58912cbddaad?w=400", "kcal": "500", "price": 7500}
        else:
             st.session_state.menu_db[i] = {"name": "주말특식", "full_name": "주말 스페셜 브런치", "img": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=400", "kcal": "900", "price": 8900}

if 'user_db' not in st.session_state: st.session_state.user_db = {"admin": "1234", "user": "1234"}
if 'orders' not in st.session_state: st.session_state.orders = pd.DataFrame()
if 'purchases' not in st.session_state: st.session_state.purchases = pd.DataFrame()
if 'history_df' not in st.session_state: 
    dates = pd.date_range(end=datetime.now(), periods=30)
    history_data = [{'날짜': d.strftime("%Y-%m-%d"), '총매출': np.random.randint(20,100)*7500, '총매입(원가)': np.random.randint(20,100)*4000} for d in dates]
    st.session_state.history_df = pd.DataFrame(history_data)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().day
if 'page' not in st.session_state: st.session_state.page = "calendar"

# ==========================================
# [화면 1] 로그인
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2979FF; font-size: 3rem;'>12:10</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>직장인을 위한 점심 구독</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["로그인", "회원가입"])
        with tab1:
            id_in = st.text_input("아이디", key="login_id")
            pw_in = st.text_input("비밀번호", type="password", key="login_pw")
            if st.button("로그인", type="primary", use_container_width=True):
                if id_in in st.session_state.user_db and st.session_state.user_db[id_in] == pw_in:
                    st.session_state.logged_in = True
                    st.session_state.user_name = id_in
                    st.session_state.user_role = "admin" if id_in == "admin" else "user"
                    st.rerun()
                else: st.error("아이디/비번 확인")
        with tab2:
            new_id = st.text_input("새 아이디")
            new_pw = st.text_input("새 비밀번호", type="password")
