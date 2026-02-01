import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10 Premium", layout="centered")

# 2. [디자인] 4칸 전용 강제 고정 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* [핵심] 모바일에서 컬럼 세로 풀림 방지 (4등분 = 25%) */
    @media (max-width: 768px) {
        div[data-testid="column"] {
            flex: 0 0 25% !important; /* 4칸이니까 25% */
            width: 25% !important;
            min-width: 0px !important;
            padding: 2px !important;
        }
    }

    /* PC에서도 4등분 */
    div[data-testid="column"] {
        flex: 0 0 25% !important;
        width: 25% !important;
        min-width: 0px !important;
    }

    /* 버튼 스타일 */
    div.stButton > button {
        background-color: #2C2C2C;
        border: 1px solid #333;
        color: #E0E0E0;
        border-radius: 6px;
        width: 100%;
        height: 60px !important;
        padding: 0px !important;
        font-size: 12px !important; /* 글씨 크기 적당하게 */
        white-space: pre-wrap;
        line-height: 1.3;
    }
    div.stButton > button:hover { border-color: #2979FF; color: #2979FF; }
    
    /* 카드 및 텍스트 */
    .menu-card { background-color: #1E1E1E; border-radius: 15px; padding: 15px; margin-bottom: 15px; border: 1px solid #333; }
    h1, h2, h3, h4 { color: #FFFFFF !important; }
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

# 요일 계산 함수 (월, 화, 수...)
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

    # ----------------------------------
    # [A] 사용자: 4칸 바둑판 달력 (가장 안전한 방식)
    # ----------------------------------
    if st.session_state.user_role == "user":
        
        if st.session_state.page == "calendar":
            st.markdown("<h3 style='text-align:center;'>2026년 2월</h3>", unsafe_allow_html=True)
            
            # 2월 1일 ~ 28일까지 날짜 리스트 생성
            days_in_month = range(1, 29)
            
            # 4개씩 끊어서 배치 (Chunking)
            for i in range(0, len(days_in_month), 4):
                cols = st.columns(4) # 무조건 4칸
                
                # 현재 줄에 들어갈 4개의 날짜 가져오기
                current_days = days_in_month[i : i+4]
                
                for idx, day in enumerate(current_days):
                    with cols[idx]:
                        info = st.session_state.menu_db.get(day, {"name": ""})
                        day_str = get_day_kor(2026, 2, day) # 요일 구하기
                        
                        # 버튼 텍스트: "1 (일) \n 메뉴이름"
                        btn_text = f"{day} ({day_str})\n{info['name']}"
                        
                        if st.button(btn_text, key=f"d_{day}"):
                            st.session_state.selected_date = day
                            st.session_state.page = "detail"
                            st.rerun()
                
                # 줄바꿈 간격 살짝
                st.write("")

        # 상세 페이지 (기존 유지)
        elif st.session_state.page == "detail":
            sel_day = st.session_state.selected_date
            menu = st.session_state.menu_db.get(sel_day)
            day_str = get_day_kor(2026, 2, sel_day)
            
            if st.button("← 뒤로가기"):
                st.session_state.page = "calendar"
                st.rerun()
                
            st.markdown(f"<div class='menu-card'>", unsafe_allow_html=True)
            st.markdown(f"<span class='highlight'>{sel_day}일 ({day_str})</span>의 메뉴", unsafe_allow_html=True)
            st.markdown(f"<h3>{menu['full_name']}</h3>", unsafe_allow_html=True)
            st.image(menu['img'], use_container_width=True)
            
            c1, c2 = st.columns(2)
            with c1: st.markdown(f"🔥 **{menu['kcal']}**")
            with c2: st.markdown(f"💰 **{menu['price']:,}원**")
            
            with st.form("order"):
                qty = st.number_input("수량", 1, 10, 1)
                loc = st.selectbox("수령장소", ["스마트베이", "오비즈타워", "동일테크노"])
                if st.form_submit_button("주문하기", type="primary", use_container_width=True):
                    new_ord = {'날짜': f"2026-02-{sel_day}", '고객명': st.session_state.user_name, '메뉴': menu['full_name'], '수량': qty, '합계': qty*menu['price'], '거점': loc}
                    st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_ord])], ignore_index=True)
                    st.success("주문 완료!")
            st.markdown("</div>", unsafe_allow_html=True)

    # 관리자 모드 (기존 유지)
    elif st.session_state.user_role == "admin":
        st.markdown("### 📊 관리자 모드")
        st.dataframe(st.session_state.orders, use_container_width=True)
