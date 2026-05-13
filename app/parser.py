
import re

QUALITY_MAP = {
    "poor": 2,
    "fair": 4,
    "average": 5,
    "normal": 5,
    "good": 7,
    "very good": 8,
    "excellent": 9,
    "luxury": 10,
}

BASEMENT_QUAL_MAP = {
    "excellent basement": "Ex",
    "good basement": "Gd",
    "average basement": "TA",
    "fair basement": "Fa",
    "poor basement": "Po",
}

GARAGE_TYPE_KEYWORDS = {
    "attached garage": "Attchd",
    "detached garage": "Detchd",
    "built-in garage": "BuiltIn",
    "car port": "CarPort",
    "no garage": "None",
}

def parse_house_text(text: str) -> dict:
    text = text.lower()
    features = {}

    # GrLivArea
    match = re.search(r"(\d+)\s*(sq ft|square feet|sqm|m2)", text)
    if match:
        value = int(match.group(1))
        # simple assumption: if sqm or m2, convert to sq ft
        if match.group(2) in ["sqm", "m2"]:
            value = value * 10.7639
        features["GrLivArea"] = round(value, 2)

    # TotalBsmtSF
    match = re.search(r"basement of (\d+)\s*(sq ft|square feet|sqm|m2)", text)
    if match:
        value = int(match.group(1))
        if match.group(2) in ["sqm", "m2"]:
            value = value * 10.7639
        features["TotalBsmtSF"] = round(value, 2)

    # GarageCars
    match = re.search(r"(\d+)[-\s]car garage", text)
    if match:
        features["GarageCars"] = int(match.group(1))

    # YearBuilt
    match = re.search(r"built in (\d{4})", text)
    if match:
        features["YearBuilt"] = int(match.group(1))

    # YearRemodAdd
    match = re.search(r"remodeled in (\d{4})|renovated in (\d{4})", text)
    if match:
        year = match.group(1) or match.group(2)
        features["YearRemodAdd"] = int(year)

    # LotArea
    match = re.search(r"lot of (\d+)\s*(sq ft|square feet|sqm|m2)", text)
    if match:
        value = int(match.group(1))
        if match.group(2) in ["sqm", "m2"]:
            value = value * 10.7639
        features["LotArea"] = round(value, 2)

    # CentralAir
    if "central air" in text or "air conditioning" in text:
        features["CentralAir"] = "Y"
    elif "no central air" in text or "without air conditioning" in text:
        features["CentralAir"] = "N"

    # GarageType
    for phrase, value in GARAGE_TYPE_KEYWORDS.items():
        if phrase in text:
            features["GarageType"] = value
            break

    # BsmtQual
    for phrase, value in BASEMENT_QUAL_MAP.items():
        if phrase in text:
            features["BsmtQual"] = value
            break

    # OverallQual
    for phrase, value in QUALITY_MAP.items():
        if phrase in text:
            features["OverallQual"] = value
            break

    # OverallCond
    if "well maintained" in text:
        features["OverallCond"] = 7
    elif "needs renovation" in text or "poor condition" in text:
        features["OverallCond"] = 3

    return features