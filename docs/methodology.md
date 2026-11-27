# Screening methodology

Version 1 is a discovery filter, not an investment recommendation. It uses eight selected US stocks and the largest 250 cryptocurrencies by market capitalization at collection time. It does not represent the entire market.

## Rules
- Price at most USD 5.
- Daily dollar volume at least USD 100,000.
- Positive, finite market capitalization, price and volume.
- Missing data fails screening rather than being replaced by zero.

Stock volume is approximated by last quoted price times session volume; cryptocurrency volume is provider-reported 24-hour volume. They are not directly comparable. Collection time is not necessarily exchange quote time. Stale quotes, manipulation, delistings, dilution and fees are not yet modelled.

## Next steps
Add financial statements, debt and cash flow metrics for stocks; token supply, unlocks and concentration for crypto. Separate asset-class rankings. Use point-in-time historical universes, delisted securities, realistic costs and out-of-sample evaluation before claiming predictive value.
