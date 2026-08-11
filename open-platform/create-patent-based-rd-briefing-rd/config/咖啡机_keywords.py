"""Reviewed discovery vocabulary for the coffee-machine worked example.

The Chinese filename is retained solely because exact frozen-source topology is
required. All executable content and display text are localized to English.
"""

CONFIG_VERSION = "1.1.0-localized"
TOPIC_KEY = "coffee-machine"
TOPIC_LABEL = "Coffee-machine technology"

SEARCH_FIELDS = [
    "title",
    "normalized_title",
    "technical_problem",
    "technical_solution",
    "technical_effect",
    "abstract",
    "independent_claims",
]

COLUMN_ALIASES = {
    "publication_number": ["Publication number", "Publication Number", "PN"],
    "title": ["Title", "Patent title", "Original title"],
    "normalized_title": ["PatSnap patent title", "Normalized title"],
    "applicant": ["Current applicant", "Applicant", "Assignee"],
    "legal_status": ["Legal status", "Simple legal status", "Status"],
    "application_date": ["Application date", "Filing date"],
    "publication_date": ["Publication date"],
    "technical_problem": ["Technical problem"],
    "technical_solution": ["Technical solution", "Technical means"],
    "technical_effect": ["Technical effect"],
    "abstract": ["Abstract"],
    "independent_claims": ["Independent claims", "Claims"],
    "family_id": ["Simple family ID", "Family ID"],
    "source_url": ["Source URL", "Patent URL"],
}

INCLUDE_KEYWORDS = [
    # Grinding precision and uniformity
    "grinding precision",
    "grinding uniformity",
    "coffee grinder",
    "burr grinder",
    "particle size distribution",
    "conical burr",
    "flat burr",
    "grinding consistency",

    # Heating and temperature control
    "heating control",
    "temperature control",
    "PID control",
    "thermal stability",
    "heating block",
    "boiler",
    "heat exchanger",
    "preheating",

    # Pressure control
    "extraction pressure",
    "pressure profiling",
    "pre-infusion",
    "pressure curve",
    "pump pressure",
    "pressure sensor",
    "dynamic pressure",

    # Brew-head distribution and extraction
    "brew head",
    "shower screen",
    "water distribution",
    "extraction uniformity",
    "coffee extraction",
    "brewing uniformity",

    # Steam and milk texture
    "steam wand",
    "steam nozzle",
    "milk froth",
    "microfoam",
    "milk texture",
    "automatic milk frother",

    # Controls and water circuit
    "closed-loop control",
    "electronic control",
    "smart coffee machine",
    "water flow control",
    "flow sensor",
    "water level detection",
    "remote control",
    "IoT",

    # Domain terms
    "coffee machine",
    "espresso machine",
    "coffee maker",
    "automatic coffee machine",
    "semi-automatic coffee machine",
]

EXCLUDE_KEYWORDS = [
    "tea machine",
    "juice machine",
    "juicer",
    "coffee plantation",
    "green coffee processing",
    "coffee roasting only",
    "coffee packaging",
    "coffee delivery",
]

TECHNOLOGY_CATEGORIES = {
    "grinding-precision-and-uniformity": [
        "grind",
        "grinder",
        "burr",
        "particle size",
        "dose correction",
    ],
    "heating-and-temperature-control": [
        "heat",
        "temperature",
        "thermal",
        "boiler",
        "heater",
    ],
    "dynamic-pressure-control": [
        "pressure",
        "pump",
        "pre-infusion",
        "pressure profile",
    ],
    "brew-head-and-water-distribution": [
        "brew head",
        "extraction",
        "water distribution",
        "shower screen",
    ],
    "steam-and-milk-texture": [
        "steam",
        "milk",
        "froth",
        "foam",
    ],
    "controls-and-water-circuit": [
        "control",
        "sensor",
        "water circuit",
        "flow",
        "automation",
    ],
}

ENTITY_ALIASES = {
    "De'Longhi S.p.A.": ["DeLonghi", "DE LONGHI", "DELONGHI"],
    "Nestlé S.A.": ["Nestle", "NESTLE", "NESTEC"],
    "Midea Group Co., Ltd.": ["Midea", "MIDEA"],
    "Breville Group Limited": ["Breville"],
    "Philips": ["PHILIPS"],
    "Joyoung Co., Ltd.": ["Joyoung"],
}

RELEVANCE_LABELS = {
    "include": "Included — reviewer confirmed",
    "candidate": "Candidate — requires review",
    "exclude": "Excluded — reviewer confirmed",
}

REVIEW_POLICY = {
    "automatic_inclusion": False,
    "title_only_review_allowed": False,
    "independent_claim_review_for_material_findings": True,
    "family_normalization_required": True,
    "record_matched_terms": True,
    "record_reviewer_and_date": True,
}
