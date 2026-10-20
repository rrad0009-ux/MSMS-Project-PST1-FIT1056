# main.py
from gui.main_dashboard import launch
from app.admin_utils import init_logger, backup_data

if __name__ == "__main__":
    # 1. Initialize session activity logging
    init_logger()
    
    # 2. Trigger automated data backup prior to GUI launch
    backup_data()
    
    # 3. Launch Streamlit GUI dashboard
    launch()
    