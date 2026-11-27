# PartSouq OEM Auto Parts Price, Stock & Cross-Reference Scraper

Extract real-time **OEM and aftermarket automotive parts pricing (USD), warehouse stock quantity, dispatch lead time, country of origin (`Made in`), and compatible cross-reference replacements** directly from [PartSouq](https://partsouq.com) by part number.

Built for automotive parts distributors, export/import wholesalers, repair shop ERP integrations, eBay/Amazon Motors sellers, and AI procurement agents.

---

## Key Features

- **Bulk Part Number Lookup:** Query dozens or hundreds of OEM/aftermarket part numbers in a single run.
- **Exact Match + Cross-Reference Replacements:** Automatically distinguishes between genuine OEM exact matches (`Exact Match`) and compatible aftermarket/superseded alternatives (`Replacement / Cross-Ref`).
- **Live Warehouse Inventory & Lead Times:** Captures exact available stock counts and processing/dispatch days for accurate sourcing decisions.
- **Country of Origin Verification:** Extracts `Made in` manufacturing origin data (e.g., Japan, Germany, UAE, Korea, USA) critical for customs, tariffs, and compliance.
- **Built-in Anti-Bot Bypass:** Configured out-of-the-box with browser TLS fingerprint impersonation and residential proxy routing—no login or cookies required.

---

## Supported OEM & Aftermarket Brands

Covers genuine OEM catalogs and global aftermarket suppliers stocked on PartSouq, including:
- **Japanese & Korean OEM:** Toyota, Lexus, Nissan, Infiniti, Honda, Mitsubishi, Subaru, Mazda, Suzuki, Isuzu, Hyundai, Kia, Genesis
- **European & US OEM:** Mercedes-Benz, BMW, VAG (VW/Audi), Land Rover, Ford, GM, Chrysler/Jeep
- **Aftermarket Brands:** Denso, Aisin, NGK, Bosch, Febest, KYB, Mann-Filter, Mahle, Gates, and more.

---

## Input Parameters

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `partNumbers` | Array of Strings | `["90915-YZZD1", "04152-YZZA1"]` | List of OEM or aftermarket part numbers to search. Hyphens and spaces are handled automatically. |
| `includeCrossRef` | Boolean | `true` | Set to `true` to collect both exact OEM matches and compatible replacement parts, or `false` for exact part number matches only. |
| `proxyConfiguration` | Object | Residential Proxy | Pre-configured to use Apify Residential Proxies for reliable access. |

### Example Input (JSON)

```json
{
  "partNumbers": [
    "90915-YZZD1",
    "04152-YZZA1"
  ],
  "includeCrossRef": true
}
