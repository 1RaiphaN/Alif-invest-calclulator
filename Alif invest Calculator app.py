import streamlit as st
import pandas as pd

st.title("Калькулятор рассрочек (простой процент)")

# Ввод данных
total_price = st.number_input("Стоимость товара", value=700000, step=1000)
down_payment = st.number_input("Первоначальный взнос", value=0, step=1000)
months = st.number_input("Количество месяцев рассрочки", value=10, step=1)
monthly_rate = st.number_input("Месячный процент (%)", value=5.0) / 100

# Сумма кредита
loan_amount = total_price - down_payment

# Итоговая сумма с суммарным процентом
total_with_interest = loan_amount * (1 + monthly_rate * months)

# Ежемесячный платеж
monthly_payment = total_with_interest / months

st.subheader("Результаты")
st.write(f"Сумма после первоначального взноса: {loan_amount:,.2f} руб.")
st.write(f"Общая сумма выплат: {total_with_interest:,.2f} руб.")
st.write(f"Ежемесячный платеж: {monthly_payment:,.2f} руб.")

# График платежей
principal_per_month = loan_amount / months
interest_per_month = (total_with_interest - loan_amount) / months
schedule = []

remaining = loan_amount
for month in range(1, months + 1):
    remaining -= principal_per_month
    schedule.append({
        "Месяц": month,
        "Платеж": monthly_payment,
        "Основной долг": principal_per_month,
        "Остаток долга": max(remaining, 0)
    })

st.subheader("График платежей")
df_schedule = pd.DataFrame(schedule)
st.dataframe(df_schedule.style.format({
    "Платеж": "{:,.2f}",
    "Основной долг": "{:,.2f}",
    "Остаток долга": "{:,.2f}"
}))