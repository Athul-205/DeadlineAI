import streamlit as st
import sqlite3
from datetime import datetime, date
from ai_agent import generate_schedule
def format_time(t):
    return datetime.strptime(t, "%H:%M:%S").strftime("%I:%M %p")
st.set_page_config(
    page_title="DeadlineAI",
    page_icon="🤖",
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
margin-top:5px;">
Adaptive AI Productivity
</p>

<hr style="border:1px solid #243153;">
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ================= Sidebar ================= */

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#090F1F,#101B3D,#090F1F);
    border-right:1px solid #283B70;
}

[data-testid="stSidebar"] *{
    color:white;
}

[data-testid="stSidebarNav"]{
    padding-top:20px;
}

[data-testid="stSidebarNav"] a{

    border-radius:15px;
    padding:12px 15px;
    margin-bottom:8px;
    transition:0.3s;

}

[data-testid="stSidebarNav"] a:hover{

    background:linear-gradient(
        90deg,
        rgba(124,58,237,.35),
        rgba(37,99,235,.35)
    );

    border:1px solid #7C3AED;

}

[data-testid="stSidebarNav"] a[aria-current="page"]{

    background:linear-gradient(
        90deg,
        #7C3AED,
        #5B21B6
    );

    color:white;

    font-weight:700;

    box-shadow:0 0 18px rgba(124,58,237,.45);

}            
/* Background */
.stApp{
    background:linear-gradient(
        180deg,
        #090F1F 0%,
        #101B3D 50%,
        #090F1F 100%
    );
}


/* Main title */
h1{
    color:white;
    text-align:center;
    font-size:45px;

    text-shadow:
    0 0 10px #8B5CF6,
    0 0 25px #7C3AED,
    0 0 40px #2563EB;

    animation:glow 2s infinite alternate;
}

@keyframes glow{

from{
    text-shadow:0 0 10px #8B5CF6;
}

to{
    text-shadow:
    0 0 25px #8B5CF6,
    0 0 45px #2563EB;
}

}

/* Subheaders */
h2,h3{
    color:#60a5fa;
}

/* Cards */
div[data-testid="stVerticalBlock"] > div:has(div.stButton){
    background:#1e293b;
    border-radius:15px;
    padding:18px;
    border:1px solid #334155;
    box-shadow:0px 5px 15px rgba(0,0,0,0.25);
}

/* Metric cards */
div[data-testid="metric-container"]{
    background:#1e293b;
    border:1px solid #334155;
    padding:18px;
    border-radius:15px;
}

/* Buttons */
.stButton > button{

    width:100%;

    border-radius:12px;

    background:linear-gradient(
        90deg,
        #7C3AED,
        #8B5CF6,
        #2563EB
    );

    background-size:250% 250%;

    color:white;

    border:none;

    font-weight:bold;

    transition:.35s;

}

.stButton > button:hover{

    background-position:right center;

    transform:scale(1.03);

    box-shadow:0 0 20px rgba(139,92,246,.45);

}

/* Info boxes */
div[data-testid="stAlert"]{
    border-radius:12px;
}
hr{
    border:1px solid #243153;
}
/* Card Hover Animation */

div[data-testid="stVerticalBlock"] > div{

    transition:all .25s ease;

}

div[data-testid="stVerticalBlock"] > div:hover{

    transform:translateY(-4px);

    box-shadow:0 0 25px rgba(139,92,246,.35);

}           
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align:center;font-size:48px;">
🤖 <span style="color:white;">Deadline</span><span style="color:#8B5CF6;">AI</span>
</h1>

<p style="
text-align:center;
color:#94A3B8;
font-size:18px;
margin-top:-8px;">
Adaptive AI Productivity Assistant
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================
# Current Date & Time
# ==========================

now = datetime.now()

# Greeting
hour = now.hour

if hour < 12:
    greeting = "🌅 Good Morning"
elif hour < 17:
    greeting = "☀️ Good Afternoon"
elif hour < 21:
    greeting = "🌆 Good Evening"
else:
    greeting = "🌙 Good Night"

