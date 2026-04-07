from utils.logger import logger

def detect_ats(url: str) -> str:
    url = url.lower()

    if "workday" in url:
        ats = "workday"
    elif "greenhouse" in url:
        ats = "greenhouse"
    elif "lever" in url:
        ats = "lever"
    elif "linkedin" in url:
        ats = "linkedin"
    else:
        ats = "unknown"

    logger.info(f"[ATS] Detection result: {ats}")
    return ats