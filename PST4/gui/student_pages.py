# gui/student_pages.py
import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Search Section (remains the same) ---
    st.subheader("Find a Student")
    search_term = st.text_input("Enter student name or ID to search")
    if search_term: #performs case insensitive search across studentuser objects 
        results = [
            s for s in manager.students 
            if search_term.lower() in s.name.lower() or str(s.id) == search_term.strip()
        ]
        if results:
            st.write(f"Found {len(results)} matching student(s):")
            for student in results:
                st.write(f"- **ID:** {student.id} | **Name:** {student.name} | **Enrolled Courses:** {student.enrolled_course_ids}")
        else:
            st.info("No matching students found.")

    st.divider()

    # --- Registration Section (now works correctly) ---
    st.subheader("Register New Student")  #streamlit creates typing in input boxes (form batch block )
    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name")
        reg_instrument = st.text_input("First Instrument")
        submitted = st.form_submit_button("Register Student")
        
        if submitted: #maintains input validation (guardrail for fields not being blank)
            if reg_name.strip() and reg_instrument.strip():
                # Call ScheduleManager to register student
                new_student = manager.register_student(reg_name.strip())
                if new_student:
                    st.success(f"Successfully registered {new_student.name} with ID {new_student.id}!")
                    st.balloons()
                else:
                    st.error("Could not register student. Please check inputs.")
            else:
                st.warning("Please enter both a name and an instrument.")