st.markdown(
    f"""
    <h2 style="
        text-align:center;
        color:#A78BFA;
        margin-bottom:20px;">
        {greeting}
    </h2>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.info(f"🕒 Current Time : {now.strftime('%I:%M %p')}")

with col2:
    st.info(f"📅 Today : {now.strftime('%d %B %Y')}")

# ==========================
# Database
# ==========================

conn = sqlite3.connect("database/tasks.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM tasks")
total_tasks = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Completed'")
completed = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM commitments WHERE date=?", (str(date.today()),))
commitments = cursor.fetchone()[0]

# ==========================
# Statistics
# ==========================

st.markdown("## 📊 Dashboard")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("📋 Tasks", total_tasks)

with c2:
    st.metric("📅 Commitments", commitments)

with c3:
    st.metric("✅ Completed", completed)

st.markdown("---")

# ==========================
# Today's Commitments
# ==========================

st.markdown("## 📅 Today's Commitments")

cursor.execute("""
SELECT title,start_time,end_time
FROM commitments
WHERE date=?
ORDER BY start_time
""",(str(date.today()),))

rows = cursor.fetchall()

if len(rows)==0:
    st.info("No commitments added today.")
else:

    for row in rows:

     with st.container(border=True):

        st.write(f"### 📅 {row[0]}")
        st.write(f"🕒 {format_time(row[1])} - {format_time(row[2])}")
st.markdown("---")

# ==========================
# Pending Tasks
# ==========================

# ==========================
# Pending Tasks
# ==========================

st.markdown("## 📋 Pending Tasks")

cursor.execute("""
SELECT id, task_name, deadline, duration
FROM tasks
WHERE status='Pending'
ORDER BY deadline
""")

tasks = cursor.fetchall()

if len(tasks) == 0:

    st.success("No pending tasks.")

else:

    for task in tasks:

        with st.container(border=True):

            st.write(f"### {task[1]}")
            st.write(f"📅 Deadline : {task[2]}")
            st.write(f"⏱ Duration : {task[3]} mins")

            if st.button("✅ Mark as Completed", key=f"complete_{task[0]}"):

                cursor.execute(
                    "UPDATE tasks SET status='Completed' WHERE id=?",
                    (task[0],)
                )

                conn.commit()

                st.success("✅ Task marked as completed!")

                st.rerun()

conn.close()

st.markdown("---")

# ==========================
# Today's Status
# ==========================

st.markdown("## 🤖 AI Planner")

if total_tasks == 0:
    st.success("No tasks scheduled today.")
else:
    st.info("Generate your AI schedule to analyse today's workload.")

if st.button("🧠 Generate My Day"):

    conn = sqlite3.connect("database/tasks.db")
    cursor = conn.cursor()

    current_time = datetime.now().strftime("%I:%M %p")

    # Today's Commitments
    cursor.execute("""
    SELECT title,start_time,end_time
    FROM commitments
    WHERE date=?
    ORDER BY start_time
    """, (str(date.today()),))

    commitments = cursor.fetchall()

    # Pending Tasks
    cursor.execute("""
    SELECT task_name,deadline,duration,category
    FROM tasks
    WHERE status='Pending'
    ORDER BY deadline
    """)

    tasks = cursor.fetchall()

    conn.close()

    commitment_text = ""

    if commitments:

        for c in commitments:

            commitment_text += f"""
{c[0]}
{c[1]} - {c[2]}

"""

    else:

        commitment_text = "No commitments today."

    task_text = ""

    for t in tasks:

        task_text += f"""
Task : {t[0]}
Deadline : {t[1]}
Duration : {t[2]} minutes
Category : {t[3]}

"""

    prompt = f"""

Current Time

{current_time}

Today's Commitments

{commitment_text}

Pending Tasks

{task_text}

"""

    with st.spinner("🤖 DeadlineAI is creating today's schedule..."):

        result = generate_schedule(prompt)

    st.markdown("---")

    st.subheader("🧠 Today's AI Plan")

    st.markdown(result)