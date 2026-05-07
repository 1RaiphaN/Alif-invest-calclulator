import streamlit as st
import pandas as pd
import math

# Настройки страницы
st.set_page_config(
    page_title="ALIF INVEST",
    page_icon="💰",
    layout="centered"
)

# ===== СТИЛИ =====
st.markdown("""
<style>
.main {
    background-color: #0b0f19;
    color: white;
}

h1, h2, h3 {
    color: white;
    text-align: center;
}

.stButton>button {
    background-color: #2dc7c9;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    border: none;
}

.stNumberInput label {
    color: white !important;
    font-size: 16px !important;
}

[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

.result-box {
    background: #121826;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===== ЛОГОТИП =====
st.image(
    "https://i.imgur.com/9I6NRUm.png",
    width=180
)

st.title("ALIF INVEST")
st.subheader("Калькулятор рассрочек")

# ===== ВВОД ДАННЫХ =====
total_price = st.number_input(
    "Стоимость товара",
    value=105000,
    step=1000
)

down_payment = st.number_input(
    "Первоначальный взнос",
    value=0,
    step=1000
)

months = st.number_input(
    "Количество месяцев",
    value=10,
    step=1
)

monthly_rate = st.number_input(
    "Месячный процент (%)",
    value=5.0,
    step=1.0
)

# ===== КНОПКА =====
if st.button("Рассчитать"):

    # Сумма кредита
    loan_amount = total_price - down_payment

    # Общая сумма
    total_with_interest = loan_amount * (
        1 + (monthly_rate / 100) * months
    )

    # Округленный платеж
    monthly_payment = round(
        total_with_interest / months / 100
    ) * 100

    # ===== РЕЗУЛЬТАТЫ =====
    st.markdown(
        '<div class="result-box">',
        unsafe_allow_html=True
    )

    st.subheader("Результаты")

    st.write(
        f"Сумма после взноса: "
        f"{loan_amount:,.0f} руб."
    )

    st.write(
        f"Общая сумма выплат: "
        f"{total_with_interest:,.0f} руб."
    )

    st.write(
        f"Ежемесячный платеж: "
        f"{monthly_payment:,.0f} руб."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ===== ТАБЛИЦА =====
    schedule = []

    principal_per_month = (
        loan_amount / months
    )

    remaining = loan_amount

    for month in range(1, months + 1):

        remaining -= principal_per_month

        schedule.append({
            "Месяц": month,
            "Платеж": round(monthly_payment),
            "Основной долг": round(principal_per_month),
            "Остаток долга": max(
                round(remaining),
                0
            )
        })

    df = pd.DataFrame(schedule)

    st.subheader("График платежей")

    st.dataframe(
        df,
        use_container_width=True
    )