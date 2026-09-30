# gui/roster_pages.py
#==========================
# Daily roster and student check in GUI
#==============================

import streamlit as st
import pandas as pd


#Roster check in page view 

def show_roster_page(manager):
    """Renders the daily roster and check-in functionality."""
    st.header("Daily Roster & Check-In")

    # --- View Roster Section ---
    st.subheader("Daily Schedule")
    day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    
    # filter courses and lessons scheduled for the selected weekday
    scheduled_courses = []
    for course in manager.courses:
        day_lessons = [l for l in course.lessons if l.get("day", "").lower() == day.lower()]
        if day_lessons:
            #lookup teacher if available 
            teacher = manager.find_teacher_by_id(course.teacher_id) if hasattr(manager, 'find_teacher_by_id') else None
            teacher_name = teacher.name if teacher else "Unassigned"
            
            for lesson in day_lessons:
                scheduled_courses.append({
                    "Course Name": course.name,
                    "Instrument": course.instrument,
                    "Teacher": teacher_name,
                    "Time": lesson.get("time", "N/A"),
                    "Enrolled Students": len(course.enrolled_student_ids)
                })
    #print as a nice table using pandas dataframe
    if scheduled_courses:
        df = pd.DataFrame(scheduled_courses)
        st.dataframe(df, use_container_width=True)
    else:
        st.info(f"No classes scheduled for {day}.")

    st.divider()
    
    # --- Student Check-in Section ---
    #handles loggin in attendace
    st.subheader("Student Check in")
    
    if not manager.students or not manager.courses:
        st.warning(" ensure students and courses exist before performing check ins.")
        return

    # Populating dropdown selections mapping display names to integer IDs
    student_list = {s.name: s.id for s in manager.students}
    course_list = {c.name: c.id for c in manager.courses}

    with st.form("check_in_form"):
        selected_student_name = st.selectbox("Select Student", list(student_list.keys()))
        selected_course_name = st.selectbox("Select Course", list(course_list.keys()))
        
        submitted = st.form_submit_button("Check-in Student")

        if submitted:
            #grab integer ID back from chosen dropdown name
            student_id = student_list[selected_student_name]
            course_id = course_list[selected_course_name]

            # run check in method from schedule manager
            success = manager.check_in(student_id, course_id)

            if success:
                st.success(f"Checked in {selected_student_name} for {selected_course_name}!")
                st.balloons()
            else:
                st.error("Check-in failed. Please verify student enrollment and course assignment.")