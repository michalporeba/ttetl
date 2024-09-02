def format_duration(seconds: int) -> str:
    if seconds >= 3*24*60*60:
        return f"{seconds // (24*60*60)} days"

    h = seconds // (60 * 60)
    m = (seconds // 60) % 60
    s = seconds % 60

    if seconds >= 60*60:
        return f"{h:02d}:{m:02d}:{s:02d}"

    return f"{m:02d}:{s:02d}"