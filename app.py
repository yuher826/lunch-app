import streamlit as st
import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt
from datetime import datetime

# 1. 페이지 설정 (레이아웃 고정)
st.set_page_config(page_title="12:10 프리미엄", layout="centered")

# 2. [디자인] 프리미엄 다크 모드 CSS (한국어 폰트 적용)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    /* 전체 배경: 딥 블랙 */
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* 입력창 커스텀 */
    .stTextInput > div > div > input { color: white; background-color: #2C2C2C; border: none; }
    .stSelectbox > div > div > div { color: white; background-color: #2C2C2C; }
    .stNumberInput > div > div > input { color: white; background-color: #2C2C2C; }
    
    /* 버튼 스타일 (기본) */
    div.stButton > button {
        background-color: #2C2C2C;
        border: 1px solid #333;
        color: #E0E0E0;
        border-radius: 8px;
        transition: 0.3s;
        width: 100%;
        padding: 0.5rem 0; /* 버튼 높이 조절 */
    }
    div.stButton > button:hover { border-color: #2979FF; color: #2979FF; }
    div.stButton > button:focus { border-color: #2979FF; color: #2979FF; background-color: #1A237E; }
    
    /* [핵심] 달력 날짜 버튼 전용 스타일 */
    .date-btn { font-size: 0.8rem; }

    /* [강조] 메인 액션 버튼 (파란색) */
    .primary-btn {
        background-color: #2979FF !important; 
        color: white !important;
        border: none !important;
        font-weight: 800 !important;
    }
    
    /* 카드 디자인 */
    .menu-card {
        background-color: #1E1E1E;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        border: 1px solid #333;
    }
    
    /* 텍스트 컬러 */
    h1, h2, h3, h4 { color: #FFFFFF !important; }
    p, span, div, label { color: #E0E0E0; }
    .highlight { color: #2979FF; font-weight: bold; }
    .sub-text { font-size: 0.8rem; color: #888; }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1E1E1E; border-radius: 10px; color: white; border: none; }
    .stTabs [aria-selected="true"] { background-color: #2979FF !important; color: white !important; }
    
    /* 모바일 달력 강제 정렬을 위한 CSS */
    div[data-testid="column"] {
        padding: 0 2px !important; /* 좌우 여백 최소화 */
        min-width: 0 !important;
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
        st.session_state.menu_db[i] = {"name": "오늘의 셰프 특선", "img": "https://images.unsplash.com/photo-1544124499-58912cbddaad?w=400", "kcal": "500", "price": 7500}

if 'user_db' not in st.session_state: st.session_state.user_db = {"admin": "1234", "user": "1234"}
if 'orders' not in st.session_state: st.session_state.orders = pd.DataFrame()
if 'purchases' not in st.session_state: st.session_state.purchases = pd.DataFrame()
if 'history_df' not in st.session_state: 
    dates = pd.date_range(end=datetime.now(), periods=30)
    history_data = [{'날짜': d.strftime("%Y-%m-%d"), '총매출': np.random.randint(20,100)*7500, '총매입(원가)': np.random.randint(20,100)*4000} for d in dates]
    st.session_state.history_df = pd.DataFrame(history_data)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().day

# ==========================================
# [화면 1] 로그인 & 회원가입 (한글화 완료)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2979FF; font-size: 3rem;'>12:10</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>직장인을 위한 프리미엄 점심 구독</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["로그인", "회원가입"])
        
        with tab1:
            id_in = st.text_input("아이디", key="login_id")
            pw_in = st.text_input("비밀번호", type="password", key="login_pw")
            if st.button("로그인 하기", type="primary", use_container_width=True):
                if id_in in st.session_state.user_db and st.session_state.user_db[id_in] == pw_in:
                    st.session_state.logged_in = True
                    st.session_state.user_name = id_in
                    st.session_state.user_role = "admin" if id_in == "admin" else "user"
                    st.rerun()
                else: st.error("아이디 또는 비밀번호를 확인해주세요.")
        
        with tab2:
            new_id = st.text_input("새 아이디")
            new_pw = st.text_input("새 비밀번호", type="password")
            if st.button("계정 생성", use_container_width=True):
                if new_id:
                    st.session_state.user_db[new_id] = new_pw
                    st.success("회원가입이 완료되었습니다!")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# [화면 2] 메인 앱
# ==========================================
else:
    c1, c2 = st.columns([5, 1])
    with c1: st.markdown(f"### 반갑습니다, {st.session_state.user_name}님")
    with c2: 
        if st.button("나가기"): 
            st.session_state.logged_in = False
            st.rerun()

    # ----------------------------------
    # [A] 사용자 화면: 달력 + 주문 (한글 & 그리드 적용)
    # ----------------------------------
    if st.session_state.user_role == "user":
        
        # 1. 메인 배너
        today = datetime.now().day
        today_menu = st.session_state.menu_db[today]
        
        st.markdown(f"<div class='sub-text'>오늘의 추천 메뉴</div>", unsafe_allow_html=True)
        st.markdown(f"<h2>{today_menu['name']}</h2>", unsafe_allow_html=True)
        st.image(today_menu['img'], use_container_width=True)
        
        st.markdown("---")
        
        # 2. 캘린더 뷰 (7열 그리드 강제 적용)
        st.markdown("### 📅 2026년 2월 식단표")
        st.caption("날짜를 누르면 메뉴를 볼 수 있어요.")
        
        cal = calendar.monthcalendar(2026, 2)
        days_header = ['월', '화', '수', '목', '금', '토', '일']
        
        # 요일 헤더 (7칸)
        cols = st.columns(7)
        for idx, day in enumerate(days_header):
            cols[idx].markdown(f"<div style='text-align:center; font-size:0.8rem; color:#888; margin-bottom:5px;'>{day}</div>", unsafe_allow_html=True)
            
        # 날짜 버튼 (7칸 그리드 유지)
        for week in cal:
            cols = st.columns(7) # 매 주마다 새로운 7칸 열 생성
            for idx, day in enumerate(week):
                with cols[idx]:
                    if day != 0:
                        # 오늘 날짜나 선택된 날짜 강조 로직은 버튼 스타일로 대체
                        if st.button(f"{day}", key=f"d_{day}", use_container_width=True):
                            st.session_state.selected_date = day
                            st.rerun()
                    else:
                        st.write("") # 빈 칸 유지
        
        st.markdown("---")
        
        # 3. 상세 메뉴 및 주문 (한글화)
        sel_day = st.session_state.selected_date
        sel_menu = st.session_state.menu_db.get(sel_day, today_menu)
        
        st.markdown(f"<div class='menu-card'>", unsafe_allow_html=True)
        st.markdown(f"<span class='highlight'>{sel_day}일의 메뉴</span>", unsafe_allow_html=True)
        st.markdown(f"<h3>{sel_menu['name']}</h3>", unsafe_allow_html=True)
        
        c_img, c_info = st.columns([1, 1.5])
        with c_img: st.image(sel_menu['img'], use_container_width=True)
        with c_info:
            st.markdown(f"""
            <div style='margin-left:10px;'>
                <p>🔥 {sel_menu['kcal']} kcal</p>
                <p>💰 {sel_menu['price']:,}원</p>
                <p style='color:#888; font-size:0.8rem;'>신선한 재료로<br>매일 아침 조리합니다.</p>
            </div>
            """, unsafe_allow_html=True)
            
        qty = st.number_input("수량 선택", 1, 10, 1)
        bld = st.selectbox("수령 장소", ["평촌 스마트베이", "오비즈타워", "동일테크노"])
        
        # 주문 버튼 (파란색)
        if st.button("장바구니 담기 & 결제", type="primary", use_container_width=True):
            new_ord = {
                '날짜': f"2026-02-{sel_day}",
                '고객명': st.session_state.user_name,
                '메뉴': sel_menu['name'],
                '수량': qty,
                '합계': qty * sel_menu['price'],
                '거점': bld
            }
            st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_ord])], ignore_index=True)
            st.success(f"2월 {sel_day}일 주문이 완료되었습니다!")
        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------
    # [B] 관리자 화면 (한글화 & 기능 유지)
    # ----------------------------------
    elif st.session_state.user_role == "admin":
        st.markdown("### 📊 관리자 대시보드")
        
        df_ord = st.session_state.orders
        df_buy = st.session_state.purchases
        
        adm_tab1, adm_tab2, adm_tab3, adm_tab4 = st.tabs(["대시보드", "주문
