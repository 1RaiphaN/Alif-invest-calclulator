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

# Ежемесячный платеж до округления
monthly_payment = total_with_interest / months

# Округление платежей до целых рублей
rounded_monthly_payment = math.ceil(monthly_payment)

# Коррекция последнего платежа, чтобы сумма была точной
payments = [rounded_monthly_payment] * months
total_rounded = rounded_monthly_payment * months
difference = total_rounded - total_with_interest

# Уменьшаем последний платеж на разницу
payments[-1] = rounded_monthly_payment - difference

st.subheader("Результаты")
st.write(f"Сумма после первоначального взноса: {loan_amount:,.2f} руб.")
st.write(f"Общая сумма выплат (округлённая): {sum(payments):,.2f} руб.")
st.write(f"Ежемесячный платеж (примерно, последний может отличаться): {rounded_monthly_payment:,.0f} руб.")

# График платежей
schedule = []
remaining = loan_amount
principal_per_month = loan_amount / months

for month in range(1, months + 1):
    payment = payments[month - 1]
    interest_part = (total_with_interest - loan_amount) / months
    principal_part = payment - interest_part
    remaining -= principal_part
    schedule.append({
        "Месяц": month,
        "Платеж": payment,
        "Основной долг": principal_part,
        "Остаток долга": max(remaining, 0)
    })

st.subheader("График платежей")
df_schedule = pd.DataFrame(schedule)
st.dataframe(df_schedule.style.format({
    "Платеж": "{:,.0f}",
    "Основной долг": "{:,.0f}",
    "Остаток долга": "{:,.0f}"
}))
