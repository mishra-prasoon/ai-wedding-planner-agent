import re
import logging

# Setup logging for security events
logging.basicConfig(
    filename='wedding_planner_security.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def sanitize_input(text: str, max_length: int = 200) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    # Remove dangerous characters
    text = re.sub(r'[<>{}|\[\]`]', '', text)
    
    # Limit length
    text = text.strip()[:max_length]
    
    if not text:
        raise ValueError("Input cannot be empty")
    
    return text

def validate_budget(amount: float) -> float:
    """Validate budget amount is reasonable."""
    if not isinstance(amount, (int, float)):
        raise ValueError("Budget must be a number")
    if amount <= 0:
        raise ValueError("Budget must be positive")
    if amount > 100000000:  # 10 crore max
        raise ValueError("Budget amount seems unrealistic")
    return float(amount)

def validate_date(date_str: str) -> str:
    """Validate date format YYYY-MM-DD."""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        raise ValueError("Date must be in YYYY-MM-DD format")
    return date_str

def validate_email(email: str) -> str:
    """Basic email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email address")
    return email.lower()

def mask_sensitive_data(data: dict) -> dict:
    """Mask sensitive fields before logging."""
    sensitive_fields = ['email', 'phone', 'contact', 'address']
    masked = data.copy()
    for field in sensitive_fields:
        if field in masked:
            masked[field] = "***MASKED***"
    return masked

def log_security_event(event_type: str, details: str):
    """Log security-relevant events."""
    logging.warning(f"SECURITY EVENT [{event_type}]: {details}")