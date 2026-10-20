# gui/finance_pages.py
#==========================================
# FINANCIAL MANAGEMENT AND PAYMENTS GUI VIEW
#==========================================

# handles payment recording, history tracking, and report exports

import streamlit as st

def show_finance_page(manager):
    """Renders the finance and payment management page in Streamlit."""
    st.header("Financial Management & Payment History")

    # --- section 1: record a new payment ---
    st.subheader("Record Student Payment")
    
    # dynamically retrieve student records directly from live manager state
    if manager.students:
        student_options = {f"{s.name} (ID: {s.id})": s.id for s in manager.students}
        
        with st.form("record_payment_form"):
            selected_student_label = st.selectbox("Select Student", list(student_options.keys()))
            student_id = student_options[selected_student_label]
            amount = st.number_input("Payment Amount ($)", min_value=1.0, value=50.0, step=5.0)
            method = st.selectbox("Payment Method", ["Credit Card", "Bank Transfer", "Cash", "PayPal"])
            
            submit_payment = st.form_submit_button("Record Payment")
            
            if submit_payment:
                payment = manager.record_payment(student_id, amount, method)
                if payment:
                    st.success(f"Successfully recorded ${amount:.2f} payment via {method} for Student ID {student_id}!")
                    st.rerun()
                else:
                    st.error("Failed to record payment. Please check student details.")
    else:
        st.info("No students registered yet. Please register a student first under Student Management.")

    st.divider()

    # --- section 2: view payment history ---
    st.subheader("Student Payment History")
    
    if manager.students:
        lookup_student_label = st.selectbox("Select Student to View History", list(student_options.keys()), key="history_select")
        lookup_student_id = student_options[lookup_student_label]
        
        history = manager.get_payment_history(lookup_student_id)
        
        if history:
            st.write(f"Payment records for **{lookup_student_label}**:")
            st.dataframe(history, use_container_width=True)
        else:
            st.info(f"No payment history found for Student ID {lookup_student_id}.")
    else:
        st.info("No students registered yet.")

    st.divider()

    # --- section 3: export financial report ---
    st.subheader("Export Reports")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export Finance Report (CSV)"):
            out_file = "data/finance_report.csv"
            if manager.export_report("finance", out_file):
                st.success(f"Exported financial log to `{out_file}`.")
            else:
                st.error("Failed to export report.")
    with col2:
        if st.button("Export Attendance Report (CSV)"):
            out_file = "data/attendance_report.csv"
            if manager.export_report("attendance", out_file):
                st.success(f"Exported attendance log to `{out_file}`.")
            else:
                st.error("Failed to export report.")
                