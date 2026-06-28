import streamlit as st
import sqlite3
from datetime import date

st.set_page_config(page_title="Today's Commitments", page_icon="📅")

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

/* ================= Background ================= */

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

[data-testid="stSidebarNav"] a{
    border-radius:14px;
    padding:12px 16px;
    margin-bottom:8px;
}

[data-testid="stSidebarNav"] a:hover{
    background:linear-gradient(
        90deg,
        rgba(139,92,246,.30),
        rgba(37,99,235,.30)
    );
}

/* ================= Titles ================= */

h1,h2,h3{
    color:white;
}

/* ================= Inputs ================= */

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div{

    background:#131B35;
    color:white;
    border:1px solid #243153;
    border-radius:12px;

}

/* ================= Buttons ================= */

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

/* ================= Containers ================= */

div[data-testid="stVerticalBlock"] > div{

    background:#131B35;
    border:1px solid #243153;
    border-radius:15px;
    padding:15px;

}

div[data-testid="stAlert"]{
    border-radius:12px;
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
<h1 style="text-align:center;">
<span style="color:white;">Today's</span>
<span style="color:#8B5CF6;">Commitments</span>
</h1>
""", unsafe_allow_html=True)

option = st.radio(
    "Choose an option",
    ["➕ Add Commitment", "📋 Manage Commitments"],
    horizontal=True
)

if option == "➕ Add Commitment":

    title = st.text_input("Commitment Name")

    col1, col2 = st.columns(2)

    with col1:
        start_time = st.time_input("Start Time")

    with col2:
        end_time = st.time_input("End Time")

    category = st.selectbox(
        "Category",
        [
            "College",
            "Office",
            "Meeting",
            "Travel",
            "Personal",
            "Other"
        ]
    )

    if st.button("Save Commitment"):

        if title.strip() == "":
            st.error("Please enter a commitment name.")

        else:

            conn = sqlite3.connect("database/tasks.db")
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO commitments
            (title, start_time, end_time, category, date)
            VALUES (?, ?, ?, ?, ?)
            """, (
                title,
                str(start_time),
                str(end_time),
                category,
                str(date.today())
            ))

            conn.commit()
            conn.close()

            st.success("✅ Commitment Saved")

if option == "📋 Manage Commitments":

    st.subheader("📋 Existing Commitments")

    conn = sqlite3.connect("database/tasks.db")
    cursor = conn.cursor()

    if "edit_commitment_id" not in st.session_state:
        st.session_state.edit_commitment_id = None

    cursor.execute("""
        SELECT id, title, start_time, end_time, category
        FROM commitments
        ORDER BY start_time
    """)

    commitments = cursor.fetchall()

    # ==========================
    # EDIT COMMITMENT
    # ==========================

    if st.session_state.edit_commitment_id is not None:

        cursor.execute("""
            SELECT title,start_time,end_time,category
            FROM commitments
            WHERE id=?
        """, (st.session_state.edit_commitment_id,))

        commitment = cursor.fetchone()

        st.markdown("## ✏ Edit Commitment")

        new_title = st.text_input(
            "Commitment Name",
            value=commitment[0]
        )

        new_start = st.text_input(
            "Start Time",
            value=commitment[1]
        )

        new_end = st.text_input(
            "End Time",
            value=commitment[2]
        )

        categories = [
            "College",
            "Office",
            "Meeting",
            "Travel",
            "Personal",
            "Other"
        ]

        new_category = st.selectbox(
            "Category",
            categories,
            index=categories.index(commitment[3])
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("💾 Update Commitment"):

                cursor.execute("""
                    UPDATE commitments
                    SET title=?,
                        start_time=?,
                        end_time=?,
                        category=?
                    WHERE id=?
                """, (
                    new_title,
                    new_start,
                    new_end,
                    new_category,
                    st.session_state.edit_commitment_id
                ))

                conn.commit()

                st.session_state.edit_commitment_id = None

                st.success("✅ Commitment Updated!")

                st.rerun()

        with col2:

            if st.button("Cancel"):

                st.session_state.edit_commitment_id = None

                st.rerun()

        st.markdown("---")

    # ==========================
    # LIST COMMITMENTS
    # ==========================

    if len(commitments) == 0:

        st.info("No commitments found.")

    else:

        for commitment in commitments:

            with st.container(border=True):

                st.write(f"### 📅 {commitment[1]}")
                st.write(f"🕒 {commitment[2]} - {commitment[3]}")
                st.write(f"📂 Category : {commitment[4]}")

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✏ Edit",
                        key=f"edit_commitment_{commitment[0]}"
                    ):

                        st.session_state.edit_commitment_id = commitment[0]

                        st.rerun()

                with col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_commitment_{commitment[0]}"
                    ):

                        cursor.execute(
                            "DELETE FROM commitments WHERE id=?",
                            (commitment[0],)
                        )

                        conn.commit()

                        st.success("✅ Commitment Deleted!")

                        st.rerun()

    conn.close()