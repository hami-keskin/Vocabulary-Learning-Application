from datetime import datetime

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")

def get_today():
    return format_date(datetime.now())
