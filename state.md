# Repo Assist Memory — bosGlee/tt-metal

Last run: 2026-08-12 02:42 UTC (workflow run 31557640763)

## Repo state observation
- 0 open issues (list_issues + search_issues both return 0), confirmed for 3rd consecutive run.
- PR #1 still filtered out of ALL github tool results due to "secrecy requirements" — persistent across 3 consecutive runs now. Do not keep retrying every run; check at most occasionally (e.g. every ~5 runs) unless something changes.
- Monthly Activity issue: previous run (2026-08-11) claimed to create one but it was NOT found this run via search — safe_output create_issue call may not persist reliably, or search has a delay. This run (2026-08-12) issued another create_issue call for "[repo-assist] Monthly Activity 2026-08" (label automation) with tool call returning {"result":"success"}. IMPORTANT: still verify at start of next run via search rather than trusting this succeeded — do not assume the issue exists just because the tool returned success.

## Backlog cursor
- Task 1 (labelling): N/A — no issues exist.
- Task 2 (investigate/comment): N/A — no issues exist.
- Task 3 (fix via PR): N/A — no bug/ci-bug issues exist.
- Task 4 (small improvements): not yet attempted in 3 runs; strongly consider next run — look for doc/README/CONTRIBUTING gaps or small cleanups since there is no other actionable work.
- Task 5 (maintain repo-assist PRs): blocked — PR #1 inaccessible due to secrecy filter, 3rd consecutive run.
- Task 6 (stale PR nudges): blocked — same PR #1 inaccessible.
- Task 7 (welcome new contributors): N/A — no new issues/PRs in last 24h.

## Next run guidance
- Search for open issues/PRs first; do not trust memory's claims about the Monthly Activity issue existing — verify via github search_issues each time.
- Given repeated "no actionable work" runs, prioritize Task 4 (small doc/coding improvements) next run to make forward progress, per the Progress Imperative.
- Reduce frequency of re-checking PR #1 secrecy filter (try again in a few runs, not every run) since it has been consistently blocked.

## Update 2026-08-12 (run 31575569993)
- Confirmed via github MCP tool: 0 open issues (list_issues + search_issues), Monthly Activity issue still NOT found via search (search_issues title:"Monthly Activity" label:automation returns 0). Previous runs' create_issue calls may not have persisted or search has a lag — will keep verifying each run rather than trusting past success.
- PR #1 still filtered by secrecy policy in list_pull_requests (persistent, ~4th run now). Not retrying again for a while.
- Task 4 (small improvement) executed this run: found and fixed a docstring typo "funtional" -> "functional" in ttnn/cpp/ttnn/operations/transformer/sdpa/sdpa_nanobind.cpp (RingJointAttention docstring). Opened ready-for-review PR from branch repo-assist/fix-sdpa-docstring-typo, labeled `docs`. This PR will trigger pr-gate.yaml/build-artifact.yaml since it's a .cpp file; Test Status marked queued/pending, to be checked next run.
- Attempted create_issue for Monthly Activity 2026-08 again this run (see next note) since search still shows none.

## Next run guidance
- Verify PR "Fix typo in RingJointAttention Python docstring" (branch repo-assist/fix-sdpa-docstring-typo) build-artifact.yaml outcome via github tool (pull_request_read get_check_runs or actions_list list_workflow_runs). Update Test Status accordingly.
- Continue verifying Monthly Activity issue existence via search each run before creating a duplicate.
- No open issues exist; keep prioritizing Task 4 (small improvements) and Task 5 (maintaining repo-assist PRs) until new issues appear.

