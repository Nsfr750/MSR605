"""
Logging configuration for MSR605 Card Reader.
Creates a new log file each day with the format: msr605_YYYYMMDD.log
"""
import logging
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Constants
LOG_FILE_PREFIX = "msr605_"
LOG_FILE_EXT = ".log"
MAX_LOG_DAYS = 30  # Maximum number of days to keep log files

# Get the project root directory (one level up from script directory)
APP_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR = APP_DIR / "logs"

def ensure_log_dir():
    """Ensure the log directory exists and return the log file path."""
    try:
        LOG_DIR.mkdir(exist_ok=True, parents=True)
        return True
    except Exception as e:
        print(f"ERROR: Failed to create log directory {LOG_DIR}: {e}", file=sys.stderr)
        return False

def get_log_file():
    """Get the path to the current log file based on the current date."""
    date_str = datetime.now().strftime("%Y%m%d")
    return LOG_DIR / f"{LOG_FILE_PREFIX}{date_str}{LOG_FILE_EXT}"

class DailyFileHandler(logging.FileHandler):
    """Custom file handler that creates a new log file each day."""
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        self.current_date = datetime.now().date()
        filename = self.get_filename()
        super().__init__(filename, mode, encoding, delay)
        
    def get_filename(self):
        """Get the current log filename based on the current date."""
        date_str = self.current_date.strftime("%Y%m%d")
        return LOG_DIR / f"{LOG_FILE_PREFIX}{date_str}{LOG_FILE_EXT}"
        
    def should_rollover(self):
        """Check if we should roll over to a new log file."""
        return datetime.now().date() > self.current_date
        
    def emit(self, record):
        """Emit a record, creating a new file if the date has changed."""
        if self.should_rollover():
            self.current_date = datetime.now().date()
            self.baseFilename = str(self.get_filename())
            self.stream = self._open()
        super().emit(record)

def setup_logging() -> logging.Logger:
    """
    Configure logging for the application with daily log rotation.
    
    Returns:
        logging.Logger: The configured logger instance
    """
    global logger
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Set log level
    logger.setLevel(logging.DEBUG)
    
    # Create formatter
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    
    # Console handler (always available)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with daily rotation (only if log directory is accessible)
    if ensure_log_dir():
        try:
            log_file = get_log_file()
            file_handler = DailyFileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.info(f"Logging to file: {log_file.absolute()}")
            
            # Clean up old log files
            cleanup_old_logs()
        except Exception as e:
            logger.error(f"Failed to configure file logging: {e}")
    else:
        logger.warning("Logging to console only - could not access log directory")
    
    return logger

def cleanup_old_logs():
    """Remove log files older than MAX_LOG_DAYS days."""
    try:
        if not LOG_DIR.exists():
            return
            
        cutoff_date = datetime.now() - timedelta(days=MAX_LOG_DAYS)
        
        for log_file in LOG_DIR.glob(f"{LOG_FILE_PREFIX}*{LOG_FILE_EXT}"):
            try:
                # Extract date from filename (format: msr605_YYYYMMDD.log)
                date_str = log_file.stem.replace(LOG_FILE_PREFIX, '')
                file_date = datetime.strptime(date_str, "%Y%m%d").date()
                
                if file_date < cutoff_date.date():
                    log_file.unlink()
                    logger.debug(f"Removed old log file: {log_file}")
            except (ValueError, Exception) as e:
                logger.warning(f"Error processing log file {log_file}: {e}")
                
    except Exception as e:
        logger.error(f"Error cleaning up old log files: {e}", exc_info=True)

# Create a module-level logger instance
logger = logging.getLogger("msr605")
setup_logging()
