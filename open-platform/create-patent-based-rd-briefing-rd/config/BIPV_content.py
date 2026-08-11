"""BIPV briefing configuration migrated from the frozen source example.

The source contained dated news, numerical assertions, organization summaries,
and patent lists that were not accompanied by a frozen evidence register.
They are retained below only as discovery leads. The renderer must not publish a
lead until `review_status` is `reviewed` and its evidence IDs resolve.
"""

CONFIG_VERSION = "1.1.0-localized"
TOPIC_KEY = "BIPV"
TOPIC_LABEL = "Building-integrated photovoltaics"
DEFAULT_REPORT_TITLE = "Patent-Based R&D Briefing: Building-Integrated Photovoltaics"

REPORT_SCOPE = {
    "mechanisms": [
        "photovoltaic roof tiles and shingles",
        "residential pitched-roof integration",
        "roof mounting, connection, drainage, and weatherproofing",
        "integrated energy storage and energy management",
        "glass, encapsulation, and curved photovoltaic structures",
    ],
    "excluded": [
        "standalone inverters without a material BIPV relationship",
        "utility-scale or flat-roof systems without building integration",
        "facade-only systems outside the approved decision scope",
    ],
    "geography": "Global; report actual search jurisdictions and languages",
    "count_unit": "Publication records unless a report explicitly selects simple patent families",
}

# A release report should normally populate current awareness from reviewed
# primary sources. These source-example records are intentionally withheld.
CURRENT_AWARENESS = []

SOURCE_NEWS_DISCOVERY_LEADS = [
    {
        "lead_id": "BIPV-N1",
        "topic": "Green-building project governance",
        "source_region": "Shanghai, China",
        "source_date": "2026-04-13",
        "original_source_type": "industry-news portal",
        "review_status": "unverified migrated source lead",
        "publication_allowed": False,
        "required_action": "Verify the underlying government notice, effective date, scope, and official URL.",
    },
    {
        "lead_id": "BIPV-N2",
        "topic": "Facade contractor and developer project announcement",
        "source_region": "Hong Kong",
        "source_date": "2026-04-16",
        "original_source_type": "organization social-media post",
        "review_status": "unverified migrated source lead",
        "publication_allowed": False,
        "required_action": "Verify project relevance to BIPV and replace the social-media lead with a stable primary source.",
    },
    {
        "lead_id": "BIPV-N3",
        "topic": "Energy-technology company sustainability report",
        "source_date": "2026-04-30",
        "review_status": "unverified migrated source lead",
        "publication_allowed": False,
        "required_action": "Review the report and extract only decision-relevant BIPV facts.",
    },
    {
        "lead_id": "BIPV-N4",
        "topic": "Back-contact cell and module efficiency announcement",
        "source_date": "2026-04-28",
        "review_status": "unverified migrated source lead",
        "publication_allowed": False,
        "required_action": "Verify test laboratory, device area, test standard, certification, and applicability to BIPV.",
    },
    {
        "lead_id": "BIPV-N5",
        "topic": "Commercial module-efficiency ranking",
        "source_date": "2026-04-25",
        "review_status": "unverified migrated source lead",
        "publication_allowed": False,
        "required_action": "Verify ranking methodology and use a direct publisher record.",
    },
]

ORGANIZATION_DISCOVERY_LEADS = [
    {
        "organization": "Tesla, Inc.",
        "region": "United States",
        "source_publications": ["US12598838B2", "US12580517B2", "HK40076670B"],
        "themes_to_verify": ["visual integration", "roof-tile mounting", "coating and appearance"],
    },
    {
        "organization": "AUTARQ GmbH",
        "region": "Germany",
        "source_publications": ["WO2025256709A3"],
        "themes_to_verify": ["modular electrical connection for roof tiles"],
    },
    {
        "organization": "LONGi Green Energy Technology Co., Ltd.",
        "region": "China",
        "source_publications": ["CN223978599U"],
        "themes_to_verify": ["adjustable roof-tile mounting"],
    },
    {
        "organization": "CHINT New Energy Technology Co., Ltd.",
        "region": "China",
        "source_publications": ["CN224154164U"],
        "themes_to_verify": ["residential module support and attachment"],
    },
    {
        "organization": "Trina Solar Co., Ltd.",
        "region": "China",
        "source_publications": ["CN223937481U", "CN224106747U", "CN224111100U"],
        "themes_to_verify": ["mounting connection", "roof system integration", "weatherproofing"],
    },
    {
        "organization": "Gotion High-tech Co., Ltd.",
        "region": "China",
        "source_publications": ["CN223967818U"],
        "themes_to_verify": ["tile overlap and support"],
    },
    {
        "organization": "Risen Energy Co., Ltd.",
        "region": "China",
        "source_publications": ["CN223978600U", "CN224161307U"],
        "themes_to_verify": ["flat and curved photovoltaic tiles"],
    },
]

TECHNOLOGY_CATEGORIES = [
    {
        "category_id": "installation-and-connection",
        "label": "Installation and connection systems",
        "decision_questions": ["installation time", "tolerance", "weatherproofing", "serviceability", "interface standardization"],
        "source_example_publications": ["CN223957486U", "CN224119821U", "CN223978600U", "CN117536393B", "CN223978599U"],
    },
    {
        "category_id": "photovoltaic-tile",
        "label": "Photovoltaic tile and shingle structures",
        "decision_questions": ["appearance", "encapsulation", "weathering", "thermal behavior", "cell integration"],
        "source_example_publications": ["CN224161307U", "CN117558786B", "US12598838B2", "HK40076670B", "CN120941858B"],
    },
    {
        "category_id": "roof-system-integration",
        "label": "Roof-system integration",
        "decision_questions": ["drainage", "wind loading", "fire", "replacement", "building-code interfaces"],
        "source_example_publications": ["CN224119805U", "CN223964086U", "CN223964067U", "CN223967818U", "CN224106747U"],
    },
    {
        "category_id": "energy-storage-and-management",
        "label": "Energy storage and management",
        "decision_questions": ["system boundary", "control architecture", "safety", "grid interface", "economics"],
        "source_example_publications": ["CN121461405A"],
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
