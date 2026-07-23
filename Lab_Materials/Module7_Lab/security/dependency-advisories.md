# Dependency advisories — Acme Customer Portal (fixed exercise snapshot)

_(This stable scenario is used when live Dependabot results differ or are unavailable. Advisory facts
were checked against the GitHub Advisory Database on **2026-07-23**. Live results will change as new
advisories are published. Triage locally in VS Code; do not use Autofix. Prioritise by reachable exposure,
not badge colour.)_

| ID | Advisory | Package | Installed | Fixed in | Severity | Verified condition | Acme reachability context |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADV-1 | [GHSA-9hjg-9r4m-mvj7](https://github.com/advisories/GHSA-9hjg-9r4m-mvj7) | `requests` | 2.25.1 | 2.32.4 | **Moderate** | A maliciously crafted URL can leak `.netrc` credentials. | KYC workers have `.netrc` credentials and follow a provider-returned URL. Confirm whether that URL can be influenced or the provider can redirect it. |
| ADV-2 | [GHSA-8q59-q68h-6hv4](https://github.com/advisories/GHSA-8q59-q68h-6hv4) | `pyyaml` | 5.3.1 | 5.4 | **Critical** | `full_load` / `FullLoader` can execute code from untrusted YAML. | The known path uses `yaml.safe_load` on trusted, in-repo `app-config.yaml`; search for any untrusted YAML and unsafe loader before ranking it. |
| ADV-3 | [GHSA-h75v-3vvj-5mfj](https://github.com/advisories/GHSA-h75v-3vvj-5mfj) | `jinja2` | 2.11.3 | 3.1.4 | **Moderate** | User-controlled **keys** passed to `xmlattr` can inject HTML attributes and enable XSS; user-controlled values alone are not this flaw. | The HTML reset-email template passes customer-defined profile-field names as `xmlattr` keys, so this path is reachable. |
| ADV-4 | [GHSA-44wm-f244-xhp3](https://github.com/advisories/GHSA-44wm-f244-xhp3) | `pillow` | 8.1.0 | 10.3.0 | **High** | A buffer overflow exists in Pillow's `_imagingcms.c`. | The portal does not process images and no import is known. Determine why the direct dependency exists; removal is preferable if unused. |
| ADV-5 | [GHSA-34jh-p97f-mpxf](https://github.com/advisories/GHSA-34jh-p97f-mpxf) | `urllib3` | 1.26.4 | 1.26.19 | **Moderate** | `Proxy-Authorization` was not stripped on cross-host redirects. | `requests` depends on it and this snapshot also pins it directly; no proxy credentials are expected in production. Confirm runtime proxy configuration. |

## What a good triage produces
For each advisory: **is it reachable in our system?**, **what is the real exposure?**, **what is the fix
(bump / remove / mitigate)?**, and **who owns it by when?** An unreachable Critical can rank below a
reachable High. Say which you would do first, and why — and flag anything that should ride the next
release versus needing an out-of-band patch. Even a lower-ranked vulnerable dependency still needs an
owned remediation or an evidence-backed, time-bounded exception.

> A dependency you don't actually use is best **removed**, not bumped.
