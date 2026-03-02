# Invoice Intake Agent (OpenAI Agents SDK)

## Overview

This project implements an automated invoice-intake workflow using the
OpenAI Agents SDK.

The agent processes:

1.  An inbound email (local JSON file)
2.  A PDF invoice attachment
3.  Extracts structured invoice data (including fields embedded inside
    images)
4.  Generates a notification for Customer Service with:
    -   A human-readable summary
    -   A structured JSON payload suitable for downstream systems

The system is designed to balance: - Structured LLM-based extraction -
Deterministic Python-based formatting - Controlled token usage -
Reliability under limited API credits

------------------------------------------------------------------------

## Architecture

The system follows a hybrid agentic design:

### 1. Agent Layer

The agent: - Decides which tool to call - Executes tools sequentially -
Stops when the workflow is complete

The workflow is not hard-coded in order. The model determines when to: -
Call `extract_invoice_data` - Then call `send_notification`

A loop is used to allow multi-step tool execution until completion.

------------------------------------------------------------------------

### 2. Extraction Tool

The `extract_invoice_data` tool:

-   Reads inbound email JSON
-   Extracts text from PDF
-   Renders PDF pages to images (for vision-based extraction)
-   Calls `gpt-5-mini` for structured extraction
-   Validates output using Pydantic schema

Design decisions: - PDF text is truncated to control token usage -
Vision input is used to ensure invoice number extraction from header
images - Strict JSON schema reduces hallucination risk - Pydantic
validation ensures structured integrity

------------------------------------------------------------------------

### 3. Notification Tool

The `send_notification` tool:

-   Accepts validated structured invoice data
-   Writes:
    -   `output/outbound_email.json`
    -   `output/outbound_email.txt`
-   Builds a deterministic summary in Python

The LLM is not used for final formatting.\
Formatting is handled in Python to: - Prevent mutation of financial
values - Reduce token cost - Improve reliability

------------------------------------------------------------------------

### 4. Hybrid Data Integrity Strategy

Although the workflow is agent-driven, structured invoice data is stored
locally after extraction and reused during notification.

This avoids: - Re-serialization of large JSON payloads - Token waste -
Risk of the model mutating structured data

The agent controls sequencing.\
Python guarantees deterministic data flow.

------------------------------------------------------------------------

## Project Structure

    invoice_agent/
      ├── agent.py
      ├── schemas.py
      └── tools/
            ├── extract_invoice.py
            └── notify.py

    data/
      ├── Email.json
      └── Invoice.pdf

    main.py

------------------------------------------------------------------------

## Setup

This project uses `uv` for environment management.

1.  Install dependencies:

```{=html}
<!-- -->
```
    uv sync

2.  Create a `.env` file in the root directory:

```{=html}
<!-- -->
```
    OPENAI_API_KEY=your_api_key_here

Ensure `.env` is not committed to GitHub.

------------------------------------------------------------------------

## Run

From the project root:

    uv run python main.py --email data/Email.json --pdf data/Invoice.pdf

------------------------------------------------------------------------

## Output

The system generates:

    output/outbound_email.json
    output/outbound_email.txt

-   `outbound_email.json` → structured invoice payload
-   `outbound_email.txt` → human-readable summary for Customer Service

------------------------------------------------------------------------

## Design Considerations

### Hallucination Reduction

-   Strict JSON schema
-   Clear extraction instructions
-   Null for missing fields
-   Pydantic validation layer
-   Deterministic formatting in Python

### Token & Cost Control

-   PDF text truncation
-   Limited page rendering
-   No LLM usage for formatting
-   Hybrid structured data reuse

### Scalability

The architecture can be extended to: - Support multiple PDF
attachments - Chunk large invoices by logical sections - Add validation
checks (e.g., subtotal + taxes = total) - Add duplicate invoice
detection - Add retry logic for extraction failures

------------------------------------------------------------------------

## Future Improvements

Potential enhancements include:

-   Confidence scoring for extracted fields
-   Cross-validation of financial totals
-   Logging and monitoring
-   Duplicate invoice detection
-   Support for batch email processing
-   Unit tests with mocked LLM responses

