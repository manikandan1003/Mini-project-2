


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import mysql.connector

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Placement Dashboard", layout="wide")

# -------------------- IMAGE HEADER --------------------
img = Image.open("C:\\Users\\User\\Pictures\\2023-03-08\\unnamed.jpg")
resized_img = img.resize((700, 300))
st.image(resized_img)
st.markdown("<h1 style='color: red;'>PLACEMENT ELIGIBILITY</h1>", unsafe_allow_html=True)

# -------------------- SIDEBAR NAVIGATION --------------------
st.sidebar.title("🔽 Navigation")
section = st.sidebar.radio("Go to", ["📂 Student Placement Details", "🔍 Student Info", "📘 Questions"])

# -------------------- MYSQL CONNECTION FUNCTIONS --------------------
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="mani",
            password="1234",
            database="student_perfomance"
        )
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

def fetch_data(query):
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(query)
            return pd.DataFrame(cur.fetchall())
        finally:
            conn.close()
    return pd.DataFrame()

def get_student_info(student_id):
    conn = create_connection()
    if conn:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM student_performance WHERE student_id = %s", (student_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result
    return None

# -------------------- SECTION: STUDENT PLACEMENT DETAILS --------------------
if section == "📂 Student Placement Details":
    st.title("📂 Student Placement Details")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.session_state.df = df
            st.success("✅ File uploaded successfully!")
            st.dataframe(df)

            # Metrics
            st.header("📊 Placement Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Avg. Age", round(df["age"].mean(), 1))
            col2.metric("Avg. Mock Interview", round(df["mock_interview_score"].mean(), 1))
            col3.metric("Avg. Package", f"{round(df['placement_package'].mean(), 2)} LPA")

            # Gender Distribution
            st.subheader("📈 Gender Distribution")
            gender_data = df['gender'].value_counts().reset_index()
            gender_data.columns = ['gender', 'count']
            fig, ax = plt.subplots()
            ax.pie(gender_data['count'], labels=gender_data['gender'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

            # Recent Records
            st.subheader("🧾 Recent Students (Top 10)")
            sort_column = 'enrollment_year' if 'enrollment_year' in df.columns else df.columns[0]
            st.dataframe(df.sort_values(by=sort_column, ascending=False).head(10))

        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
    else:
        st.info("📤 Please upload an Excel file to view placement data.")

# -------------------- SECTION: STUDENT INFO --------------------
elif section == "🔍 Student Info":
    st.title("🔍 Student Information Viewer")
    student_id_input = st.text_input("Enter Student ID")

    if st.button("🔎 Get Student Info"):
        if not student_id_input.strip().isdigit():
            st.error("❌ Enter a valid numeric Student ID.")
        else:
            info = get_student_info(student_id_input)
            if info:
                st.success(f"✅ Found: {info['name']}")
                st.subheader("📋 Basic Info")
                st.markdown(f"""
                - **Age:** {info['age']}
                - **Gender:** {info['gender']}
                - **City:** {info['city']}
                - **Batch:** {info['course_batch']}
                - **Graduation:** {info['graduation_year']}
                """)
                st.subheader("📊 Performance")
                st.markdown(f"""
                - **Problems Solved:** {info['problems_solved']}
                - **Certifications:** {info['certifications_earned']}
                - **Mock Interview Score:** {info['mock_interview_score']}
                - **Placement Status:** {info['placement_status']}
                - **Company:** {info['company_name']}
                - **Package:** ₹{info['placement_package'] or 0}
                """)
                with st.expander("🗂 Full Record"):
                    st.json(info)
            else:
                st.warning("⚠️ No student found with that ID.")

# -------------------- SECTION: QUESTIONS --------------------
elif section == "📘 Questions":
    st.title("📘 SQL-Based Analysis")

    st.subheader("Medium Level Queries")
    medium_queries = {
        "Count Total Students": "SELECT COUNT(*) AS total_students FROM student_performance",
        "Group by Placement Status": "SELECT placement_status, COUNT(*) AS total FROM student_performance GROUP BY placement_status",
        "City with Highest Placements": "SELECT city, COUNT(*) AS placement_count FROM student_performance WHERE placement_status = 'Placed' GROUP BY city ORDER BY placement_count DESC LIMIT 1",
        "Average Placement Package": "SELECT ROUND(AVG(placement_package), 2) AS avg_package FROM student_performance WHERE placement_package > 0",
        "Count Students per Graduation Year": "SELECT graduation_year, COUNT(*) AS total_students FROM student_performance GROUP BY graduation_year ORDER BY graduation_year",
        "Count Placed Students by Gender": "SELECT gender, COUNT(*) AS placed_count FROM student_performance WHERE placement_status = 'Placed' GROUP BY gender"
    }

    selected_medium = st.selectbox("Choose a Medium Query", list(medium_queries.keys()))
    if st.button("▶️ Run Medium Query"):
        df_result = fetch_data(medium_queries[selected_medium])
        if df_result.shape == (1, 1):
            st.metric(label=selected_medium, value=float(df_result.iloc[0, 0]))
        else:
            st.dataframe(df_result)

    st.subheader("🎓 Complex Queries")
    complex_queries = {
        "Average Certifications of Placed Students": """
            SELECT ROUND(AVG(certifications_earned), 2) AS avg_certifications
            FROM student_performance WHERE placement_status = 'Placed'
        """,
        "Average Latest Project Score per Course Batch": """
            SELECT course_batch, ROUND(AVG(latest_project_score), 2) AS avg_project_score
            FROM student_performance GROUP BY course_batch ORDER BY avg_project_score DESC
        """,
        "Average Mock Interview Score": """
            SELECT ROUND(AVG(mock_interview_score), 2) AS avg_mock_score
            FROM student_performance
        """,
        "Count of Not Placed Students by Gender": """
            SELECT gender, COUNT(*) AS not_placed_count
            FROM student_performance WHERE placement_status != 'Placed' GROUP BY gender
        """
    }

    selected_complex = st.selectbox("Choose a Complex Query", list(complex_queries.keys()))
    if st.button("▶️ Run Complex Query"):
        df_complex = fetch_data(complex_queries[selected_complex])
        if df_complex.shape == (1, 1):
            st.metric(label=selected_complex, value=float(df_complex.iloc[0, 0]))
        else:
            st.dataframe(df_complex)


