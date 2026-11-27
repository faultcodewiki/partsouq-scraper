# PartSouq OEM Auto Parts Price, Stock & Cross-Reference Scraper

Extract real-time **OEM & aftermarket automotive parts pricing, warehouse stock quantity, processing lead time, country of origin (`Made in`), and cross-reference replacements** from PartSouq by part number.

## Extracted Data Fields
- `search_query`: Input OEM or aftermarket part number
- `match_type`: `Exact Match` or `Replacement / Cross-Ref`
- `part_number`: Matched manufacturer part number
- `brand`: Manufacturer / Make
- `title`: Full part description
- `price_usd`: Unit price in USD
- `in_stock_qty`: Available warehouse quantity
- `lead_time`: Processing / dispatch time
- `made_in`: Country of origin
- `search_url`: Direct verification link
