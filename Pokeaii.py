import plotly.graph_objects as go
import numpy as np
import plotly.figure_factory as ff
import streamlit as st
import pandas as pd
import pokeai


st.title('Pokemon Type Recommend')


numberMat, types = pokeai.getTypeMapMat()

# sidebar

option1 = st.sidebar.multiselect(
    'Existing Pokemon types',
    types,
    default=None)
option2 = st.sidebar.radio(
    'Strategy',
    ["Balance", "Attack", "Defense"],
    index=0)

# main page

st.subheader('Recommend')
# my_slot1 = st.empty()
# my_slot1.text('This will appear second')

def readReport(report, section):
    data = report.get(section)
    if data:
        values = ', '.join(report[section])
        n = len(report[section])
        message = f'Top{n} {section}: {values}'
    return message
doctor = pokeai.PokeDoctor(strategy=option2.lower())

# Next Type Recommend
recommendReport = doctor.getRecommend(option1)
nextTypeRank = recommendReport['nextTypeRank']
nextRecommend = readReport(recommendReport, 'next')
st.write(nextRecommend)

x = [x[0] for x in nextTypeRank]
y = [x[1] for x in nextTypeRank]
fig2 = go.Figure(
    data=[go.Bar(x=x, y=y)],
    layout_title_text="Next Recommend Pokemon Type Rank"
)
st.plotly_chart(fig2)

if len(option1) > 0:
    st.subheader('Team Analysis')
    report = doctor.getReport(option1)
    for section in ('goodness', 'weakness'):
        message = readReport(report, section)
        message
    # Chart goodness weakness
    details = report["details"]
    defense = [x[1][0] for x in details]
    attack = [x[1][1] for x in details]
    overall = [x[1][2] for x in details]
    labels = [x[0] for x in details]
    fig1 = go.Figure(layout_title_text="Goodness and Weakness Type Rank")
    fig1.add_trace(go.Bar(x=labels, y=overall,
                          name="Overall", marker_color="yellow"))
    fig1.add_trace(go.Bar(x=labels, y=attack,
                          name="Attack", marker_color="indianred"))
    fig1.add_trace(go.Bar(x=labels, y=defense,
                          name="Defense", marker_color="lightgreen"))
    st.plotly_chart(fig1)
