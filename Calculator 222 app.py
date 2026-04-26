import streamlit as st
import pandas as pd
import math

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

# Ежемесячный платеж с округлением
monthly_payment = math.ceil(total_with_interest / months)

# Коррекция последнего платежа
payments = [monthly_payment] * months
difference = sum(payments) - total_with_interest
payments[-1] -= difference

st.subheader("Результаты")
st.write(f"Сумма после первоначального взноса: {loan_amount:,.0f} руб.")
st.write(f"Общая сумма выплат: {sum(payments):,.0f} руб.")
st.write(f"Ежемесячный платеж (примерно, последний может отличаться): {monthly_payment:,.0f} руб.")

# График платежей
schedule = []
remaining = total_with_interest  # остаток долга начинается с полной суммы с процентами

for month in range(1, months + 1):
    payment = payments[month - 1]
    remaining -= payment
    schedule.append({
        "Месяц": month,
        "Платеж": payment,
        "Остаток долга": max(remaining, 0)
    })

st.subheader("График платежей")
df_schedule = pd.DataFrame(schedule)
st.dataframe(df_schedule.style.format({
    "Платеж": "{:,.0f}",
    "Остаток долга": "{:,.0f}"
}))
