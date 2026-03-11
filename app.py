import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import numpy as np

st.set_page_config(page_title="Renewals Integration Control Tower", layout="wide")

# -------------------------
# HEADER
# -------------------------

st.markdown("""
# Renewals Integration Control Tower
### InsuranceDekho → RenewBuy Merger
""")

# -------------------------
# SIDEBAR INPUTS
# -------------------------

st.sidebar.header("Migration Inputs")

motor_total = 6000000
health_total = 220000
life_total = 25000

motor_migrated = st.sidebar.number_input("Motor Policies Migrated", value=1200000)
health_migrated = st.sidebar.number_input("Health Policies Migrated", value=50000)
life_migrated = st.sidebar.number_input("Life Policies Migrated", value=8000)

days_elapsed = st.sidebar.number_input("Days Since Migration Start", value=10)

avg_motor_premium = st.sidebar.number_input("Avg Motor Premium", value=6000)
avg_health_premium = st.sidebar.number_input("Avg Health Premium", value=18000)
avg_life_premium = st.sidebar.number_input("Avg Life Premium", value=25000)

# -------------------------
# DATA MODEL
# -------------------------

lob_data = pd.DataFrame({
    "LOB":["Motor","Health","Life"],
    "Total":[motor_total,health_total,life_total],
    "Migrated":[motor_migrated,health_migrated,life_migrated]
})

lob_data["Remaining"] = lob_data["Total"] - lob_data["Migrated"]
lob_data["Completion"] = lob_data["Migrated"]/lob_data["Total"]*100

total_policies = lob_data["Total"].sum()
migrated_total = lob_data["Migrated"].sum()
completion = migrated_total/total_policies*100

velocity = migrated_total/days_elapsed

remaining = total_policies - migrated_total

if velocity > 0:
    forecast_days = remaining/velocity
else:
    forecast_days = 0

expected_completion = date.today() + pd.Timedelta(days=int(forecast_days))

# -------------------------
# KPI TILES
# -------------------------

st.subheader("Program Overview")

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric("Total Policies", f"{total_policies:,}")
col2.metric("Migrated", f"{migrated_total:,}")
col3.metric("Remaining", f"{remaining:,}")
col4.metric("Completion %", f"{round(completion,2)}%")
col5.metric("Velocity (Policies/Day)", f"{round(velocity):,}")

st.divider()

# -------------------------
# GAUGE CHART
# -------------------------

st.subheader("Migration Completion")

fig = go.Figure(go.Indicator(
mode="gauge+number",
value=completion,
title={'text':"Migration Progress"},
gauge={'axis':{'range':[0,100]},
'bar':{'color':"green"}}
))

st.plotly_chart(fig,use_container_width=True)

# -------------------------
# LOB BREAKDOWN
# -------------------------

st.subheader("LOB Migration Status")

fig = px.bar(
lob_data,
x="LOB",
y="Completion",
text=lob_data["Completion"].round(1),
color="LOB"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------
# MIGRATION FORECAST
# -------------------------

st.subheader("Migration Forecast")

col1,col2 = st.columns(2)

col1.metric("Remaining Policies", f"{remaining:,}")
col2.metric("Expected Completion Date", str(expected_completion))

forecast_df = pd.DataFrame({
"Stage":["Migrated","Remaining"],
"Policies":[migrated_total,remaining]
})

fig = px.pie(forecast_df, names="Stage", values="Policies")

st.plotly_chart(fig,use_container_width=True)

# -------------------------
# REVENUE EXPOSURE
# -------------------------

st.subheader("Revenue Exposure")

motor_rev = motor_total*avg_motor_premium
health_rev = health_total*avg_health_premium
life_rev = life_total*avg_life_premium

total_rev = motor_rev+health_rev+life_rev

revenue_risk = (100-completion)/100 * total_rev

col1,col2 = st.columns(2)

col1.metric("Total Renewal Revenue", f"₹{round(total_rev/10000000,2)} Cr")
col2.metric("Revenue at Risk", f"₹{round(revenue_risk/10000000,2)} Cr")

# -------------------------
# INSURER RISK HEATMAP
# -------------------------

st.subheader("Insurer Migration Risk")

insurers = pd.DataFrame({
"Insurer":[
"HDFC Ergo","ICICI Lombard","Star Health",
"Niva Bupa","Aditya Birla Life","Bajaj Life"
],
"LOB":[
"Motor","Motor","Health",
"Health","Life","Life"
],
"Risk":[20,40,70,30,50,60]
})

fig = px.density_heatmap(
insurers,
x="Insurer",
y="LOB",
z="Risk",
color_continuous_scale="reds"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------
# PROGRAM HEALTH SCORE
# -------------------------

risk_avg = insurers["Risk"].mean()
health_score = 100-risk_avg

st.subheader("Program Health")

st.metric("Integration Health Score", f"{round(health_score,1)}/100")

# -------------------------
# TIMELINE
# -------------------------

st.subheader("Migration Timeline")

timeline = pd.DataFrame({
"Phase":[
"IRDA Approval",
"Insurer Alignment",
"Data Migration",
"Parallel Systems",
"Full Cutover"
],
"Status":[
"Pending",
"In Progress",
"Pending",
"Pending",
"Pending"
],
"Deadline":[
"2026-05-01",
"2026-05-15",
"2026-06-01",
"2026-06-20",
"2026-07-01"
]
})

st.dataframe(timeline,use_container_width=True)

# -------------------------
# WORKSTREAM PROGRESS
# -------------------------

st.subheader("Workstream Progress")

workstreams = pd.DataFrame({
"Workstream":[
"Health Data Migration",
"Motor TP Linking",
"Life ECS Migration",
"Insurer UAT",
"Renewal Notice Update"
],
"Progress":[40,10,25,60,50]
})

fig = px.bar(workstreams,x="Workstream",y="Progress",color="Progress")

st.plotly_chart(fig,use_container_width=True)