import streamlit as st
import sqlite3

st.set_page_config(page_title="Add Task", page_icon="➕")
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

/* Background */
.stApp{
    background:linear-gradient(
        180deg,
        #090F1F 0%,
        #101B3D 50%,
        #090F1F 100%
    );
}

/* ================= Sidebar ================= */

[data-testid="stSidebar"]{
    background:linear-gradient(
        180deg,
        #090F1F 0%,
        #101B3D 50%,
        #090F1F 100%
    );
    border-right:1px solid #243153;
}

[data-testid="stSidebar"] *{
    color:white;
}

[data-testid="stSidebarNav"]{
    padding-top:15px;
}

[data-testid="stSidebarNav"] a{

    border-radius:14px;
    padding:12px 16px;
    margin-bottom:8px;
    color:white;
    transition:.3s;

}

[data-testid="stSidebarNav"] a:hover{

    background:linear-gradient(
        90deg,
        rgba(139,92,246,.30),
        rgba(37,99,235,.30)
    );

}

[data-testid="stSidebarNav"] a[aria-current="page"]{

    background:linear-gradient(
        90deg,
        #8B5CF6,
        #2563EB
    );

    color:white;
    font-weight:bold;

}

/* Titles */
h1,h2,h3{
    color:white;
}

/* Input Boxes */
.stTextInput input,
.stTextArea textarea,
.stDateInput input,
.stNumberInput input,
.stSelectbox div{

    background:#131B35;
    color:white;
    border:1px solid #243153;
    border-radius:12px;

}

/* Buttons */
.stButton > button{

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

.stButton > button:hover{

    background:linear-gradient(
        90deg,
        #7C3AED,
        #1D4ED8
    );

}

/* Containers */
div[data-testid="stVerticalBlock"] > div{

    background:#131B35;
    border:1px solid #243153;
    border-radius:15px;
    padding:15px;

}

/* Alerts */

div[data-testid="stAlert"]{

    border-radius:12px;

}

/* Divider */

hr{

    border:1px solid #243153;

}

</style>
""", unsafe_allow_html=True)
st.title("➕ Add New Task")

option = st.radio(
    "Choose an option",
    ["➕ Add New Task", "📋 Manage Existing Tasks"],
    horizontal=True
)

if option == "➕ Add New Task":

    task = st.text_input("Task Name")
    description = st.text_area("Description")
    deadline = st.date_input("Deadline")

    duration = st.number_input(
        "Estimated Duration (minutes)",
        min_value=15,
        max_value=600,
        step=15
    )

    category = st.selectbox(
        "Category",
        ["Assignment", "Exam", "Meeting", "Personal", "Work", "Other"]
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("Save Task"):

        if task.strip() == "":
            st.error("Task Name cannot be empty!")

        else:
            conn = sqlite3.connect("database/tasks.db")
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO tasks
            (task_name, description, deadline, duration, category, difficulty)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                task,
                description,
                str(deadline),
                duration,
                category,
                difficulty
            ))

            conn.commit()
            conn.close()

            st.success("✅ Task Saved Successfully!")
if option == "📋 Manage Existing Tasks":

    st.subheader("📋 Existing Tasks")

    conn = sqlite3.connect("database/tasks.db")
    cursor = conn.cursor()

    # If an edit button was clicked previously
    if "edit_task_id" not in st.session_state:
        st.session_state.edit_task_id = None

    cursor.execute("""
        SELECT id, task_name, description, deadline,
               duration, category, difficulty
        FROM tasks
        ORDER BY deadline
    """)

    tasks = cursor.fetchall()

    # ==========================
    # EDIT FORM
    # ==========================

    if st.session_state.edit_task_id is not None:

        cursor.execute("""
            SELECT task_name, description, deadline,
                   duration, category, difficulty
            FROM tasks
            WHERE id=?
        """, (st.session_state.edit_task_id,))

        task = cursor.fetchone()

        st.markdown("## ✏ Edit Task")

        new_name = st.text_input("Task Name", value=task[0])
        new_description = st.text_area("Description", value=task[1])
        new_deadline = st.date_input("Deadline", value=task[2])
        new_duration = st.number_input(
            "Duration (minutes)",
            min_value=15,
            max_value=600,
            step=15,
            value=task[3]
        )

        categories = [
            "Assignment",
            "Exam",
            "Meeting",
            "Personal",
            "Work",
            "Other"
        ]

        difficulties = [
            "Easy",
            "Medium",
            "Hard"
        ]

        new_category = st.selectbox(
            "Category",
            categories,
            index=categories.index(task[4])
        )

        new_difficulty = st.selectbox(
            "Difficulty",
            difficulties,
            index=difficulties.index(task[5])
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("💾 Update Task"):

                cursor.execute("""
                    UPDATE tasks
                    SET task_name=?,
                        description=?,
                        deadline=?,
                        duration=?,
                        category=?,
                        difficulty=?
                    WHERE id=?
                """, (
                    new_name,
                    new_description,
                    str(new_deadline),
                    new_duration,
                    new_category,
                    new_difficulty,
                    st.session_state.edit_task_id
                ))

                conn.commit()

                st.session_state.edit_task_id = None

                st.success("✅ Task Updated Successfully!")

                st.rerun()

        with col2:

            if st.button("Cancel"):

                st.session_state.edit_task_id = None

                st.rerun()

        st.markdown("---")

    # ==========================
    # TASK LIST
    # ==========================

    if len(tasks) == 0:

        st.info("No tasks found.")

    else:

        for task in tasks:

            with st.container(border=True):

                st.write(f"### 📘 {task[1]}")
                st.write(f"📅 Deadline : {task[3]}")
                st.write(f"⏱ Duration : {task[4]} mins")
                st.write(f"📂 Category : {task[5]}")
                st.write(f"🎯 Difficulty : {task[6]}")

                col1, col2 = st.columns(2)

                with col1:

                    if st.button("✏ Edit", key=f"edit_{task[0]}"):

                        st.session_state.edit_task_id = task[0]

                        st.rerun()

                with col2:

                    if st.button("🗑 Delete", key=f"delete_{task[0]}"):

                        cursor.execute(
                            "DELETE FROM tasks WHERE id=?",
                            (task[0],)
                        )

                        conn.commit()

                        st.success("✅ Task Deleted Successfully!")

                        st.rerun()

    conn.close()