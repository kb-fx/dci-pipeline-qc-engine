# Automated DCI Theatrical QC Pipeline

A context-aware Python automation utility designed to parse and validate Digital Cinema Package (DCP) media assets against strict theatrical distribution standards.

## Overview
Authoring theatrical deliverables requires strict adherence to DCI (Digital Cinema Initiatives) specifications. Manually verifying MXF media containers via GUI interfaces is time-consuming and prone to human error. This utility acts as an automated "gatekeeper," utilizing FFmpeg/FFprobe as a backend engine to interrogate media headers, calculate real-world bitrates, and flag critical compliance failures before distribution.

## Key Features
* **Context-Aware Asset Parsing:** Dynamically identifies whether the target MXF container is a Video or Audio essence to prevent false-positive failures inherent in component-media structures.
* **Bandwidth Limit Verification:** Calculates exact Megabits-per-second (Mbps) using raw byte-size and duration to ensure the JPEG2000 codestream stays strictly beneath the 250 Mbps hardware ceiling, preventing theater projector crashes.
* **Audio Matrix Validation:** Scans the audio layout to ensure a minimum of 6 discrete channels (5.1 surround format) are present, satisfying mandatory digital cinema ingestion requirements.

## System Requirements
* Python 3.x
* FFmpeg & FFprobe (Must be configured in the system environment variables PATH)

## Usage
1. Place `qc_verifier.py` in your project root directory.
2. Update the `target_file` variable with the absolute or relative path to your DCP's Video or Audio `.mxf` file.
3. Execute the script via terminal:

```bash
python qc_verifier.py

## Example Output
Initializing Media Pipeline Quality Control Check...

========================================
      DCI COMPLIANCE REPORT CACHE       
========================================

[FAIL] Audio Matrix : Only 0 channels detected! Theater servers require 6 or 8.
[PASS] Bandwidth    : 240.02 Mbps (Safe beneath 250 Mbps limit).

========================================