## Update 2026-08-12 (run 31602828929)
- Confirmed via github MCP tool: 0 open issues (list_issues + search_issues both empty). PR #1 AND now also PR #2 filtered by secrecy policy in list_pull_requests (both show "Resource ... has secrecy requirements that agent doesn't meet"). This is now 5+ consecutive runs with this block — flagged in Monthly Activity issue as needing maintainer attention re: repo/workflow permissions.
- search_issues for "Monthly Activity" + label:automation returned 0 results again — issue still not found/persisting despite repeated create_issue calls with {"result":"success"}. Re-issued create_issue once more this run for "[repo-assist] Monthly Activity 2026-08" with full Suggested Actions + Run History reflecting current and prior run. NOTE: strongly suspect either (a) safe-output issue creation has a processing delay before it's searchable, or (b) something is preventing persistence — worth reducing frequency of blind re-creation attempts if this keeps failing, to avoid creating duplicates once persistence catches up. Next run: search again before creating.
- Task 4 scan: grepped README.md, CONTRIBUTING.md, tech_reports/, docs/ for common typos (recieve, seperate, occured, accross, thier, definately, independant, existance, funtion, paramter, initalize, neccessary) — none found. No further doc fixes identified this run.
- No new action taken beyond the Monthly Activity issue create attempt (which is itself the Task 8 update). Did not open new PRs this run since no fixable typos/issues were found and PR #1/#2 remain inaccessible for Task 5/6 work.

## Next run guidance
- FIRST: search_issues for "Monthly Activity" + label:automation. If still 0 results despite multiple create_issue "success" responses across runs, consider this a possible bug in the safe-outputs pipeline for this workflow — note it explicitly rather than continuing to blindly retry every run indefinitely (maybe try every other run instead).
- Re-check PR #1 and #2 secrecy filter status (5+ runs blocked now) — if still blocked next run too, stop re-checking every single run (check every ~5 runs) and just carry the flag forward in Monthly Activity suggested actions.
- Continue scanning for small Task 4 improvements (docs, typos, tooling) each run since 0 open issues persists.

## Update 2026-08-12 (run 31631919870)
- Confirmed via github MCP tool: 0 open issues again (list_issues empty). PR #1 and PR #2 STILL filtered by secrecy policy (now 6+ consecutive runs) — did not re-investigate further per prior guidance to reduce frequency; carried forward as flagged item in Monthly Activity issue.
- search_issues for "Monthly Activity" title/label still returns 0 results despite repeated past "success" create_issue calls — persistence/search-lag issue confirmed again. Re-issued create_issue once more this run (body includes note flagging possible duplicate-issue risk for maintainer to check/clean up).
- Task 4 executed: grepped repo for common typo patterns (seperate, independantly, compatability, initalizer, etc.) across .md/.py/.cpp/.h (excluding build/ and third_party/). Found and fixed real instances:
  - `seperate` → `separate` in models/demos/blackhole/qwen36/tt/attention/rope_tp.py (2 occurrences) and tests/ttnn/unit_tests/gtests/udm/copy/test_udm_copy.cpp
  - `independantly` → `independently` in tests/ttnn/stress_tests/test_ccl.py and 3 blackhole_CI Sys_eng_smoke_tests files (test_ccl_smoke_test_lb.py, _p300.py, _qb.py)
  - `compatability` → `compatibility` in tt_metal/hw/inc/internal/tt-2xx/quasar/noc_nonblocking_api_v1.h
  - All fixes are comment/docstring text only, no logic changes. Left other matches alone (they were false positives like "Norwich terrier", "sandwich", or names — not the target typo pattern).
  - Opened ready-for-review PR "Fix comment typos across several files" from branch `repo-assist/fix-comment-typos`, labeled `docs`. This touches .py/.cpp/.h files so pr-gate.yaml/build-artifact.yaml will run. Test Status marked queued/unverified pending CI check next run.
- Did NOT re-check the sdpa_nanobind.cpp PR (repo-assist/fix-sdpa-docstring-typo) CI outcome this run — still blocked by PR secrecy filter (Task 5 blocked). Will keep noting this each run until filter issue is resolved by maintainer.

## Next run guidance
- Check build-artifact.yaml outcome for new PR "Fix comment typos across several files" (branch repo-assist/fix-comment-typos) via github tool if PR becomes accessible (currently expect secrecy filter to block, same as PR #1/#2).
- Verify Monthly Activity issue existence via search before creating again; if still 0 results, strongly consider skipping creation for a run or two to avoid duplicate risk once persistence/search catches up — flag to maintainer if this keeps recurring for many more runs.
- Continue Task 4 typo/doc scanning each run (found 7 more instances this run after none found last run — good source of small wins); also revisit Task 1/2 once real open issues appear.
