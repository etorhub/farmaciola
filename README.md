# Farmaciola

[![HACS][hacs-badge]][hacs-url]
[![GitHub Release][release-badge]][release-url]
[![License: MIT][license-badge]][license-url]
[![Home Assistant][ha-badge]][ha-url]

A Home Assistant custom integration that turns your instance into a smart medicine cabinet — with CIMA-powered medicine lookup, expiry tracking, and a dedicated Lovelace panel.

---

## Features

- **Dedicated Lovelace panel** — browse and manage all your medicines in one place, without editing any YAML
- **CIMA medicine search** — look up any medicine registered with the Spanish Agency of Medicines (AEMPS) and import its name, manufacturer, and photo with one tap
- **Expiry tracking** — set expiry dates and get automatic reminders during the expiry month
- **Dashboard stats bar** — see at a glance how many medicines are OK, expiring soon, or already expired; click any card to filter the list
- **Persistent storage** — your medicine data is stored locally and survives restarts

---

## Installation via HACS (recommended)

[![Open your Home Assistant instance and add this repository to HACS.][hacs-my-badge]][hacs-my-url]

1. Click the button above (or open HACS → Integrations → ⋮ → Custom repositories and add `etorhub/farmaciola` with category **Integration**).
2. Search for **Farmaciola** and click **Download**.
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration** and search for **Farmaciola**.

---

## Manual installation

1. Download the [latest release][release-url] and copy the `custom_components/farmaciola` folder into your `config/custom_components/` directory.
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration** and search for **Farmaciola**.

---

## Configuration

During setup you can optionally set a default **notify service** (`notify.notify` by default). That value seeds the panel settings on first run.

**Reminder delivery** is configured in the Farmaciola panel: open the sidebar app and click **Reminders** in the header. There you can:

- Turn expiry reminders on or off
- Choose **Notification center** (Home Assistant bell), **Mobile push**, or both
- Pick which `notify.*` service receives mobile alerts (dropdown of services discovered in your instance)

---

## Usage

Once installed, a **Farmaciola** entry appears in your Home Assistant sidebar.

### Adding a medicine

1. Open the Farmaciola panel and click **Add medicine**.
2. Use the **Search CIMA** tab to find the medicine by name — this auto-fills the details from the official registry.
3. Or use the **Manual** tab to enter the name yourself.
4. Set an expiry date if you want to receive alerts.
5. Click **Save**.

### Expiry alerts

Farmaciola checks expiry dates every 24 hours. When the calendar reaches a medicine's **expiry month**, you receive a reminder through the channels you enabled in **Reminder settings**. Each medicine notifies only once. If reminders are disabled, nothing is sent and medicines remain eligible for a future alert when you turn reminders back on.

### Stats bar

The panel header shows three cards — **Total**, **Expiring** (≤ 30 days), and **Expired**. Click any card to filter the list to that subset.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

- Follow [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages.
- Include tests for behaviour changes.
- Ensure CI passes before requesting review.

### Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements_test.txt -r requirements_dev.txt
pre-commit run --all-files
pytest
```

---

## License

Distributed under the [MIT License](LICENSE).

---

[hacs-badge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[hacs-url]: https://hacs.xyz
[release-badge]: https://img.shields.io/github/v/release/etorhub/farmaciola?style=flat-square
[release-url]: https://github.com/etorhub/farmaciola/releases/latest
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
[license-url]: LICENSE
[ha-badge]: https://img.shields.io/badge/Home%20Assistant-integration-41BDF5?style=flat-square&logo=home-assistant
[ha-url]: https://www.home-assistant.io
[hacs-my-badge]: https://my.home-assistant.io/badges/hacs_repository.svg
[hacs-my-url]: https://my.home-assistant.io/redirect/hacs_repository/?owner=etorhub&repository=farmaciola&category=integration
