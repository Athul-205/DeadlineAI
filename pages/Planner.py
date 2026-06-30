import streamlit as st
import sqlite3
from datetime import datetime, date

from ai_agent import generate_schedule

st.set_page_config(
    page_title="AI Planner",
    page_icon="🧠",
    layout="wide"
)

st.sidebar.markdown("""
<h2 style="text-align:center;margin-bottom:0;">
<span style="color:white;">Deadline</span>
<span style="color:#8B5CF6;">AI</span>
</h2>

<p style="
text-align:center;
color:#94A3B8;
font-size:13px;
margin-top:4px;">
Adaptive AI Productivity
</p>

<hr style="border:1px solid #243153;">
""", unsafe_allow_html=True)

st.markdown("""
<style>

.stApp{
background:linear-gradient(
180deg,
#090F1F 0%,
#101B3D 50%,
#090F1F 100%
);
}

[data-testid="stSidebar"]{
background:linear-gradient(
180deg,
#090F1F,
#101B3D,
#090F1F
);
}

h1{
color:white;
text-align:center;
}

.stButton>button{

width:100%;
background:linear-gradient(
90deg,
#8B5CF6,
#2563EB
);

color:white;
border:none;
border-radius:12px;
font-weight:bold;

}

.stButton>button:hover{

background:linear-gradient(
90deg,
#7C3AED,
#1D4ED8
);

}

hr{
border:1px solid #243153;
}
[data-testid="stSidebarNav"] a[aria-current="page"]{

    background:linear-gradient(
        90deg,
        #8B5CF6,
        #2563EB
    );

    color:white !important;

    border-radius:15px;

    font-weight:bold;

    box-shadow:0 0 20px rgba(139,92,246,.45);

}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<h1>
<span style="color:white;">AI</span>
<span style="color:#8B5CF6;">Planner</span>
</h1>

<p style="
text-align:center;
color:#94A3B8;
font-size:18px;">
Generate your optimized daily schedule
</p>
""", unsafe_allow_html=True)



col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    generate = st.button("🧠 Generate My Day", use_container_width=True)

if generate:

    conn = sqlite3.connect("database/tasks.db")
    cursor = conn.cursor()

    ...

    conn = sqlite3.connect("database/tasks.db")
    cursor = conn.cursor()

    # -------------------------
    # Current Time
    # -------------------------

    current_time = datetime.now().strftime("%I:%M %p")

    # -------------------------
    # Get Today's Commitments
    # -------------------------

    cursor.execute("""
    SELECT title,start_time,end_time
    FROM commitments
    WHERE date=?
    ORDER BY start_time
    """,(str(date.today()),))

    commitments = cursor.fetchall()

    # -------------------------
    # Get Pending Tasks
    # -------------------------

    cursor.execute("""
    SELECT task_name,deadline,duration,category
    FROM tasks
    WHERE status='Pending'
    ORDER BY deadline
    """)

    tasks = cursor.fetchall()

    conn.close()

    if len(tasks)==0:

        st.warning("No pending tasks.")

    else:

        commitment_text = ""

        if len(commitments)==0:

            commitment_text = "No commitments today."

        else:

            for c in commitments:

                commitment_text += f"""
{c[0]}
{c[1]} - {c[2]}

"""

        task_text = ""

        for task in tasks:

            task_text += f"""
Task : {task[0]}
Deadline : {task[1]}
Duration : {task[2]} minutes
Category : {task[3]}

"""

        full_prompt = f"""

Current Time

{current_time}

Today's Commitments

{commitment_text}

Pending Tasks

{task_text}

"""

        with st.spinner("🤖 AI is planning your day..."):

            result = generate_schedule(full_prompt)

        st.success("Plan Generated")

        st.markdown(result)