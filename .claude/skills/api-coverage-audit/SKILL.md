---
name: api-coverage-audit
description: "Compare this SDK's implemented endpoints against the inMotion server's live Play route definitions to find unimplemented or changed API surface. Use when asked to check SDK coverage, find missing endpoints, check for API drift, or audit the SDK against the inmotion-api routes. Triggers on: 'what endpoints are missing', 'check API coverage', 'has the API changed', 'audit routes', 'sync SDK with routes'."
---

# API Coverage Audit

Compares `inmotion-python-sdk` (this repo) against the server-side route definitions in the
sibling `inmotion` repo, to find:

1. **API areas with zero SDK coverage** (a whole `.routes` file with no corresponding SDK module).
2. **Individual endpoints missing** from an otherwise-implemented SDK module.
3. **Drift**: SDK code that calls a URL shape the server no longer exposes (renamed/restructured
   routes) — these are worse than "missing", since they compile but fail at runtime.

## Inputs

- Server routes: `/Users/waring/source/inmotion/inmotion/modules/inmotion-api/conf/*.routes`
  (note: extension is `.routes`, not `.route`). Ignore `target/` copies — only the ones directly
  in `conf/` are authoritative.
- SDK source: `/Users/waring/source/inmotion/inmotion-python-sdk/inmotion/*.py`

## Step 1 — Extract the route inventory

Each `.routes` file is Play Framework syntax: `METHOD  /path  @controller.action(args)`, often
preceded by a `# summary: ...` OpenAPI comment. `inmotion.routes` is the router that mounts each
module file at a path prefix (e.g. `-> /api/latest/account account.Routes`) and also defines a
handful of routes directly inline. Extract every route with method, path, controller action, and
summary using a script like:

```python
import re
files = ["event.routes","account.routes","upload.routes","authenticate.routes","activities.routes",
         "datastream.routes","folio.routes","site.routes","track.routes","datastreams.routes",
         "devkey.routes","user.routes","apikey.routes","activity_config.routes","admin.routes",
         "inmotion.routes"]
for fname in files:
    summary = None
    for line in open(fname):
        m = re.match(r'#\s*summary:\s*(.+)', line)
        if m: summary = m.group(1).strip(); continue
        m2 = re.match(r'^(GET|POST|PUT|DELETE|PATCH)\s+(\S+)\s+(.+)$', line)
        if m2:
            method, path, action = m2.groups()
            print(fname, method, path, action.strip(), summary)
            summary = None
```

Route file → URL mount prefix (from `inmotion.routes`):

| Routes file | Mount prefix |
|---|---|
| `authenticate.routes` | `/api/latest/authenticate` |
| `user.routes` | `/api/latest/user` |
| `account.routes` | `/api/latest/account` |
| `apikey.routes` | `/api/latest/apikey` |
| `devkey.routes` | `/api/latest/devkey` |
| `activities.routes` | `/api/latest/activities` |
| `track.routes` | `/api/latest/activity/track` |
| `site.routes` | `/api/latest/activity/site` |
| `activity_config.routes` | `/api/latest/activity-config` (routes already include this segment) |
| `upload.routes` | `/api/latest/upload` |
| `event.routes` | `/api/latest/events` |
| `datastream.routes` | `/api/latest/data-stream` |
| `datastreams.routes` | `/api/latest/data-streams` |
| `folio.routes` | `/api/latest/folio` |
| `admin.routes` | `/api/latest/admin` |
| `inmotion.routes` | (root — defines its own full paths, e.g. `/api/latest/accounts`, `/api/latest/otc`) |

Ignore anything marked `### NoDocs ###` or routed to a controller ending in `Old` (e.g.
`ActivitiesControllerOld`, `APIAuthControllerOld`, `findByFilterOld`) — these are deprecated
back-compat shims, not current surface.

`admin.routes` is operator/back-office tooling (user/account provisioning across the whole
system) — treat as out of scope for this SDK unless the user says otherwise; don't flag its
endpoints as gaps.

## Step 2 — Map routes files to SDK modules

