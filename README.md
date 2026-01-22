Multilingual Invoice Information Extraction System
Overview

This project implements an end-to-end document understanding pipeline to extract structured information from tractor invoices and quotations with unknown layouts, multiple Indian languages, and scanned image noise.

The system is designed for cloud execution, low latency, and cost-efficient inference, aligned with the evaluation criteria of DLA, latency, and inference cost.

Invoice Image
     │
     ▼
Image Preprocessing
     │
     ▼
OCR (EasyOCR – multilingual)
     │
     ▼
Layout Grouping (Header / Body / Footer)
     │
     ▼
Rule + Fuzzy Field Extraction
     │
     ├── Dealer Name
     ├── Model Name
     ├── Horse Power
     ├── Asset Cost
     │
     ▼
Vision Validation
     ├── Signature Detection
     └── Stamp Detection
     │
     ▼
Confidence Scoring
     │
     ▼
Structured JSON Output


OCR Capabilities

Engine: EasyOCR

Languages Supported:

English

Hindi

Gujarati

Handles:

Printed text

Handwritten text

Low-quality scans

Rotated documents
