# Browser Workflow

Use browser automation only after policy gates pass.

1. Open official ATS/company URL.
2. Inspect form fields.
3. Compare each field against tenant policy.
4. Upload only manifest-approved artifacts.
5. Stop for explicit approval before final submit.
6. Stop for every CAPTCHA and request current challenge approval.
7. Record submission result or block reason.

Do not rely on hidden CAPTCHA inputs as visible challenges. Confirm visually or through interactable DOM.

