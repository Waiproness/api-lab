# API lab results

Observations from QuickPizza on 9 November 2026. The service is shared and results can change.

## Part 0

- Step 0.1: 18 pizza names.
- Step 0.3: 401 without a token.
- Step 0.4: A Nasty Pugliese (the name is random).
- Step 0.12: Three separate pytest runs without a session all failed: user creation returned 201 and login returned 401 on each run. The temporary flaky test was removed afterwards.
- Step 0.16: Number of excluded tools: 0, 1, 2, or 3. Excluding all 3 exposed the defect.

## Defect report

- Title: Excluding all cutting tools returns a server error.
- Request: `POST /api/pizza`, with a valid user token and body `{"excludedTools":["Knife","Pizza cutter","Scissors"]}`.
- Expected: 400 and a JSON error message explaining that the request cannot be satisfied.
- Actual: 500 with an empty body.
- Severity: Medium: an allowed input causes an unexpected server error and gives the client no actionable explanation, but the observed impact is limited to the request.

## Part A

- Other user reading the rating: 404; changing it: 400; deleting it: 400.
- Step A2: `curl` returned HTTP 400 for decimal stars (`json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int`), text stars (`json: cannot unmarshal string into Go struct field Rating.stars of type int`), missing stars (`number of stars must be between 1 and 5 (inclusive)`), and a nonexistent pizza (`pizza ID 999999999 not found`). Missing and short tokens both returned HTTP 401 with `authentication failed`. The requests used a new fictional user and a cookie jar; `curl_checks.py` reproduces them.
- Final full run: 32 passed, 1 xfailed; see report.html. The test user's token in the report was redacted before publication.

## Part B

1. Real API tests can find a client/server integration mismatch and a failure in the real database or deployment. Stubbed unit tests are also useful because they run quickly and isolate a function when a failure occurs.
2. A unique user gives each test its own ratings and prevents interference with shared data. For Project 2 I would create unique test records for my group and clean up only those records.
3. A session retains the AWSALB cookie so the load balancer routes the requests to the same server, where the newly created user exists. In all three optional pytest runs without a session, creation returned 201 but login returned 401. This is consistent with requests reaching different servers, though these three results alone do not prove the route taken.
4. Excluding all three tools revealed the defect. A 500 with no body offers no useful reason to a client and suggests a server failure; a 400 with a message lets the client explain the invalid request. The strict xfail preserves the defect as a visible regression check and signals when it passes.
5. Base choice needs 1 + (3-1) + (4-1) + (2-1) + (3-1) = 9 cases. All combinations need 3 × 4 × 2 × 3 = 72 cases.
6. Read returned 404, update 400, and delete 400. A 403 or 404 would also be plausible ways to deny access. All three responses refused access, and the owner's rating remained unchanged; the differing 400 codes alone do not establish an authorization defect, although a consistent documented contract would help clients.
7. `GET /api/ratings` with the made-up 16-character token returned 200 and a list of ratings. Treating a made-up token as authenticated is an authentication defect: on a real system a stranger could read data exposed to that token. Only a read was performed; no mutation was attempted with it.
8. API tests check status codes and JSON fields directly. Browser tests can check visible layout and whether a user can operate the interface.
