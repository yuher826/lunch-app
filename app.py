import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="12:10 든든밀 ERP", layout="wide")

# 2. 스타일 설정 (사용자용 초소형 + 관리자용 대시보드)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; }

    /* [사용자] 모바일 강제 가로 정렬 */
    div[data-testid="column"] { padding: 0px 1px !important; min-width: 0 !important; }

    .micro-card {
        background-color: white; border-radius: 4px; padding: 4px 1px;
        text-align: center; border: 1px solid #dee2e6; height: 100%;
    }
    .day-badge { font-size: 0.6rem; font-weight: 800; color: #5B7DB1; margin-bottom: 2px; display: block; }
    .tiny-img { width: 35px; height: 35px; border-radius: 3px; object-fit: cover; margin: 0 auto 2px; display: block; }
    .menu-txt { font-size: 0.5rem; font-weight: 700; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    div.stButton > button {
        width: 100%; font-size: 0.5rem !important; padding: 0px !important;
        height: 18px !important; min-height: 18px !important; margin-top: 2px !important;
    }

    .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 초기화
if 'menu_data' not in st.session_state:
    st.session_state.menu_data = [
        {"day": "월", "name": "직화제육", "img": "https://images.unsplash.com/photo-1626071466175-79aba923853e?w=100", "kcal": "650k"},
        {"day": "화", "name": "안동찜닭", "img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=100", "kcal": "580k"},
        {"day": "수", "name": "마늘불고기", "img": "https://images.unsplash.com/photo-1624300627238-d698184f4751?w=100", "kcal": "610k"},
        {"day": "목", "name": "닭갈비", "img": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=100", "kcal": "630k"},
        {"day": "금", "name": "소불고기", "img": "https://images.unsplash.com/photo-1544124499-58912cbddaad?w=100", "kcal": "590k"}
    ]

if 'orders' not in st.session_state:
    st.session_state.orders = pd.DataFrame([
        {'날짜': datetime.now().strftime("%Y-%m-%d"), '시간': '09:15', '성함': '김철수', '거점': '평촌 스마트베이', '메뉴': '직화제육', '수량': 1, '합계': 7500, '원가': 4000},
        {'날짜': datetime.now().strftime("%Y-%m-%d"), '시간': '09:42', '성함': '이영희', '거점': '오비즈타워', '메뉴': '안동찜닭', '수량': 2, '합계': 15000, '원가': 8000},
    ])

if 'purchases' not in st.session_state:
    st.session_state.purchases = pd.DataFrame([
        {'날짜': datetime.now().strftime("%Y-%m-%d"), '구분': '식자재', '내용': '돼지 전지 10kg', '거래처': '한돈유통', '금액': 85000},
        {'날짜': datetime.now().strftime("%Y-%m-%d"), '구분': '포장재', '내용': '용기 100개', '거래처': '패키지몰', '금액': 32000}
    ])

if 'history_df' not in st.session_state:
    dates = pd.date_range(end=datetime.now(), periods=30)
    history_data = []
    for d in dates:
        sales_qty = np.random.randint(20, 100)
        history_data.append({
            '날짜': d.strftime("%Y-%m-%d"),
            '총매출': sales_qty * 7500,
            '총매입(원가)': sales_qty * 4000,
            '주문건수': sales_qty
        })
    st.session_state.history_df = pd.DataFrame(history_data)

if 'page' not in st.session_state: st.session_state.page = 'main'
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'pre_selected' not in st.session_state: st.session_state.pre_selected = "직화제육"

# --- 사이드바 ---
with st.sidebar:
    st.title("12:10 ERP")
    mode = st.radio("모드 선택", ["🍱 사용자 (주문)", "📊 관리자 (통합관제)"])

# ==========================================
# [모드 1] 사용자 화면
# ==========================================
if mode == "🍱 사용자 (주문)":

    if st.session_state.page == 'main':
        st.caption("오늘의 메뉴 (10:30 마감)")
        cols = st.columns(5)
        for i, item in enumerate(st.session_state.menu_data):
            with cols[i]:
                st.markdown(f"""
                    <div class="micro-card">
                        <span class="day-badge">{item['day']}</span>
                        <img src="{item['img']}" class="tiny-img">
                        <div class="menu-txt">{item['name']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("보기", key=f"btn_{i}"):
                    st.session_state.selected_item = item
                    st.session_state.page = 'detail'
                    st.rerun()

        st.divider()

        st.caption("📝 간편 주문")
        with st.form("order_form"):
            c1, c2 = st.columns(2)
            with c1:
                u_name = st.text_input("성함", value="홍길동")
                u_bld = st.selectbox("수령 거점", ["평촌 스마트베이", "오비즈타워", "동일테크노"])
            with c2:
                u_menu = st.text_input("메뉴", value=st.session_state.pre_selected, disabled=True)
                u_qty = st.number_input("수량", min_value=1, value=1)

            if st.form_submit_button("7,500원 결제", use_container_width=True):
                new_row = {
                    '날짜': datetime.now().strftime("%Y-%m-%d"),
                    '시간': datetime.now().strftime("%H:%M"),
                    '성함': u_name, '거점': u_bld, '메뉴': u_menu,
                    '수량': u_qty, '합계': u_qty*7500, '원가': u_qty*4000
                }
                st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_row])], ignore_index=True)
                st.success("주문 완료!")

    elif st.session_state.page == 'detail':
        m = st.session_state.selected_item
        if st.button("🔙 뒤로"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"**{m['day']}요일: {m['name']}**")
        st.image(m['img'], width=150)
        st.button("✅ 선택", type="primary", on_click=lambda: [st.session_state.update(pre_selected=m['name'], page='main')])

# ==========================================
# [모드 2] 관리자 화면
# ==========================================
elif mode == "📊 관리자 (통합관제)":
    st.title("📊 통합 경영 관리")

    df_ord = st.session_state.orders
    df_buy = st.session_state.purchases

    t_sales = df_ord['합계'].sum()
    t_cost = df_buy['금액'].sum()
    t_profit = t_sales - t_cost
    margin = (t_profit / t_sales * 100) if t_sales > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("총 매출", f"{t_sales:,} 원")
    k2.metric("총 지출", f"{t_cost:,} 원")
    k3.metric("순수익", f"{t_profit:,} 원")
    k4.metric("순수익률", f"{margin:.1f}%")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["🚀 실시간 운영", "💰 고급 매출분석", "🛒 매입 등록", "📈 통합 보고서"])

    with tab1:
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.subheader("📋 실시간 주문 장부")
            st.dataframe(df_ord[['시간','성함','거점','메뉴','수량']], use_container_width=True, hide_index=True)
        with c2:
            st.subheader("📦 배송 거점 집계")
            pivot = df_ord.groupby('거점')['수량'].sum().reset_index()
            st.dataframe(pivot, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("📈 시각적 매출 분석")
        col_anal1, col_anal2 = st.columns(2)
        with col_anal1:
            st.markdown("##### 🏆 메뉴별 판매 순위")
            menu_rank = df_ord.groupby('메뉴')[['수량', '합계']].sum().sort_values('수량', ascending=False)
            st.bar_chart(menu_rank['수량']) 

        with col_anal2:
            st.markdown("##### 🏢 거점별 점유율")
            bld_rank = df_ord.groupby('거점')['수량'].sum()
            st.bar_chart(bld_rank)

        st.markdown("---")
        st.markdown("##### 🔥 [Heatmap] 메뉴 선호도")
        heatmap_df = pd.pivot_table(df_ord, values='수량', index='메뉴', columns='거점', aggfunc='sum', fill_value=0)
        try:
            st.dataframe(heatmap_df.style.background_gradient(cmap='Blues'), use_container_width=True)
        except:
            st.dataframe(heatmap_df, use_container_width=True)

    with tab3:
        c_in, c_view = st.columns(2)
        with c_in:
            st.subheader("🧾 지출 입력")
            with st.form("buy_form", clear_on_submit=True):
                p_date = st.date_input("날짜", datetime.now())
                p_cat = st.selectbox("항목", ["식자재", "부자재", "배송비", "기타"])
                p_content = st.text_input("내용")
                p_price = st.number_input("금액", step=1000)
                if st.form_submit_button("등록"):
                    new_buy = {'날짜': str(p_date), '구분': p_cat, '내용': p_content, '거래처': '', '금액': p_price}
                    st.session_state.purchases = pd.concat([st.session_state.purchases, pd.DataFrame([new_buy])], ignore_index=True)
                    st.rerun()
        with c_view:
            st.subheader("📋 지출 내역")
            st.dataframe(st.session_state.purchases, use_container_width=True)

    with tab4:
        st.subheader("📈 경영 분석 보고서")
        df_hist = st.session_state.history_df
        period = st.radio("분석 기준", ["일별 추이", "월별 보고서"], horizontal=True)
        if period == "일별 추이":
            st.line_chart(df_hist.set_index('날짜')[['총매출', '총매입(원가)']])
        elif period == "월별 보고서":
            df_hist['월'] = pd.to_datetime(df_hist['날짜']).dt.strftime('%Y-%m')
            monthly_df = df_hist.groupby('월')[['총매출', '총매입(원가)']].sum()
            st.bar_chart(monthly_df)
            st.dataframe(monthly_df)