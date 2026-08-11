"""Coffee-machine briefing configuration migrated from the frozen source.

The filename is preserved for exact topology. Source examples are discovery
leads only because the frozen package supplied no evidence register for its
future-dated news, market percentages, or technical-leadership statements.
"""

CONFIG_VERSION = "1.1.0-localized"
TOPIC_KEY = "coffee-machine"
TOPIC_LABEL = "Coffee-machine technology"
DEFAULT_REPORT_TITLE = "Patent-Based R&D Briefing: Coffee-Machine Technology"

REPORT_SCOPE = {
    "mechanisms": [
        "grinding and dosing",
        "heating and temperature control",
        "pressure and pre-infusion control",
        "brew-head water distribution and extraction",
        "steam and milk-texture systems",
        "electronic controls, sensors, and water circuits",
    ],
    "excluded": [
        "coffee cultivation",
        "roasting without a material machine relationship",
        "packaging and distribution",
        "unrelated beverage equipment",
    ],
    "geography": "Global; disclose searched jurisdictions and languages",
    "count_unit": "Publication records unless the report explicitly selects simple patent families",
}

CURRENT_AWARENESS = []

SOURCE_NEWS_DISCOVERY_LEADS = [
    {
        "lead_id": "COFFEE-N1",
        "topic": "Market growth and smart-machine adoption",
        "source_date": "2026-04-15",
        "review_status": "unverified migrated source lead",
        "publication_allowed": False,
        "required_action": "Locate the underlying market dataset; verify geography, currency, price year, denominator, and methodology.",
    },
    {
        "lead_id": "COFFEE-N2",
        "topic": "Dynamic pressure-control announcement",
        "source_date": "2026-04-08",
        "review_status": "unverified migrated source lead",
        "publication_allowed": False,
        "required_action": "Verify an official product, patent, or technical source and avoid unsupported leadership language.",
    },
    {
        "lead_id": "COFFEE-N3",
        "topic": "Premium-machine patent activity",
        "source_date": "2026-04-20",
        "review_status": "unverified migrated source lead",
        "publication_allowed": False,
        "required_action": "Reproduce the patent search and separate activity volume from capability or market positioning.",
    },
]

ORGANIZATION_DISCOVERY_LEADS = [
    {
        "organization": "Nestlé S.A.",
        "region": "Switzerland",
        "source_publications": ["EP4142506B1", "CN121866375A", "WO2026074139A1"],
        "themes_to_verify": ["roasting equipment", "capsule materials", "beverage system integration"],
    },
    {
        "organization": "De'Longhi S.p.A.",
        "region": "Italy",
        "source_publications": ["US20260114661A1", "EP4391875B1", "WO2026082413A1", "EP4468924B1"],
        "themes_to_verify": ["grinding-time calculation", "hot/cold extraction", "dose control"],
    },
    {
        "organization": "Midea Group Co., Ltd.",
        "region": "China",
        "source_publications": ["CN121890870A", "CN121910257A", "CN121867605A", "KR102951938B1"],
        "themes_to_verify": ["extraction", "pressure control", "water-treatment integration"],
    },
    {
        "organization": "Bear Electric Appliance Co., Ltd.",
        "region": "China",
        "source_publications": ["CN224070203U", "CN224070204U", "CN224070190U"],
        "themes_to_verify": ["milk-foaming structures"],
    },
    {
        "organization": "Breville Group Limited",
        "region": "Australia",
        "source_publications": ["AU2024360509A1", "EP4540926A4", "EP4732725A2"],
        "themes_to_verify": ["machine architecture", "accessory power and communication", "sensors"],
    },
    {
        "organization": "Guangdong Xinbao Electrical Appliances Holdings Co., Ltd.",
        "region": "China",
        "source_publications": ["CN224166124U", "CN121890878A", "CN118104965B"],
        "themes_to_verify": ["brewing structures", "rotating extraction", "cold-drip systems"],
    },
]

TECHNOLOGY_CATEGORIES = [
    {
        "category_id": "grinding-precision-and-uniformity",
        "label": "Grinding precision and uniformity",
        "decision_questions": ["particle-size distribution", "retention", "dose repeatability", "calibration", "wear"],
        "source_example_publications": ["US20260114661A1", "WO2026082413A1"],
    },
    {
        "category_id": "heating-and-temperature-control",
        "label": "Heating and temperature control",
        "decision_questions": ["warm-up time", "stability", "multi-zone control", "energy use", "test conditions"],
        "source_example_publications": ["EP4391875B1", "EP4468924B1"],
    },
    {
        "category_id": "dynamic-pressure-control",
        "label": "Dynamic pressure control",
        "decision_questions": ["profile resolution", "sensor accuracy", "pump response", "pre-infusion", "repeatability"],
        "source_example_publications": ["CN121890870A", "EP4468924B1"],
    },
    {
        "category_id": "brew-head-and-water-distribution",
        "label": "Brew-head and water-distribution systems",
        "decision_questions": ["flow uniformity", "channeling", "cleanability", "pressure drop", "extraction repeatability"],
        "source_example_publications": ["CN121890878A", "CN224166124U", "CN121910257A"],
    },
    {
        "category_id": "steam-and-milk-texture",
        "label": "Steam and milk-texture systems",
        "decision_questions": ["bubble-size distribution", "temperature", "cleaning", "automation", "milk alternatives"],
        "source_example_publications": ["CN224070203U", "CN224070204U", "CN224070190U", "CN224166112U"],
    },
    {
        "category_id": "controls-and-water-circuit",
        "label": "Controls, sensors, and water circuits",
        "decision_questions": ["closed-loop control", "sensor drift", "flow metering", "diagnostics", "interoperability"],
        "source_example_publications": ["EP4540926A4", "CN121867605A", "KR102951938B1"],
    },
]

RELEASE_REQUIREMENTS = {
    "current_awareness_requires_evidence_ids": True,
    "organization_summaries_derived_from_reviewed_records": True,
    "configured_counts_are_never_authoritative": True,
    "publication_and_family_counts_are_separate": True,
    "legal_status_as_of_date_required": True,
    "patent_professional_review_for_legal_conclusions": True,
}
