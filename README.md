```markdown
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
```

# bsn-generator
Python tool for generating valid and invalid Dutch BSN numbers for testing purposes.  
This utility uses the official 11-test (11-proef) (BSN variant) to create numbers suitable for testing purposes.

---

## Features
- Generate valid BSNs (11-test compliant)
- Generate invalid BSNs for negative testing
- Colorised CLI output (valid vs invalid)
- Stats summary after generation
- Save results to a .txt file

## Installation
Clone the repository and run the script:

```bash
git clone https://github.com/asifnawazminhas/bsn-generator
cd bsn-generator
python3 bsn_generator.py --help
```

## Generate 10 valid BSNs:
```bash
python3 bsn_generator.py --type valid --count 10 --output valid_bsns.txt
```

## Generate 10 invalid BSNs:
```bash
python3 bsn_generator.py --type invalid --count 10 --output invalid_bsns.txt
```

## Output example (valid_bsns.txt)
```bash
202760352
286569632
20160100
577090501
523728712
750528126
465910506
953627251
594900062
868905215
```

## Output example (invalid_bsns.txt)
```bash
786960614
581920007
131105738
463837611
316283116
941171818
341034738
206682226
366299735
881739257
```

---
## Notes

These BSNs are synthetic and automatically generated using mathematical rules.
They do not correspond to real individuals and are intended solely for testing applications that require BSN validation logic.
