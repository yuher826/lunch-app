import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10 Premium", layout="centered")

# 2. [디자인] 갤럭시 캘린더 스타일 (Grid + 자동 줄바꿈)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .stApp { background-color: #121212; color: #FFFFFF; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* -------------------------------------------------------- */
    /* [모바일] 768px 이하: 7칸 격자 + 텍스트 줄바꿈 최적화 */
    /* -------------------------------------------------------- */
    @media (max-width: 768px) {
        /* 1. 7칸 격자 (절대 깨지지 않는 뼈대) */
        div[data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(7, 1fr) !important;
            gap: 2px !important;
            padding: 0px !important;
        }
        
        div[data-testid="column"] {
            width: auto !important;
            flex: none !important;
            min-width: 0px !important;
            padding: 0px !important;
        }
        
        /* 2. 갤럭시 캘린더 스타일 버튼 */
        div.stButton > button {
            /* 크기 및 배치 */
            width: 100% !important;
            height: 65px !important;     /* 메뉴 2~3줄 들어갈 높이 */
            padding: 4px 1px !important; /* 내부 여백 */
            border-radius: 6px !important;
            
            /* [핵심] 텍스트 배치: 위(날짜) -> 아래(메뉴) */
            display: flex !important;
            flex-direction: column !important;
            justify-content: flex-start !important; /* 위쪽 정렬 */
            align-items: center !important;
            
            /* [핵심] 폰트 및 줄바꿈 설정 */
            font-size: 9px !important;
            line-height: 1.3 !important;
            text-align: center !important;
            
            /* 가로로 쓰다가 꽉 차면 다음 줄로! (갤럭시 스타일) */
            white-space: pre-wrap !important; /* \n 인식 + 자동 줄바꿈 */
            word-break: break-all !important; /* 단어가 길면 쪼개서라도 줄바꿈 */
            overflow: hidden !important; /* 칸 넘치면 숨김 */
        }
        
        /* 요일 헤더 */
        .day-header { font-size: 10px !important; margin-bottom: 3px !important; }
    }

    /* -------------------------------------------------------- */
    /* [PC] 큰 화면 스타일 */
    /* -------------------------------------------------------- */
    div[data-testid="column"] { min-width: 0px !important; }

    /* 공통 버튼 스타일 */
    div.stButton > button {
        background-color: #2C2C2C;
        border: 1px solid #333;
        color: #E0E0E0;
        border-radius: 6px;
        margin: 0px;
    }
    /* 오늘/선택 날짜 강조 */
    div.stButton > button:hover { border-color: #2979FF; color: #2979FF; }
    div.stButton > button:active { background-color: #2979FF; color: white; }

    /* 날짜/요일 색상 */
    .day-header { text-align: center; font-weight: bold; font-size: 12px; margin-bottom: 5px; }
    .sun { color: #FF5252; }
    .sat { color: #448AFF; }
    .wday { color: #AAAAAA; }

    /* 상세 페이지 카드 */
    .menu-card { background-color: #1E1E1E; border-radius: 15px; padding: 15px; margin-bottom: 15px; border: 1px solid #333; }
    .big-btn > button {
        background-color: #2979FF !important;
        color: white !important;
        height: 50px !important;
        font-size: 14px !important;
        display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 초기화
if 'menu_db' not in st.session_state:
    st.session_state.menu_db = {
        1: {"name": "직화제육", "img": "https://images.unsplash.com/photo-1626071466175-79aba923853e?w=400", "kcal": "650", "price": 7500},
        2: {"name": "연어포케", "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400", "kcal": "480", "price": 8500},
        3: {"name": "스테이크", "img": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=400", "kcal": "720", "price": 9000},
        4: {"name": "닭가슴살", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", "kcal": "350", "price": 7000},
        5: {"name": "안동찜닭", "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=400", "kcal": "600", "price": 7500},
    }
    for i in range(6, 32):
        if i % 2 == 0: st.session_state.menu_db[i] = {"name": "셰프특선", "img": "https://images.unsplash.com/photo-1544124499-58912cbddaad?w=400", "kcal": "500", "price": 7500}
        else: st.session_state.menu_db[i] = {"name": "주말특식", "img": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=400", "kcal": "900", "price": 8900}

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
        st.markdown("<div class='menu-card' style='text-align:center;'>", unsafe_allow_html=True)
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
# [화면 2] 메인 앱
# ==========================================
else:
    with st.sidebar:
        st.write(f"👋 **{st.session_state.user_name}**님")
        if st.button("로그아웃"): 
            st.session_state.logged_in = False
            st.rerun()

    if st.session_state.user_role == "user":
        
        # [모드 1] 갤럭시 캘린더 스타일 (Grid + Wrapping)
        if st.session_state.view_mode == "calendar":
            st.markdown("<h3 style='text-align:center;'>2026년 2월</h3>", unsafe_allow_html=True)
            
            # 요일 헤더
            cols = st.columns(7)
            days = ['일', '월', '화', '수', '목', '금', '토']
            classes = ['sun', 'wday', 'wday', 'wday', 'wday', 'wday', 'sat']
            for i, (d, c) in enumerate(zip(days, classes)):
                cols[i].markdown(f"<div class='day-header {c}'>{d}</div>", unsafe_allow_html=True)
            
            # 달력 본문
            cal = calendar.Calendar(firstweekday=6)
            month_days = cal.monthdayscalendar(2026, 2)
            
            for week in month_days:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    with cols[i]:
                        if day != 0:
                            info = st.session_state.menu_db.get(day, {"name": ""})
                            
                            # [핵심] 날짜 + 줄바꿈 + 메뉴명
                            # CSS에서 'pre-wrap'과 'break-all'을 줬기 때문에
                            # 갤럭시 캘린더처럼 칸에 맞춰서 자동으로 줄이 바뀝니다.
                            btn_text = f"{day}\n{info['name']}"
                            
                            if st.button(btn_text, key=f"d_{day}"):
                                st.session_state.selected_date = day
                                st.session_state.view_mode = "detail"
                                st.rerun()
                        else:
                            st.write("") 
            
            st.markdown("<br><p style='text-align:center; color:#666; font-size:12px;'>날짜를 터치하면 메뉴가 보입니다.</p>", unsafe_allow_html=True)

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
            <div class='menu-card'>
                <p style='color:#2979FF; margin-bottom:5px;'>2월 {sel_day}일</p>
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
                    st.success("주문 완료!")
                st.markdown('</div>', unsafe_allow_html=True)

    # 관리자 모드
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