| Routes file | SDK module | ABC in `inmotion/api.py` |
|---|---|---|
| `account.routes` | `inmotion/accounts.py` | `InMotionAccounts` |
| `track.routes` / `site.routes` / `activities.routes` | `inmotion/activities.py` | `InMotionActivities` |
| `activity_config.routes` | `inmotion/activity_config.py` | `InMotionActivityConfig` |
| `apikey.routes` | `inmotion/apikey.py` | `InMotionApiKeys` |
| `devkey.routes` | `inmotion/devkey.py` | `InMotionDevKeys` |
| `datastream.routes` / `datastreams.routes` | `inmotion/datastream.py` | `InMotionDataStream` |
| `folio.routes` | `inmotion/folio.py` | `InMotionFolio` |
| `upload.routes` | `inmotion/upload.py` | `InMotionUpload` |
| `user.routes` | `inmotion/user.py` | `InMotionUser` |
| `authenticate.routes` | `inmotion/apikey_client.py` / `inmotion/credentials_client.py` | (session bootstrap, not an activities ABC) |
| `event.routes` | `inmotion/event.py` | `InMotionEvents` |
| `admin.routes` | *(out of scope)* | — |

Root-level routes defined directly in `inmotion.routes` (not under a sub-module prefix) land in
whichever ABC matches their OpenAPI `tags` comment: `master-data`/analytics → `InMotionActivities`,
`device-config` (global) + `findMyAccounts` → `InMotionAccounts`, `otc` → `InMotionUser`.

For each SDK impl file, grep the literal path segments passed to `request_json`/`request_raw`
(look for `self._prefix_path` string interpolations) and match HTTP method + path shape against
the route inventory from Step 1. Matching is structural (e.g. `/account/{account_key}/users` ~
`/:accountKey/users`), not textual.

## Step 3 — Classify and report

For every route in the inventory (minus deprecated/admin), classify as:

- **Implemented** — a matching method+path exists in the mapped SDK module.
- **Missing** — no SDK module exposes it, or the mapped module exists but lacks this specific
  endpoint.
- **Drift** — SDK code calls a URL shape that doesn't correspond to any current route in that
  file (this is the most serious: the SDK compiles but the call will 404/error at runtime). This
  happens when a route file's shape has clearly changed (e.g. renamed resource, restructured
  path) — compare the *set* of path shapes on both sides, not just count them.

Report grouped by API area, most severe first (drift > whole-area gaps > individual missing
endpoints). For each finding give: HTTP method + path, the summary text from the route comment,
and the SDK file/method it should live in (or does live in, if drift).

## Known findings as of 2026-08-04, resolved same day (re-verify, don't trust blindly — routes and SDK both move)

All gaps found in the 2026-08-04 audit were addressed the same day:

- **Drift — `inmotion/folio.py`** was rewritten from the old two-level FolioSet→Folio model to
  the current flat `/folio`, `/folio/{key}`, section/item sub-resource shape. `FolioSetModel`/
  `FolioSetDetailsModel`/`FolioStreamModel` were removed from `models.py`.
- **Missing area — Event API**: added `inmotion/event.py` + `InMotionEvents` ABC, wired into both
  session implementations via `session.events()`.
- **Missing endpoints — Account Management**: added Standard Data Type/Variant Type CRUD and the
  full Device Config lifecycle to `InMotionAccounts`/`accounts.py` (raw-dict returns, since the
  server declares no fixed response schema for these).
- **Missing endpoints — Activities**: added `batch_record_update`, `find_activity_analytics`,
  `find_activity_track_metrics`, `find_activity_variable_stats`, `find_activity_master_data`,
  `find_latest_activity_stats_by_type` to `InMotionActivities`/`activities.py`.
- **Missing endpoints — Upload**: added `upload_diagnostics`.
- **Missing root-level endpoints**: added `find_my_accounts`/`fetch_global_device_configs`/
  `sync_device_configs` to `InMotionAccounts`, and `create_otc` to `InMotionUser`.
- The `create_user_against_account`/`userKey` naming question was left as-is (unconfirmed, not
  reproduced as an actual bug) — flag again on a future audit if it resurfaces.
- Unrelated pre-existing issue in `CLAUDE.md` about `credentials_client.py` broken imports no
  longer reproduces — that file already uses correct `inmotion.` prefixed imports.

When this skill is re-run in the future and finds no gaps, replace this whole section with a
one-line "clean as of \<date\>" note rather than letting stale resolved-findings prose accumulate.
