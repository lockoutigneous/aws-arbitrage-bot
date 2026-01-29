"""
Các hàm xác thực và kiểm tra đầu vào.
"""
from typing import List, Tuple, Optional
from configs import BOT_MODES, SUPPORTED_EXCHANGES


def validate_mode(mode: str) -> bool:
    """
    Kiểm tra chế độ bot có hợp lệ không.
    
    Args:
        mode (str): Chế độ bot
        
    Returns:
        bool: True nếu hợp lệ, False nếu không
    """
    return mode in BOT_MODES


def validate_exchange(exchange_id: str) -> bool:
    """
    Kiểm tra sàn giao dịch có được hỗ trợ không.
    
    Args:
        exchange_id (str): ID của sàn giao dịch
        
    Returns:
        bool: True nếu được hỗ trợ, False nếu không
    """
    return exchange_id.lower() in SUPPORTED_EXCHANGES


def validate_positive_number(value, name: str = "value") -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra giá trị có phải là số dương không.
    
    Args:
        value (Union[int, float, str]): Giá trị cần kiểm tra
        name (str): Tên của giá trị (dùng cho thông báo lỗi)
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    try:
        num = float(value)
        if num <= 0:
            return False, f"{name} phải là số dương"
        return True, None
    except (ValueError, TypeError):
        return False, f"{name} phải là một số hợp lệ"


def validate_positive_integer(value, name: str = "value") -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra giá trị có phải là số nguyên dương không.
    
    Args:
        value (Union[int, str]): Giá trị cần kiểm tra
        name (str): Tên của giá trị (dùng cho thông báo lỗi)
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    try:
        num = int(value)
        if num <= 0:
            return False, f"{name} phải là số nguyên dương"
        return True, None
    except (ValueError, TypeError):
        return False, f"{name} phải là một số nguyên hợp lệ"


def validate_symbol(symbol: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra ký hiệu cặp giao dịch có đúng định dạng không.
    
    Args:
        symbol (str): Ký hiệu cặp giao dịch
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not symbol:
        return True, None  # Cho phép để trống để tự động tìm
    
    # Kiểm tra định dạng BASE/QUOTE hoặc BASE:QUOTE
    if '/' not in symbol and ':' not in symbol:
        return False, "Ký hiệu cặp giao dịch phải có dạng BASE/QUOTE (ví dụ: BTC/USDT)"
    
    # Kiểm tra cặp có chứa USDT
    if 'USDT' not in symbol.upper():
        return False, "Cặp giao dịch phải chứa USDT"
    
    return True, None


def validate_exchanges_unique(exchanges: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra các sàn giao dịch có khác nhau không.
    
    Args:
        exchanges (list): Danh sách các sàn giao dịch
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    # Normalize to lowercase for case-insensitive comparison
    normalized = [ex.lower() for ex in exchanges]
    if len(normalized) != len(set(normalized)):
        return False, "Các sàn giao dịch phải khác nhau"
    return True, None
