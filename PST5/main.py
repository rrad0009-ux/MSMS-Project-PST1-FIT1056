# main.py
import logging
from gui.main_dashboard import launch
from app.admin_utils import init_logger, backup_data

if __name__ == "__main__":
    # 1. Initialize logger as the very first step
    init_logger()
    
    # 2. Perform automated data backup before starting session
    backup_data()
    
    # 3. Launch interactive Streamlit GUI
    launch()
    