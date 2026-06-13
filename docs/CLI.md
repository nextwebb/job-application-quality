# CLI

`jobqa` is the simplest way to use Job Application Quality.

The plugin and skills make the workflow available to agents. The CLI is the human-friendly front door.

## Commands

```bash
./bin/jobqa demo
./bin/jobqa init my-application
./bin/jobqa run my-application
./bin/jobqa qa my-application/output/manifest.json
./bin/jobqa report my-application/output/manifest.json --format markdown
```

## Workspace Layout

`jobqa init my-application` creates:

```text
my-application/
  candidate.json
  role.json
  artifacts/
    cv.txt
  output/
```

## Exit Codes

- `jobqa demo` exits `0`; it is an explanatory demo even though the sample packet stops.
- `jobqa run` exits `1` when artifact QA fails.
- `jobqa qa` exits `1` when artifact QA fails.
- `jobqa report` exits `0`; it only prints the latest report.

## Output Formats

`run`, `qa`, and `report` support:

```bash
--format text
--format markdown
--format json
```

Use JSON for agent or CI integration. Use Markdown for human review.

## Design Rule

The public CLI stays small. Internal scripts can remain detailed, but the front door should answer one question:

```text
Can this packet be reviewed for submission, or should it stop?
```
