
# to run this->
# python -m streamlit run C:\Users\lenovo\Desktop\data\python\project.py
import streamlit as st
import pandas as pd

class Student:
    def __init__(self):
        self.students = {}

    def add_student(self, id, name, age, course, mobile, email):
        if id in self.students:
            return False  # Already exists
        self.students[id] = {
            'Name': name,
            'Age': age,
            'Course': course,
            'Mobile': mobile,
            'Email': email
        }
        return True

    def delete_student(self, id):
        if id in self.students:
            del self.students[id]
            return True
        return False

    def get_all_students(self):
        return pd.DataFrame.from_dict(self.students, orient='index').reset_index().rename(columns={'index': 'Student ID'})

    def search_student(self, keyword):
        results = []
        if keyword.isdigit():
            sid = int(keyword)
            if sid in self.students:
                student = self.students[sid].copy()
                student["Student ID"] = sid
                results.append(student)
        else:
            for sid, info in self.students.items():
                if keyword.lower() == info["Course"].lower():
                    student = info.copy()
                    student["Student ID"] = sid
                    results.append(student)
        return pd.DataFrame(results)

    def count_students(self):
        return len(self.students)

# Initialize student object in session_state
if 'student_obj' not in st.session_state:
    st.session_state.student_obj = Student()

st.title("🎓 Student Management System")

menu = st.sidebar.radio("Choose Action", ["Add Student", "Delete Student", "Show All Students", "Search Student", "Count Students"])

student_obj = st.session_state.student_obj

# Add Student
if menu == "Add Student":
    st.header("➕ Add New Student")
    with st.form("add_form"):
        id = st.number_input("Student ID", min_value=1, format="%d")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, format="%d")
        course = st.text_input("Course")
        mobile = st.text_input("Mobile")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add Student")

        if submitted:
            success = student_obj.add_student(id, name, age, course, mobile, email)
            if success:
                st.success("✅ Student added successfully!")
            else:
                st.error("❌ Student with this ID already exists.")

# Delete Student
elif menu == "Delete Student":
    st.header("🗑️ Delete Student")
    del_id = st.number_input("Enter Student ID to delete", min_value=1, format="%d")
    if st.button("Delete"):
        if student_obj.delete_student(del_id):
            st.success("✅ Student deleted successfully.")
        else:
            st.error("❌ Student ID not found.")

# Show All Students
elif menu == "Show All Students":
    st.header("📋 All Student Records")
    df = student_obj.get_all_students()
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No student records found.")

# Search Student
elif menu == "Search Student":
    st.header("🔍 Search Student")
    keyword = st.text_input("Enter Student ID or Course Name")
    if st.button("Search"):
        result_df = student_obj.search_student(keyword)
        if not result_df.empty:
            st.dataframe(result_df)
        else:
            st.warning("No matching students found.")

# Count Students
elif menu == "Count Students":
    st.header("🔢 Total Students")
    count = student_obj.count_students()
    st.info(f"📚 Total Students: {count}")
