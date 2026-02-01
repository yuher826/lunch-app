import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10", layout="wide")

# 2. [디자인] 고급 파스텔 & 리스트형 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    /* 전체 배경: 고급진 크림 베이지 */
    .stApp { background-color: #FDFCF0; }
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* 모바일 좌우 여백 거의 없애기 */
    .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
    
    /* [핵심] 메뉴 리스트 카드 디자인 */
    .menu-row {
        background-color: #FFFFFF;
        border-bottom: 1px solid #EAEAEA; /* 메뉴 사이 구분선만 살짝 */
        padding: 10px;
        margin-bottom: 0px !important; /* 간격 없애기 */
        display: flex;
        align-items: center;
    }
    
    /* 이미지 스타일 */
    .menu-img {
        width: 80px; height: 80px;
        border-radius: 8px;
        object-fit: cover;
        margin-right: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* 텍스트 스타일 */
    .menu-info { flex-grow: 1; }
    .menu-day { font-size: 0.7rem; color: #7CA1B4; font-weight: 800; margin-bottom: 2px; }
    .menu-name { font-size: 1rem; color: #333; font-weight: 700; margin-bottom: 2px; }
    .menu-kcal { font-size: 0.7rem; color: #888; }
    
    /* 버튼 스타일 커스텀 */
    div.stButton > button {
        background-color: #7CA1B4 !important; /* 파스텔 블루 */
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        font-size: 0.8rem !important;
        padding: 5px 15px !important;
        height: auto !important;
    }
    
    /* 로그인 박스 */
    .auth-box {
        background-color: white;
        padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 20px; border: 1px solid #F0F0F0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 및 상태 초기화
if 'menu_data' not in st.session_state:
    st.session_state.menu_data = [
        {"day": "MON", "name": "직화 제육볶음", "img": "https://images.unsplash.com/photo-1626071466175-79aba923853e?w=200", "kcal": "650kcal"},
        {"day": "TUE", "name": "안동 찜닭정식", "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=200", "kcal": "580kcal"},
        {"day": "WED", "name": "마늘 소불고기", "img": "https://images.unsplash.com/photo-1624300627238-d698184f4751?w=200", "kcal": "610kcal"},
        {"day": "THU", "name": "춘천 닭갈비", "img": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=200", "kcal": "630kcal"},
        {"day": "FRI", "name": "버섯 소불고기", "img": "https://images.unsplash.com/photo-1544124499-58912cbddaad?w=200", "kcal": "590kcal"}
    ]

# [중요] 회원 정보를 저장할 공간 (DB 역할)
if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": "1234", "user": "1234"} # 기본 계정

if 'orders' not in st.session_state: st.session_state.orders = pd.DataFrame()
if 'purchases' not in st.session_state: st.session_state.purchases = pd.DataFrame()
if 'history_df' not in st.session_state:
    dates = pd.date_range(end=datetime.now(), periods=30)
    history_data = [{'날짜': d.strftime("%Y-%m-%d"), '총매출': np.random.randint(20,100)*7500, '총매입(원가)': np.random.randint(20,100)*4000} for d in dates]
    st.session_state.history_df = pd.DataFrame(history_data)

# 로그인 상태
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = None 
if 'user_name' not in st.session_state: st.session_state.user_name = None

# ==========================================
# [화면 1] 로그인 & 회원가입 (탭으로 분리)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #5B7DB1;'>🍱 12:10 든든밀</h2>", unsafe_allow_html=True)
    
    # 탭 생성
    tab_login, tab_signup = st.tabs(["🔑 로그인", "✨ 회원가입"])
    
    # [탭 1] 로그인
    with tab_login:
        with st.container():
            st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
            l_id = st.text_input("아이디", key="l_id")
            l_pw = st.text_input("비밀번호", type="password", key="l_pw")
            
            if st.button("로그인", use_container_width=True, type="primary"):
                # DB에서 아이디/비번 확인
                if l_id in st.session_state.user_db and st.session_state.user_db[l_id] == l_pw:
                    st.session_state.logged_in = True
                    st.session_state.user_name = l_id
                    # 관리자 여부 체크
                    if l_id == "admin": st.session_state.user_role = "admin"
                    else: st.session_state.user_role = "user"
                    st.rerun()
                else:
                    st.error("아이디나 비밀번호를 확인해주세요.")
            st.markdown("</div>", unsafe_allow_html=True)

    # [탭 2] 회원가입 (작동함!)
    with tab_signup:
        with st.container():
            st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
            new_id = st.text_input("새 아이디", key="n_id")
            new_pw = st.text_input("새 비밀번호", type="password", key="n_pw")
            new_pw_chk = st.text_input("비밀번호 확인", type="password", key="n_pw_c")
            
            if st.button("회원가입 완료", use_container_width=True):
                if new_id and new_pw:
                    if new_id in st.session_state.user_db:
                        st.error("이미 있는 아이디입니다.")
                    elif new_pw != new_pw_chk:
                        st.error("비밀번호가 서로 다릅니다.")
                    else:
                        # [핵심] DB에 추가
                        st.session_state.user_db[new_id] = new_pw
                        st.success(f"가입 환영합니다! '{new_id}'님, 로그인 탭에서 로그인해주세요.")
                else:
                    st.warning("빈칸을 채워주세요.")
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# [화면 2] 메인 서비스
# ==========================================
else:
    # 사이드바
    with st.sidebar:
        st.info(f"안녕하세요, **{st.session_state.user_name}**님!")
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.rerun()

    # [A] 사용자 화면 (리스트형 디자인 적용)
    if st.session_state.user_role == "user":
        if 'page' not in st.session_state: st.session_state.page = 'main'
        if 'selected_item' not in st.session_state: st.session_state.selected_item = None
        
        # 메인 리스트
        if st.session_state.page == 'main':
            st.markdown("#### 📅 금주의 식단")
            
            # 여기서부터 메뉴 리스트 시작
            for i, item in enumerate(st.session_state.menu_data):
                # 카드 컨테이너 (CSS로 꾸밈)
                with st.container():
                    # Streamlit 컬럼으로 레이아웃 잡기 (이미지 | 텍스트+버튼)
                    c_img, c_txt, c_btn = st.columns([1, 2, 1])
                    
                    with c_img:
                        st.image(item['img'], use_container_width=True) # CSS로 둥글게 처리됨
                    
                    with c_txt:
                        # 간격 없이 텍스트 배치
                        st.markdown(f"""
                        <div style="display:flex; flex-direction:column; justify-content:center; height:100%;">
                            <span style="font-size:0.7rem; color:#7CA1B4; font-weight:bold;">{item['day']}</span>
                            <span style="font-size:1rem; font-weight:bold;">{item['name']}</span>
                            <span style="font-size:0.7rem; color:#aaa;">{item['kcal']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with c_btn:
                        # 버튼을 누르면 상세페이지로 이동
                        st.write("") # 줄바꿈으로 수직 중앙 정렬 효과
                        if st.button("담기", key=f"add_{i}"):
                            st.session_state.selected_item = item
                            st.session_state.page = 'detail'
                            st.rerun()
                    
                    # 구분선 느낌
                    st.markdown("<hr style='margin: 5px 0; border: 0; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

            # 하단 주문 플로팅 바 느낌
            st.markdown("---")
            with st.container():
                st.markdown("###### 🛒 주문하기")
                with st.form("order_form"):
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        bld = st.selectbox("수령 장소", ["스마트베이", "오비즈타워", "동일테크노"], label_visibility="collapsed")
                    with c2:
                        qty = st.number_input("수량", 1, 10, 1, label_visibility="collapsed")
                    
                    sel_menu = st.session_state.pre_selected if 'pre_selected' in st.session_state else "메뉴를 '담기' 해주세요"
                    st.caption(f"선택: {sel_menu}")
                    
                    if st.form_submit_button("결제하기 (7,500원)", type="primary", use_container_width=True):
                        if sel_menu != "메뉴를 '담기' 해주세요":
                            new_ord = {'시간': datetime.now().strftime("%H:%M"), '성함': st.session_state.user_name, '거점': bld, '메뉴': sel_menu, '수량': qty, '합계': qty*7500}
                            st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_ord])], ignore_index=True)
                            st.success("주문 성공!")
                        else:
                            st.warning("메뉴를 골라주세요.")

        # 상세 페이지
        elif st.session_state.page == 'detail':
            m = st.session_state.selected_item
            st.image(m['img'], use_container_width=True)
            st.markdown(f"### {m['name']}")
            st.info(m['desc'] if 'desc' in m else "든든하고 맛있는 한 끼 식사")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("취소", use_container_width=True):
                    st.session_state.page = 'main'
                    st.rerun()
            with c2:
                if st.button("확정", type="primary", use_container_width=True):
                    st.session_state.pre_selected = m['name']
                    st.session_state.page = 'main'
                    st.rerun()

    # [B] 관리자 화면 (기존 기능 유지)
    elif st.session_state.user_role == "admin":
        st.title("📊 사장님 페이지")
        st.info("관리자 모드입니다.")
        
        # (기존 관리자 기능 코드 - 여기에 이어서 쓰면 됨)
        # 테스트를 위해 간단한 매출만 표시합니다.
        if not st.session_state.orders.empty:
            st.metric("오늘 매출", f"{st.session_state.orders['합계'].sum():,}원")
            st.dataframe(st.session_state.orders)
        else:
            st.write("아직 주문이 없습니다.")

