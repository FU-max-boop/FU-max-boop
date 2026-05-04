# DeepResearch-ReportEval Offline Corpus Audit

- Generated at: `2026-05-04T15:13:55.466790+00:00`
- Input path: `data/report/qwen-reports.jsonl`
- Topic path: `data/topic/high_quality_topics.jsonl`
- Reports scanned: 100
- Redundancy risk threshold: 0.42

## Corpus Summary

- Average words per report: 3633.97
- Median words per report: 3620.0
- Average sections per report: 6.94
- Average citation markers per report: 123.98
- Reports with dangling citations: 0
- Reports with empty references: 79
- Reports with high redundancy risk: 82
- Reports with low topic-heading overlap: 8
- Reports with zero topic-heading overlap: 1
- Max top redundancy risk: 0.7407

## Category Summary

| category | count | avg_words | avg_sections | avg_citations | avg_top_redundancy_risk | avg_topic_keyword_coverage | avg_audit_risk_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Art, Music & Literature | 7 | 3585.57 | 7 | 124 | 0.4407 | 0.4517 | 1.71 |
| Economy & Business | 16 | 3625.69 | 7 | 118.62 | 0.4715 | 0.4309 | 1.94 |
| Education | 8 | 3731 | 7 | 131.88 | 0.4849 | 0.5444 | 2 |
| Entertainment & Fashion | 5 | 3262.8 | 7 | 106 | 0.5074 | 0.2347 | 2.8 |
| Environment & Nature | 2 | 3283 | 6.5 | 143 | 0.5131 | 0.4095 | 2 |
| Health & Medicine | 10 | 3674.2 | 6.5 | 130.4 | 0.43 | 0.4918 | 2.3 |
| History & Culture | 5 | 3593 | 7.4 | 115.6 | 0.4349 | 0.3776 | 1.6 |
| Lifestyle | 1 | 4254 | 10 | 190 | 0.5474 | 0.2353 | 2 |
| Other | 2 | 3699 | 7 | 127 | 0.5208 | 0.3216 | 2.5 |
| Politics & Society | 5 | 3701.4 | 6.8 | 117 | 0.522 | 0.6183 | 2.6 |
| Science & Technology | 37 | 3655.27 | 6.89 | 123.57 | 0.496 | 0.4541 | 2.16 |
| Sports & Fitness | 2 | 3724 | 7 | 139 | 0.6208 | 0.4658 | 3 |

## Top Risk Reports

| index | category | word_count | section_count | reference_count | empty_reference_count | topic_keyword_coverage | top_redundancy_risk | audit_risk_score | flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 53 | Entertainment & Fashion | 3333 | 7 | 16 | 4 | 0.1667 | 0.5737 | 4 | empty_references;low_citation_density;high_redundancy_risk;low_topic_heading_overlap |
| 95 | Education | 4162 | 7 | 24 | 3 | 0.6364 | 0.5303 | 4 | empty_references;very_long_section;low_citation_density;high_redundancy_risk |
| 59 | Sports & Fitness | 3758 | 7 | 26 | 4 | 0.1538 | 0.5008 | 4 | empty_references;low_citation_density;high_redundancy_risk;low_topic_heading_overlap |
| 46 | Art, Music & Literature | 3750 | 7 | 24 | 2 | 0.3889 | 0.4535 | 4 | empty_references;very_long_section;low_citation_density;high_redundancy_risk |
| 30 | Health & Medicine | 2821 | 1 | 29 | 3 | 0.1562 | 0.0 | 4 | empty_references;few_sections;very_long_section;low_topic_heading_overlap |
| 20 | Science & Technology | 3481 | 7 | 24 | 9 | 0.4615 | 0.6395 | 3 | empty_references;low_citation_density;high_redundancy_risk |
| 62 | Economy & Business | 3112 | 7 | 17 | 3 | 0.24 | 0.6173 | 3 | empty_references;low_citation_density;high_redundancy_risk |
| 24 | Science & Technology | 4336 | 7 | 19 | 1 | 0.5714 | 0.5713 | 3 | empty_references;low_citation_density;high_redundancy_risk |
| 38 | Politics & Society | 4429 | 7 | 23 | 2 | 1.0 | 0.5611 | 3 | empty_references;low_citation_density;high_redundancy_risk |
| 98 | Other | 3016 | 7 | 27 | 1 | 0.1765 | 0.5562 | 3 | empty_references;high_redundancy_risk;low_topic_heading_overlap |

## Low Topic-Heading Overlap Reports

| index | category | topic_keyword_coverage | report_title | flags |
| --- | --- | --- | --- | --- |
| 8 | Science & Technology | 0.0 | A Comparative Analysis of Tesla and BYD: The Battery and Charging Frontiers | empty_references;high_redundancy_risk;zero_topic_heading_overlap |
| 89 | Science & Technology | 0.08 | A Deep Dive into AI Product Methodologies and Leadership | empty_references;low_citation_density;low_topic_heading_overlap |
| 70 | Economy & Business | 0.1111 | A Deep Dive into the Composition of U.S. Consumer Spending | empty_references;low_topic_heading_overlap |
| 59 | Sports & Fitness | 0.1538 | A Deep Dive into McLaren's 2025 Formula 1 Dominance | empty_references;low_citation_density;high_redundancy_risk;low_topic_heading_overlap |
| 30 | Health & Medicine | 0.1562 | A Comprehensive Analysis of LDL Cholesterol Levels: Balancing Cardiovascular Risk and Potential Adverse Effects | empty_references;few_sections;very_long_section;low_topic_heading_overlap |
| 44 | History & Culture | 0.16 | A Comprehensive Analysis of Medieval Cats and Dogs: Myth, Reality, and Symbolism | high_redundancy_risk;low_topic_heading_overlap |
| 53 | Entertainment & Fashion | 0.1667 | An Economic Deep Dive into the Currency of Zemuria | empty_references;low_citation_density;high_redundancy_risk;low_topic_heading_overlap |
| 98 | Other | 0.1765 | The Nature of Yordle Mortality: An Analysis of Immortality and Resurrection in Runeterra | empty_references;high_redundancy_risk;low_topic_heading_overlap |
| 12 | Science & Technology | 0.1778 | A Deep Research Report on a Novel Cationic Porphyrin for Dual-Action Antimicrobial Applications | empty_references;low_citation_density;low_topic_heading_overlap |

## Metric Notes

- `top_redundancy_risk` is a deterministic lexical/citation-overlap proxy, not an LLM judge score.
- `topic_keyword_coverage` is the fraction of non-stopword topic keywords found in the report title/headings.
- `audit_risk_score` is the number of static flags triggered for a report.
- The audit is meant to triage reports before paid LLM judging and to surface corpus-level failure patterns.
