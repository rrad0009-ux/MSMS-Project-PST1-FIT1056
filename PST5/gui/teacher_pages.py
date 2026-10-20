# gui/teacher_pages.py
#==========================================
# TEACHER MANAGEMENT GUI PAGE VIEW
#==========================================

import streamlit as st

def show_teacher_management_page(manager):
    """Renders all components for the teacher management page."""
    st.header("Teacher Management")

    tab1, tab2, tab3, tab4 = st.tabs(["Directory & Search", "Add Teacher", "Update Teacher", "Remove Teacher"])

    # --- TAB 1: DIRECTORY & SEARCH ---
    with tab1:
        st.subheader("Teacher Directory")
        search_term = st.text_input("Search teachers by name or speciality", key="teacher_search")
        
        teachers_to_show = manager.teachers
        if search_term:
            term_lower = search_term.lower()
            teachers_to_show = [
                t for t in manager.teachers 
                if term_lower in t.name.lower() or term_lower in t.speciality.lower() or str(t.id) == search_term.strip()
            ]

        if teachers_to_show:
            teacher_data = [{"ID": t.id, "Name": t.name, "Speciality": t.speciality} for t in teachers_to_show]
            st.dataframe(teacher_data, use_container_width=True)
        else:
            st.info("No matching teachers found.")

    # --- TAB 2: ADD TEACHER ---
    with tab2:
        st.subheader("Add New Teacher")
        with st.form("add_teacher_form"):
            t_name = st.text_input("Teacher Name")
            t_spec = st.text_input("Speciality (e.g., Piano, Violin)")
            submit_add = st.form_submit_button("Add Teacher")

            if submit_add:
                if t_name.strip() and t_spec.strip():
                    new_teacher = manager.add_teacher(t_name.strip(), t_spec.strip())
                    st.success(f"Successfully added Teacher '{t_name}' with ID {new_teacher.id}!")
                    st.rerun()
                else:
                    st.warning("Please enter both teacher name and speciality.")

    # --- TAB 3: UPDATE TEACHER ---
    with tab3:
        st.subheader("Update Teacher Profile")
        if manager.teachers:
            t_options = {f"{t.name} (ID: {t.id})": t.id for t in manager.teachers}
            selected_t_label = st.selectbox("Select Teacher to Update", list(t_options.keys()))
            selected_t_id = t_options[selected_t_label]

            with st.form("update_teacher_form"):
                new_t_name = st.text_input("New Name (leave blank to skip)")
                new_t_spec = st.text_input("New Speciality (leave blank to skip)")
                submit_update = st.form_submit_button("Update Teacher")

                if submit_update:
                    updates = {}
                    if new_t_name.strip():
                        updates['name'] = new_t_name.strip()
                    if new_t_spec.strip():
                        updates['speciality'] = new_t_spec.strip()

                    if updates:
                        manager.update_teacher(selected_t_id, **updates)
                        st.success(f"Teacher ID {selected_t_id} updated successfully!")
                        st.rerun()
                    else:
                        st.info("No new details provided.")
        else:
            st.info("No teachers available to update.")

    # --- TAB 4: REMOVE TEACHER ---
    with tab4:
        st.subheader("Remove Teacher Record")
        if manager.teachers:
            t_rem_options = {f"{t.name} (ID: {t.id})": t.id for t in manager.teachers}
            selected_rem_label = st.selectbox("Select Teacher to Remove", list(t_rem_options.keys()))
            selected_rem_id = t_rem_options[selected_rem_label]

            if st.button("Confirm Delete Teacher", type="primary"):
                if manager.remove_teacher(selected_rem_id):
                    st.success(f"Teacher record ID {selected_rem_id} removed.")
                    st.rerun()
                else:
                    st.error("Failed to remove teacher.")
        else:
            st.info("No teachers available to remove.")
            