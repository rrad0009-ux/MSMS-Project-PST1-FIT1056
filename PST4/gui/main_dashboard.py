#=============
#MAIN APPLICATION DASHBOARD AND VIEW LAYER
#=============


#top level window config, state persistance, navigation

import streamlit as st
from app.schedule import ScheduleManager
from gui.student_pages import show_student_management_page
from gui.roster_pages import show_roster_page

def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout="wide", page_title="Music School Management System") #page config. config browser tab title and wide layout

    if 'manager' not in st.session_state:
        st.session_state.manager = ScheduleManager() #initialise schedulemanager once inside session_state
                                                    #storing and controller inside st.session_state ensuring in-memory 
                                                    # records and JSON data persists as the receptionist switches pages 

    st.sidebar.title("MSMS Navigation")
    page = st.sidebar.radio("Go to", ["Student Management", "Daily Roster", "Payments (stub)"]) #sidebar nabigation

    if page == "Student Management": #view routing
        show_student_management_page(st.session_state.manager)
    elif page == "Daily Roster": #displays daily lesson schedules and interactive student check in processing
        show_roster_page(st.session_state.manager)
    elif page == "Payments (stub)": 
        st.header("Payments")
        st.warning("This feature will be implemented in PST5.")