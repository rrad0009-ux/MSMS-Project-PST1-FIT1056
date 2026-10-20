# gui/student_pages.py
#==========================================
# STUDENT MANAGEMENT GUI PAGE VIEW
#==========================================

# handles student search directory, registration, enrolments, edits, and badge printing

import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Directory & Search", 
        "Enrol & Switch Courses", 
        "Edit Student", 
        "Remove Student", 
        "Print ID Badge"
    ])

    # --- TAB 1: DIRECTORY & SEARCH ---
    with tab1:
        st.subheader("Find a Student")
        search_term = st.text_input("Enter student name or ID to search")
        
        if search_term:
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

        st.subheader("Register New Student")

        # Display persistent registration success message if present in session state
        if "reg_success_msg" in st.session_state:
            st.success(st.session_state["reg_success_msg"])
            # Remove message after rendering so it won't persist indefinitely
            del st.session_state["reg_success_msg"]

        with st.form("registration_form"):
            reg_name = st.text_input("New Student Name")
            reg_instrument = st.text_input("First Instrument")
            submitted = st.form_submit_button("Register Student")
            
            if submitted:
                if reg_name.strip() and reg_instrument.strip():
                    new_student = manager.register_student(reg_name.strip())
                    if new_student:
                        # Save success message into session state so it survives st.rerun()
                        st.session_state["reg_success_msg"] = f"Registration Successful! Registered {new_student.name} with ID: {new_student.id}"
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Could not register student. Please check inputs.")
                else:
                    st.warning("Please enter both a name and an instrument.")

    # --- TAB 2: ENROL & SWITCH COURSES ---
    with tab2:
        st.subheader("Course Enrolment & Switching")
        
        if manager.students and manager.courses:
            student_options = {f"{s.name} (ID: {s.id})": s.id for s in manager.students}
            course_options = {f"{c.name} - {c.instrument} (ID: {c.id})": c.id for c in manager.courses}
            
            col_enrol, col_switch = st.columns(2)
            
            with col_enrol:
                st.write("**Enrol Student into Course**")
                with st.form("enrol_form"):
                    selected_student_label = st.selectbox("Select Student", list(student_options.keys()), key="enrol_stu")
                    selected_course_label = st.selectbox("Select Course to Enrol", list(course_options.keys()), key="enrol_crs")
                    
                    enrol_submitted = st.form_submit_button("Enrol Student")
                    if enrol_submitted:
                        stu_id = student_options[selected_student_label]
                        crs_id = course_options[selected_course_label]
                        
                        student = manager.find_student_by_id(stu_id)
                        course = manager.find_course_by_id(crs_id)
                        
                        if crs_id not in student.enrolled_course_ids:
                            student.enrolled_course_ids.append(crs_id)
                        if stu_id not in course.enrolled_student_ids:
                            course.enrolled_student_ids.append(stu_id)
                            
                        manager._save_data()
                        st.session_state["reg_success_msg"] = f"Enrolled {student.name} into {course.name}!"
                        st.rerun()

            with col_switch:
                st.write("**Switch Course**")
                with st.form("switch_form"):
                    switch_student_label = st.selectbox("Select Student", list(student_options.keys()), key="sw_stu")
                    from_course_label = st.selectbox("From Course", list(course_options.keys()), key="sw_from")
                    to_course_label = st.selectbox("To Course", list(course_options.keys()), key="sw_to")
                    
                    switch_submitted = st.form_submit_button("Switch Course")
                    if switch_submitted:
                        s_id = student_options[switch_student_label]
                        from_c_id = course_options[from_course_label]
                        to_c_id = course_options[to_course_label]
                        
                        student = manager.find_student_by_id(s_id)
                        old_c = manager.find_course_by_id(from_c_id)
                        new_c = manager.find_course_by_id(to_c_id)
                        
                        if from_c_id in student.enrolled_course_ids:
                            student.enrolled_course_ids.remove(from_c_id)
                        if s_id in old_c.enrolled_student_ids:
                            old_c.enrolled_student_ids.remove(s_id)
                            
                        if to_c_id not in student.enrolled_course_ids:
                            student.enrolled_course_ids.append(to_c_id)
                        if s_id not in new_c.enrolled_student_ids:
                            new_c.enrolled_student_ids.append(s_id)
                            
                        manager._save_data()
                        st.session_state["reg_success_msg"] = f"Moved {student.name} from {old_c.name} to {new_c.name}!"
                        st.rerun()
        else:
            st.info("Requires registered students and active courses.")

    # --- TAB 3: EDIT STUDENT ---
    with tab3:
        st.subheader("Edit Student Details")
        if manager.students:
            student_options = {f"{s.name} (ID: {s.id})": s.id for s in manager.students}
            edit_student_label = st.selectbox("Select Student to Edit", list(student_options.keys()))
            target_student_id = student_options[edit_student_label]
            
            target_student = manager.find_student_by_id(target_student_id)
            with st.form("edit_student_form"):
                new_name = st.text_input("Updated Student Name", value=target_student.name)
                save_edit = st.form_submit_button("Save Changes")
                if save_edit:
                    if new_name.strip():
                        target_student.name = new_name.strip()
                        manager._save_data()
                        st.session_state["reg_success_msg"] = "Student details updated successfully!"
                        st.rerun()
                    else:
                        st.warning("Student name cannot be empty.")
        else:
            st.info("No students registered yet.")

    # --- TAB 4: REMOVE STUDENT ---
    with tab4:
        st.subheader("Remove Student Record")
        if manager.students:
            student_options = {f"{s.name} (ID: {s.id})": s.id for s in manager.students}
            remove_student_label = st.selectbox("Select Student to Remove", list(student_options.keys()))
            rem_student_id = student_options[remove_student_label]
            
            with st.form("remove_student_form"):
                st.warning("Action cannot be undone. Removes student from system and courses.")
                confirm_remove = st.form_submit_button("Remove Student")
                if confirm_remove:
                    student_to_rem = manager.find_student_by_id(rem_student_id)
                    if student_to_rem:
                        manager.students.remove(student_to_rem)
                        for course in manager.courses:
                            if rem_student_id in course.enrolled_student_ids:
                                course.enrolled_student_ids.remove(rem_student_id)
                        manager._save_data()
                        st.session_state["reg_success_msg"] = f"Removed Student ID {rem_student_id}."
                        st.rerun()
        else:
            st.info("No students registered yet.")

    # --- TAB 5: PRINT ID BADGE ---
    with tab5:
        st.subheader("Print Student ID Badge")
        if manager.students:
            student_options = {f"{s.name} (ID: {s.id})": s.id for s in manager.students}
            badge_student_label = st.selectbox("Select Student for Badge", list(student_options.keys()))
            badge_student_id = student_options[badge_student_label]
            
            if st.button("Generate ID Badge File"):
                student = manager.find_student_by_id(badge_student_id)
                if student:
                    filename = f"{student.id}_card.txt"
                    course_names = [manager.find_course_by_id(cid).name for cid in student.enrolled_course_ids if manager.find_course_by_id(cid)]
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("========================\n")
                        f.write("  MUSIC SCHOOL ID BADGE\n")
                        f.write("========================\n")
                        f.write(f"ID: {student.id}\n")
                        f.write(f"Name: {student.name}\n")
                        f.write(f"Enrolled In: {', '.join(course_names) if course_names else 'None'}\n")
                    st.success(f"Exported ID Badge file to `{filename}`!")
        else:
            st.info("No students registered yet.")
            