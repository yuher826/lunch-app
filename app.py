import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10 Premium", layout="centered")

# 2. [디자인] 모바일 반응형 최적화 CSS (사장님 말씀대로 폰트 줄이고 화면 맞춤)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* [핵심 기술] 화면 폭이 768px 이하(모바일)일 때만 적용되는 반응형 코드 */
    @media (max-width: 768px) {
        /* 가로 정렬 유지 (세로로 떨어지는 것 방지) */
        div[data-testid="column"] {
            flex: 1 1 13% !important; /* 7등분이니까 약 13~14% */
            width: 13% !important;
            min-width: 0px !important; /* 좁아도 허용 */
            padding: 0px 1px !important; /* 옆 간격 거의 없앰 */
            margin: 0px !important;
        }

        /* 버튼 안의 글씨 크기를 확 줄임 (화면에 맞추기 위해) */
        div.stButton > button {
            font-size: 10px !important;  /* 글씨 작게 */
            padding: 2px 0px !important; /* 버튼 안 여백 제거 */
            height: 45px !important;     /* 버튼 높이 조절 */
            line-height: 1.1 !important; /* 줄 간격 좁게 */
        }
        
        /* 요일 헤더 글씨도 작게 */
        .day-header { font-size: 10px !important; }
    }

    /* PC 화면에서는 좀 더 여유롭게 */
    @media (min-width: 769px) {
        div[data-testid="column"] {
            flex: 1 1 14.2% !important;
            width: 14.2% !important;
        }
    }

    /* 버튼 기본 스타일 (공통) */
    div.stButton > button {
        background-color: #2C2C2C;
        border: 1px solid #333;
        color: #E0E0E0;
        border-radius: 5px;
        width: 100%;
        height: 65px;
        white-space: pre-wrap; /* 줄바꿈 허용 */
        margin-bottom: 2px;
    }
    div.stButton > button:hover { border-color: #2979FF; color: #2979FF; }

    /* 요일 색상 및 스타일 */
    .sunday { color: #FF5252; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .saturday { color: #448AFF; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .weekday { color: #AAAAAA; text-align: center; margin-bottom: 5px; }
    
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
                else: st.error("정보 불일치")
        with tab2:
            st.write("회원가입 기능 (생략)")
            if st.button("가입"): st.success("가입됨")
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
            
            # 요일 헤더 (사진처럼 일요일 시작, 색상 적용)
            cols = st.columns(7)
            days_labels = [('일', 'sunday'), ('월', 'weekday'), ('화', 'weekday'), ('수', 'weekday'), ('목', 'weekday'), ('금', 'weekday'), ('토', 'saturday')]
            
            for i, (day_text, css_class) in enumerate(days_labels):
                # .day-header 클래스 추가 (모바일에서 글씨 작게 하려고)
                cols[i].markdown(f"<div class='{css_class} day-header'>{day_text}</div>", unsafe_allow_html=True)
            
            # 달력 데이터 (일요일 시작)
            cal = calendar.Calendar(firstweekday=6) 
            month_days = cal.monthdayscalendar(2026, 2)
            
            for week in month_days:
                cols = st.columns(7) # 7칸 생성
                for i, day in enumerate(week):
                    with cols[i]:
                        if day != 0:
                            info = st.session_state.menu_db.get(day, {"name": ""})
                            # 날짜만 크게, 메뉴명은 작게 (줄바꿈)
                            btn_text = f"{day}\n{info['name']}"
                            
                            if st.button(btn_text, key=f"d_{day}"):
                                st.session_state.selected_date = day
                                st.session_state.page = "detail"
                                st.rerun()
                        else:
                            # 빈 칸은 투명 박스로 자리만 차지하게 (모양 유지)
                            st.markdown("<div style='height:45px'></div>", unsafe_allow_html=True)
                
                # 줄 간격 아주 살짝
                st.write("")

        elif st.session_state.page == "detail":
            sel_day = st.session_state.selected_date
            menu = st.session_state.menu_db.get(sel_day)
            
            if st.button("← 뒤로가기"):
                st.session_state.page = "calendar"
                st.rerun()
                
            st.markdown(f"<div class='menu-card'>", unsafe_allow_html=True)
            st.markdown(f"<span class='highlight'>{sel_day}일</span> 메뉴", unsafe_allow_html=True)
            st.markdown(f"<h3>{menu['full_name']}</h3>", unsafe_allow_html=True)
            st.image(menu['img'], use_container_width=True)
            
            c1, c2 = st.columns(2)
            with c1: st.markdown(f"🔥 {menu['kcal']}")
            with c2: st.markdown(f"💰 {menu['price']:,}원")
            
            with st.form("order"):
                qty = st.number_input("수량", 1, 10, 1)
                loc = st.selectbox("수령", ["스마트베이", "오비즈", "동일"])
                if st.form_submit_button("주문하기", type="primary", use_container_width=True):
                    new_ord = {'날짜': f"2026-02-{sel_day}", '고객명': st.session_state.user_name, '메뉴': menu['full_name'], '수량': qty, '합계': qty*menu['price'], '거점': loc}
                    st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_ord])], ignore_index=True)
                    st.success("주문 완료!")
            st.markdown("</div>", unsafe_allow_html=True)

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
