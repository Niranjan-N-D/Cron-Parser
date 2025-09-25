# Cron Expression Parser

## Overview
This is a **Python command-line tool** that parses standard cron expressions (five time fields + command) and expands each field into the exact times when it will run.  

It supports the standard cron fields:

- Minute (0–59)
- Hour (0–23)
- Day of Month (1–31)
- Month (1–12)
- Day of Week (0–6, Sunday = 0)

**Note:** Special strings like `@yearly`, `@daily`, `@hourly` are intentionally **not supported**.

---

## Features
- Expands wildcards (`*`)
- Handles step values (`*/n`)
- Handles ranges (`a-b`) and lists (`a,b,c`)
- Outputs a formatted table where the field name occupies the first 14 columns
- Works entirely from the command line

---

## Installation

1. Make sure you have **Python 3.x** installed:  
```bash
python --version

