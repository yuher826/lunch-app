import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10 Premium", layout="centered")

# 2. [디자인] 모바일 강제 7등분 고정 CSS (초강력 버전)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* [핵심 1] 모바일에서도 가로 정렬 강제 유지 (줄바꿈 금지) */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 절대 줄바꿈 하지 마! */
        gap: 1px !important;
        overflow-x: hidden !important;
    }

    /* [핵심 2] 컬럼 너비 14.28% (1/7) 강제 고정 */
    div[data-testid="column"] {
        flex: 1 1 14.28% !important;
        width: 14.28% !important;
        min-width: 0px !important; /* 내용이 커도 강제로 줄임 */
        padding: 0px !important;
        margin: 0px !important;
    }

    /* [핵심 3] 모바일용 초소형 버튼 스타일 */
    div.stButton > button {
        background-color: #2C2C2C;
        border: 1px solid #333;
        color: #E0E0E0;
        border-radius: 4px;
        width: 100%;
        height: 50px !important;     /* 높이 고정 */
        padding: 0px !important;     /* 여백 삭제 */
        font-size: 9px !important;   /* 글씨 아주 작게 */
        white-space: pre-wrap !important; /* 줄바꿈 허용 */
        line-height: 1.1 !important;
        margin: 0px !important;
    }
    div.stButton > button:hover { border-color: #2979FF; color: #2979FF; }

    /* 요일 헤더 스타일 */
    .day-header {
        font-size: 10px;
        text-align: center;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .sun { color: #FF5252; } /* 일요일 빨강 */
    .sat { color: #448AFF; } /* 토요일 파랑 */
    .wday { color: #AAAAAA; } /* 평일 회색 */

    /* 카드 및 기타 */
    .menu-card { background-color: #1E1E1E; border-radius: 15px; padding: 15px; margin-bottom: 15px; border: 1px solid #333; }
    .highlight { color: #2979FF; font-weight: bold; }
    h1, h2, h3 { color: white !important; }
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
        id_in = st.text_input("아이디", key="login_id")
        pw_in = st.text_input("비밀번호", type="password", key="login_pw")
        if st.button("로그인", type="primary", use_container_width=True):
            if id_in in st.session_state.user_db and st.session_state.user_db[id_in] == pw_in:
                st.session_state.logged_in = True
                st.session_state.user_name = id_in
                st.session_state.user_role = "admin" if id_in == "admin" else "user"
                st.rerun()
            else: st.error("정보 불일치")
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
    # [A] 사용자: 가로 7칸 강제 고정 달력
    # ----------------------------------
    if st.session_state.user_role == "user":
        
        if st.session_state.page == "calendar":
            st.markdown("<h3 style='text-align:center;'>2026년 2월</h3>", unsafe_allow_html=True)
            
            # [헤더] 일~토 (7칸)
            # st.columns(7)을 쓰면 Streamlit이 모바일에서 세로로 바꾸려고 하겠지만,
            # 위에서 정의한 CSS(flex-wrap: nowrap)가 그걸 막아서 가로로 나옵니다.
            cols = st.columns(7)
            days_labels = [('일', 'sun'), ('월', 'wday'), ('화', 'wday'), ('수', 'wday'), ('목', 'wday'), ('금', 'wday'), ('토', 'sat')]
            
            for i, (day_text, css_cls) in enumerate(days_labels):
                cols[i].markdown(f"<div class='day-header {css_cls}'>{day_text}</div>", unsafe_allow_html=True)
            
            # 달력 날짜 생성 (일요일 시작)
            cal = calendar.Calendar(firstweekday=6)
            month_days = cal.monthdayscalendar(2026, 2)
            
            for week in month_days:
                cols = st.columns(7) # 7칸 생성
                for i, day in enumerate(week):
                    with cols[i]:
                        if day != 0:
                            info = st.session_state.menu_db.get(day, {"name": ""})
                            # 버튼 내용: 날짜 + 줄바꿈 + 메뉴명 (짧게)
                            # 모바일에서는 글씨가 9px로 나옵니다.
                            btn_text = f"{day}\n{info['name']}"
                            
                            if st.button(btn_text, key=f"d_{day}"):
                                st.session_state.selected_date = day
                                st.session_state.page = "detail"
                                st.rerun()
                        else:
                            # 빈 칸은 투명 버튼으로 자리만 차지
                            st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
                
                # 주(Week) 간격
                st.write("")

        # 상세 페이지 (기존 유지)
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
            with c1: st.markdown(f"🔥 **{menu['kcal']}**")
            with c2: st.markdown(f"💰 **{menu['price']:,}원**")
            
            with st.form("order"):
                qty = st.number_input("수량", 1, 10, 1)
                loc = st.selectbox("수령장소", ["스마트베이", "오비즈", "동일"])
                if st.form_submit_button("주문하기", type="primary", use_container_width=True):
                    new_ord = {'날짜': f"2026-02-{sel_day}", '고객명': st.session_state.user_name, '메뉴': menu['full_name'], '수량': qty, '합계': qty*menu['price'], '거점': loc}
                    st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_ord])], ignore_index=True)
                    st.success("주문 완료!")
            st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------
    # [B] 관리자 모드
    # ----------------------------------
    elif st.session_state.user_role == "admin":
        st.markdown("### 📊 관리자 모드")
        df_ord = st.session_state.orders
        t1, t2, t3, t4 = st.tabs(["대시보드", "주문현황", "지출관리", "보고서"])
        
        with t1:
            sales = df_ord['합계'].sum() if not df_ord.empty else 0
            st.metric("총 매출", f"{sales:,}원")
        with t2:
            st.dataframe(df_ord, use_container_width=True)
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
