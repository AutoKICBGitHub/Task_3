def normalize_order_number(order_num_str):
    return str(order_num_str).strip().replace("#", "").lstrip('0') or '0'
