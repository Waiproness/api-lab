# QuickPizza API lab

Individual API testing exercise using pytest and requests. Tests create unique fictional users, keep load-balancer cookies in one session, and delete ratings they create. The public practice token is used only for pizza and tool requests, never to change ratings.

## Setup and run (Windows PowerShell)

Requires Python 3.10 or later and network access to QuickPizza.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v --html=report.html --self-contained-html
```

The expected defect test is marked strict xfail. An XPASS signals that its mark should be reviewed. Test results depend on the shared service and may change. See RESULTS.md for observations.

## Input domain for POST /api/ratings

Each non-base case changes one characteristic while keeping the others at the base. `test_base_choice_is_saved` covers all base blocks. The resulting base choice suite has nine cases.

| Characteristic | Block and representative value | Covering test |
|---|---|---|
| Stars value | Below 1: 0 | `test_stars_out_of_range[0]` |
| Stars value | 1–5: 3 (base) | `test_base_choice_is_saved` |
| Stars value | Above 5: 6 | `test_stars_out_of_range[6]` |
| Stars type | Integer: 3 (base) | `test_base_choice_is_saved` |
| Stars type | Decimal: 3.5 | `test_invalid_stars_type[decimal]` |
| Stars type | Text: "3" | `test_invalid_stars_type[text]` |
| Stars type | Missing | `test_invalid_stars_type[missing]` |
| Pizza | Existing (base) | `test_base_choice_is_saved` |
| Pizza | Missing: 999999999 | `test_nonexistent_pizza` |
| Token | Owner's token (base) | `test_base_choice_is_saved` |
| Token | Missing | `test_invalid_token[missing]` |
| Token | Wrong length: short | `test_invalid_token[short]` |
