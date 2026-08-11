"""Reviewed discovery vocabulary for the BIPV worked example.

This configuration preserves the source example's five concept groups while
using English/global workbook field aliases. Keyword hits are discovery
signals, not relevance, novelty, ownership, legal-status, or FTO conclusions.
"""

CONFIG_VERSION = "1.1.0-localized"
TOPIC_KEY = "BIPV"
TOPIC_LABEL = "Building-integrated photovoltaics"

# Canonical fields accepted by the localized scripts. COLUMN_ALIASES maps
# common exports to these fields without assuming a single vendor schema.
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

# Inclusive discovery concepts retained from the source configuration.
INCLUDE_KEYWORDS = [
    # Curved and roof-tile photovoltaics
    "curved photovoltaic",
    "curved solar tile",
    "photovoltaic roof tile",
    "solar roof tile",
    "solar shingle",
    "solar clay tile",
    "multi-curved photovoltaic",
    "crystalline silicon solar tile",
    "XBC",

    # Residential pitched-roof BIPV
    "pitched roof photovoltaic",
    "sloped roof BIPV",
    "residential BIPV",
    "building-integrated solar roof",
    "waterproof photovoltaic roof",
    "photovoltaic roofing material",

    # Integrated generation and storage
    "solar storage integration",
    "BIPV energy storage",
    "residential solar storage",
    "home energy storage",
    "off-grid solar storage",
    "energy management system",

    # Lightweight and plug-and-play systems
    "lightweight photovoltaic",
    "plug-and-play solar",
    "portable solar",
    "balcony solar",
    "small-scale BIPV",

    # Glass processing and encapsulation
    "ultra-clear tempered glass",
    "matte photovoltaic glass",
    "curved encapsulation",
    "ultra-thin solar cell",
    "photovoltaic encapsulation ink",
    "curved glass photovoltaic",
]

# Exclusions constrain this worked scope. A hit does not automatically reject a
# record: the script records matched terms and a reviewer confirms disposition.
EXCLUDE_KEYWORDS = [
    "photovoltaic curtain wall",
    "solar facade",
    "photovoltaic facade",
    "commercial flat-roof photovoltaic",
    "utility-scale rooftop photovoltaic",
    "photovoltaic inverter",
    "solar inverter",
    "microinverter",
]

TECHNOLOGY_CATEGORIES = {
    "installation-and-connection": [
        "mounting",
        "connector",
        "roof hook",
        "rail",
        "flashing",
        "waterproof joint",
        "quick installation",
    ],
    "photovoltaic-tile": [
        "solar tile",
        "solar shingle",
        "curved photovoltaic",
        "encapsulation",
        "photovoltaic glass",
    ],
    "roof-system-integration": [
        "roof system",
        "drainage",
        "weatherproof",
        "building envelope",
        "prefabricated roof",
    ],
    "energy-storage-and-management": [
        "energy storage",
        "battery",
        "energy management",
        "microgrid",
        "off-grid",
    ],
}

ENTITY_ALIASES = {
    "Tesla, Inc.": ["Tesla", "Tesla Inc"],
    "AUTARQ GmbH": ["AUTARQ"],
    "LONGi Green Energy Technology Co., Ltd.": ["LONGi", "LONGi Green Energy"],
    "CHINT New Energy Technology Co., Ltd.": ["CHINT New Energy"],
    "Trina Solar Co., Ltd.": ["Trina Solar"],
    "Gotion High-tech Co., Ltd.": ["Gotion", "Gotion High-tech"],
    "Risen Energy Co., Ltd.": ["Risen Energy"],
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
