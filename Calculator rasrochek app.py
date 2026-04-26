import streamlit as st
import pandas as pd
import math

st.title("Калькулятор рассрочек (простой процент)")

# Ввод данных
total_price = st.number_input("Стоимость товара", value=105000, step=1000)
down_payment = st.number_input("Первоначальный взнос", value=0, step=1000)
months = st.number_input("Количество месяцев рассрочки", value=10, step=1)
monthly_rate = st.number_input("Месячный процент (%)", value=5.0) / 100

# Сумма кредита
loan_amount = total_price - down_payment

# Общая сумма с процентами
total_with_interest = loan_amount * (1 + monthly_rate * months)

# ОКРУГЛЕНИЕ платежа до ровной суммы (например до 100 руб)
monthly_payment = math.ceil((total_with_interest / months) / 100) * 100

# Основной долг в месяц
principal_per_month = loan_amount / months

# График платежей
schedule = []
remaining = loan_amount

for month in range(1, months + 1):
    remaining -= principal_per_month
    
    # Последний месяц корректируем остаток
    if month == months:
        payment = total_with_interest - (monthly_payment * (months - 1))
        payment = round(payment, 2)
    else:
        payment = monthly_payment

    schedule.append({
        "Месяц": month,
        "Платеж": payment,
        "Основной долг": principal_per_month,
        "Остаток долга": max(remaining, 0)
    })

# Итоги
total_payment = sum(item["Платеж"] for item in schedule)

st.subheader("Результаты")
st.write(f"Сумма после первоначального взноса: {loan_amount:,.2f} руб.")
st.write(f"Общая сумма выплат: {total_payment:,.2f} руб.")
st.write(f"Ежемесячный платеж: {monthly_payment:,.0f} руб.")

# Таблица
st.subheader("График платежей")
df_schedule = pd.DataFrame(schedule)

st.dataframe(df_schedule.style.format({
    "Платеж": "{:,.0f}",
    "Основной долг": "{:,.0f}",
    "Остаток долга": "{:,.0f}"
}))