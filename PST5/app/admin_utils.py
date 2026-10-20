# app/admin_utils.py
import logging
import shutil
import os
from datetime import datetime

def init_logger(log_file="msms.log"):
    """Initializes Python's logging module for system activity tracking."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info("--- Application Session Started ---")

def backup_data(data_path="data/msms.json", backup_dir="data/backups"):
    """Creates a timestamped backup copy of the data file in the specified folder."""
    if not os.path.exists(data_path):
        logging.warning(f"Backup skipped: Source file '{data_path}' does not exist.")
        return None

    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"msms_backup_{timestamp}.json"
    destination_path = os.path.join(backup_dir, backup_filename)

    try:
        shutil.copy2(data_path, destination_path)
        logging.info(f"Data backup created successfully at: {destination_path}")
        return destination_path
    except Exception as e:
        logging.error(f"Failed to create data backup: {e}")
        return None
    