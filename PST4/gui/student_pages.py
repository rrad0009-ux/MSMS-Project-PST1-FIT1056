# gui/student_pages.py
#==========================
# Student management GUI page view
#==============================

# handles student search, registration, enrolments, swaps, edits, and ID card printing

import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # tabs to group student tasks
    tab1, tab2, tab3, tab4 = st.tabs(["Directory & Registration", "Enrol & Switch Courses", "Update / Remove", "Print ID Badge"])

    # ---Search & Registration ---
    with tab1:
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

        st.subheader("Register New Student") #streamlit creates typing in input boxes (form batch block )
        with st.form("registration_form"):
            reg_name = st.text_input("New Student Name")
            reg_instrument = st.text_input("First Instrument")
            submitted = st.form_submit_button("Register Student")
            
            if submitted: #maintains input validation (guardrail for fields not being blank)
                if reg_name.strip() and reg_instrument.strip():
                    new_student = manager.register_student(reg_name.strip())
                    if new_student:
                        st.success(f"Successfully registered {new_student.name} with ID {new_student.id}!")
                        st.balloons()
                    else:
                        st.error("Could not register student. Please check inputs.")
                else:
                    st.warning("Please enter both a name and an instrument.")

    # --- Course Operations ---
    with tab2:
        st.subheader("Course Operations")
        if not manager.students or not manager.courses:
            st.warning("Ensure both students and courses exist before managing enrolments.")
        else:
            student_map = {f"{s.name} (ID: {s.id})": s.id for s in manager.students}
            course_map = {f"{c.name} (ID: {c.id})": c.id for c in manager.courses}

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("##### Enrol in Course")
                selected_s = st.selectbox("Select Student", list(student_map.keys()), key="enrol_s")
                selected_c = st.selectbox("Select Course to Add", list(course_map.keys()), key="enrol_c")
                if st.button("Enrol Student"):
                    sid = student_map[selected_s]
                    cid = course_map[selected_c]
                    if manager.enrol_student(sid, cid):
                        st.success(f"Enrolled {selected_s} into course!")
                    else:
                        st.info("Student already enrolled or invalid selection.")

            with col2:
                st.markdown("##### Switch Course")
                selected_s2 = st.selectbox("Select Student", list(student_map.keys()), key="swap_s")
                from_c = st.selectbox("Current Course", list(course_map.keys()), key="swap_from")
                to_c = st.selectbox("Target Course", list(course_map.keys()), key="swap_to")
                if st.button("Switch Course"):
                    sid = student_map[selected_s2]
                    f_cid = course_map[from_c]
                    t_cid = course_map[to_c]
                    if manager.switch_course(sid, f_cid, t_cid):
                        st.success("Successfully swapped course!")
                    else:
                        st.error("Course switch failed. Verify student enrolment.")

    # ---Update / Remove Student ---
    with tab3:
        st.subheader("Manage Student Records")
        if not manager.students:
            st.warning("No students available.")
        else:
            student_map = {f"{s.name} (ID: {s.id})": s.id for s in manager.students}
            selected_s = st.selectbox("Select Student", list(student_map.keys()), key="mgr_s")

            with st.form("update_s_form"):
                new_name = st.text_input("New Name")
                if st.form_submit_button("Update Name"):
                    sid = student_map[selected_s]
                    if manager.update_student(sid, name=new_name.strip()):
                        st.success("Student updated successfully!")

            st.divider()

            if st.button("Remove Student Record", type="primary"):
                sid = student_map[selected_s]
                if manager.remove_student(sid):
                    st.success("Student removed successfully!")

    # --- Print ID Badge ---
    with tab4:
        st.subheader("Print Physical Student Card")
        if not manager.students:
            st.warning("No students available.")
        else:
            student_map = {f"{s.name} (ID: {s.id})": s.id for s in manager.students}
            card_student = st.selectbox("Select Student for ID Card", list(student_map.keys()))
            
            if st.button("Generate ID Badge File"):
                sid = student_map[card_student]
                filename = manager.print_student_card(sid)
                if filename:
                    st.success(f"Printed student card to text file: `{filename}`!")
                else:
                    st.error("Could not generate student card.")