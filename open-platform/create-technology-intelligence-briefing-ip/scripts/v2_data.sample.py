"""Synthetic data contract for build_report_v2.py.

Copy this file to ``v2_data.py`` in an approved working directory and replace
the placeholders with validated evidence. Never store secrets in this module.
"""

TITLE = "Technology intelligence briefing: Example topic"
TIME_RANGE = "2025-01-01 to 2025-12-31"
EVIDENCE_CUTOFF = "2026-08-07"

SCOPE = {
    "research_question": "How is the selected technology evolving?",
    "technology": "Example topic",
    "companies": ["Example Corp"],
    "jurisdictions": ["US", "EP", "WO"],
    "date_field": "publication_date",
    "counting_unit": "simple_family",
    "family_rule": "One representative publication per simple family",
    "display_selection": "Evidence-rich representative records",
}

SECTION_STATUS = {
    "patents": "executed",
    "literature": "executed",
    "news": "executed",
}

LIMITATIONS = [
    "Synthetic example only; no value in this file is a real research result.",
    "Population counts and displayed records are intentionally separate.",
]

SUMMARY = [
    {
        "finding": "Synthetic finding for renderer testing.",
        "evidence_ids": ["EXAMPLE-001"],
        "confidence": "Example only",
        "limitation": "Not a real-world conclusion.",
    }
]

PATENT_TOTAL_BY_COMPANY = {
    "Example Corp": {
        "population_count": 125,
        "count_status": "synthetic",
        "displayed_count": 1,
        "counting_unit": "simple_family",
    }
}

TREND_SERIES = {
    "Example Corp": {
        "2023": 20,
        "2024": 35,
        "2025": 42,
    }
}

TREND_META = {
    "date_field": "publication_date",
    "counting_unit": "simple_family",
    "partial_periods": [],
}

WORD_CLOUD = [
    {"term": "example mechanism", "count": 14},
    {"term": "example material", "count": 9},
]

WORD_CLOUD_META = {
    "source_field": "title_and_abstract",
    "basis": "selected candidate sample",
    "normalization": "lowercase; phrase-level counting; stopwords removed",
}

PATENTS = [
    {
        "id": "EXAMPLE-001",
        "publication_number": "US20XXXXXXXA1",
        "title": "Synthetic patent title",
        "assignee": "Example Corp",
        "inventors": ["A. Researcher"],
        "priority_date": "2023-01-15",
        "publication_date": "2024-07-18",
        "jurisdiction": "US",
        "kind": "A1",
        "status": "Unknown — synthetic fixture",
        "status_as_of": "2026-08-07",
        "classifications": ["G00X 00/00"],
        "family_id": "SIMPLE-FAMILY-EXAMPLE-1",
        "summary": "Synthetic summary used to test escaping and layout.",
        "technical_problem": "Synthetic problem statement.",
        "technical_means": "Synthetic technical means.",
        "reported_effect": "Synthetic reported effect.",
        "evidence_locator": "Synthetic fixture; not a source",
        "url": "https://example.com/patent/EXAMPLE-001",
        "limitations": "No real patent evidence.",
    }
]

PATENTS_BY_COMPANY = {
    "Example Corp": ["EXAMPLE-001"],
}

SUB_TECHS = [
    {
        "id": "example-subtechnology",
        "name": "Example subtechnology",
        "definition": "Synthetic category for layout testing.",
        "method": "Synthetic manual assignment",
        "patents": ["EXAMPLE-001"],
    }
]

LITERATURE = [
    {
        "id": "LIT-EXAMPLE-001",
        "title": "Synthetic literature title",
        "authors": ["A. Author", "B. Author"],
        "journal": "Example Journal",
        "year": 2025,
        "doi": "10.0000/example-doi",
        "url": "https://doi.org/10.0000/example-doi",
        "summary": "Synthetic summary; not a real publication.",
        "reason_included": "Renderer fixture",
        "source": "Synthetic fixture",
        "retrieved_at": "2026-08-07",
        "limitations": "Do not cite.",
    }
]

NEWS = [
    {
        "id": "NEWS-EXAMPLE-001",
        "title": "Synthetic news headline",
        "source": "Example Newsroom",
        "publication_date": "2025-11-04",
        "event_date": "2025-11-03",
        "url": "https://example.com/news/example",
        "summary": "Synthetic news synopsis for renderer testing.",
        "relevance": "Renderer fixture",
        "source_quality": "Synthetic — not evidence",
        "retrieved_at": "2026-08-07",
    }
]

SOURCES = [
    {
        "id": "SOURCE-EXAMPLE-001",
        "type": "synthetic_fixture",
        "title": "Example source",
        "url": "https://example.com/",
        "retrieved_at": "2026-08-07",
    }
]
