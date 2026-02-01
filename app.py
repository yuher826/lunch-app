import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10 Premium", layout="centered")

# 2. [디자인] 달력 전용 CSS (충돌 방지 안전 버전)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    /* 전체 배경: 딥 블랙 */
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* [핵심] 달력 5등분 강제 고정 */
    /* 화면 깨짐 방지를 위해 상단 헤더는 사이드바로 뺐습니다 */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        width: 20% !important; /* 무조건 5등분 (모바일 줄바꿈 방지) */
        flex: 1 1 20% !important;
        min-width: 0px !important;
        padding: 0px 1px !important;
    }

    /* 입력창 스타일 */
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput > div > div > input {
        color: white; background-color: #2C2C2C; border: none;
    }
    
    /* 날짜 버튼 디자인 */
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
    
    /* 탭 스타일 */
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
            if st.button("가입하기", use_container_width=True):
                if new_id:
                    st.session_state.user_db[new_id] = new_pw
                    st.success("가입 완료!")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# [화면 2] 메인 앱
# ==========================================
else:
    # [중요] 상단 헤더를 왼쪽 사이드바로 이동 (화면 깨짐 방지)
    with st.sidebar:
        st.write(f"👋 **{st.session_state.user_name}**님")
        if st.button("로그아웃", key="logout"): 
            st.session_state.logged_in = False
            st.rerun()

    # ----------------------------------
    # [A] 사용자: 5+2 배열 달력 (오타 수정 완료)
    # ----------------------------------
    if st.session_state.user_role == "user":
        
        if st.session_state.page == "calendar":
            st.markdown("<h3 style='text-align:center;'>📅 2026년 2월</h3>", unsafe_allow_html=True)
            
            # 헤더: 월화수목금 (5칸)
            days = ['월', '화', '수', '목', '금']
            cols = st.columns(5)
            for i, d in enumerate(days):
                cols[i].markdown(f"<div style='text-align:center; font-size:0.8rem; color:#888;'>{d}</div>", unsafe_allow_html=True)
            
            cal = calendar.monthcalendar(2026, 2)
            
            # 주(Week) 단위 루프
            for week_idx, week in enumerate(cal):
                
                # 1. 평일 (월~금) -> 윗줄
                cols = st.columns(5)
                for i in range(5):
                    day = week[i]
                    with cols[i]:
                        if day != 0:
                            info = st.session_state.menu_db.get(day, {"name": ""})
                            if st.button(f"{day}\n{info['name']}", key=f"d_{day}"):
                                st.session_state.selected_date = day
                                st.session_state.page = "detail"
                                st.rerun()
                        else:
                            st.write("")
                
                # 2. 주말 (토~일) -> 아랫줄
                if week[5] != 0 or week[6] != 0:
                    cols_weekend = st.columns(5) # 5칸 그리드 유지
                    
                    # 토요일
                    with cols_weekend[0]:
                        day = week[5]
                        if day != 0:
                            info = st.session_state.menu_db.get(day, {"name": ""})
                            if st.button(f"{day} (토)\n{info['name']}", key=f"d_{day}"):
                                st.session_state.selected_date = day
                                st.session_state.page = "detail"
                                st.rerun()
                    
                    # 일요일
                    with cols_weekend[1]:
                        day = week[6]
                        if day != 0:
                            info = st.session_state.menu_db.get(day, {"name": ""})
                            if st.button(f"{day} (일)\n{info['name']}", key=f"d_{day}"):
                                st.session_state.selected_date = day
                                st.session_state.page = "detail"
                                st.rerun()
                
                st.markdown("<hr style='margin: 5px 0; border-top: 1px solid #333;'>", unsafe_allow_html=True)

            st.markdown("<br><div style='text-align:center; color:#666; font-size:0.8rem;'>평일(윗줄) / 주말(아랫줄)</div>", unsafe_allow_html=True)

        # 상세 페이지
        elif st.session_state.page == "detail":
            sel_day = st.session_state.selected_date
            menu = st.session_state.menu_db.get(sel_day)
            
            if st.button("← 달력으로 돌아가기"):
                st.session_state.page = "calendar"
                st.rerun()
                
            st.markdown(f"<div class='menu-card'>", unsafe_allow_html=True)
            st.markdown(f"<span class='highlight'>{sel_day}일</span>의 메뉴", unsafe_allow_html=True)
            st.markdown(f"<h3>{menu['full_name']}</h3>", unsafe_allow_html=True)
            
            st.image(menu['img'], use_container_width=True)
            
            c1, c2 = st.columns(2)
            with c1: st.markdown(f"🔥 **{menu['kcal']}** kcal")
            with c2: st.markdown(f"💰 **{menu['price']:,}** 원")
            
            st.markdown("---")
            
            with st.form("order"):
                qty = st.number_input("수량", 1, 10, 1)
                loc = st.selectbox("받으실 곳", ["평촌 스마트베이", "오비즈타워", "동일테크노"])
                
                if st.form_submit_button("장바구니 담기 & 결제", type="primary", use_container_width=True):
                    # [에러 발생했던 지점 수정 완료]
                    new_ord = {
                        '날짜': f"2026-02-{sel_day}",
                        '고객명': st.session_state.user_name,
                        '메뉴': menu['full_name'],
                        '수량': qty,
                        '합계': qty * menu['price'],
                        '거점': loc
                    }
                    st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_ord])], ignore_index=True)
                    st.success("주문이 완료되었습니다!")
            st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------
    # [B] 관리자 화면
    # ----------------------------------
    elif st.session_state.user_role == "admin":
        st.markdown("### 📊 관리자 대시보드")
        df_ord = st.session_state.orders
        t1, t2, t3, t4 = st.tabs(["대시보드", "주문현황", "지출관리", "보고서"])
        
        with t1:
            c1, c2 = st.columns(2)
            sales = df_ord['합계'].sum() if not df_ord.empty else 0
            qty = df_ord['수량'].sum() if not df_ord.empty else 0
            with c1:
                st.markdown("<div class='menu-card' style='text-align:center;'>", unsafe_allow_html=True)
                st.metric("총 매출", f"{sales:,}")
                st.markdown("</div>", unsafe_allow_html=True)
            with c2:
                st.markdown("<div class='menu-card' style='text-align:center;'>", unsafe_allow_html=True)
                st.metric("총 주문", f"{qty}개")
                st.markdown("</div>", unsafe_allow_html=True)

        with t2:
            st.dataframe(df_ord, use_container_width=True)
            if not df_ord.empty:
                hm = pd.pivot_table(df_ord, values='수량', index='메뉴', columns='거점', aggfunc='sum', fill_value=0)
                st.dataframe(hm.style.background_gradient(cmap='Blues'), use_container_width=True)

        with t3:
            with st.form("buy"):
                i_name = st.text_input("내용")
                i_cost = st.number_input("금액", step=1000)
                if st.form_submit_button("등록"):
                    new_p = {'날짜': datetime.now().strftime("%Y-%m-%d"), '항목': i_name, '금액': i_cost}
                    st.session_state.purchases = pd.concat([st.session_state.purchases, pd.DataFrame([new_p])], ignore_index=True)
                    st.success("저장됨")
            st.dataframe(st.session_state.purchases, use_container_width=True)

        with t4:
            st.line_chart(st.session_state.history_df.set_index('날짜')[['총매출', '총매입(원가)']])
