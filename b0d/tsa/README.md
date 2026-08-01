# P032 B0 — pinned RFC-3161 Timestamping Authority trust anchors

**Pinned by:** backend_devops_eng, task `T-B0m0-rfc3161-tsa-probe-2026-07-30`
**Date pinned:** 2026-07-30
**Full probe report:** `agents/backend_devops_eng/outbox/T-B0m0-rfc3161-tsa-probe-2026-07-30.md`

## Files in this directory

- `digicert_primary.pem` — PRIMARY trust anchor (self-signed root).
- `sectigo_fallback.pem` — FALLBACK trust anchor (self-signed root).
- `README.md` — this file.

## What the checker (T-B0m2) uses this for

Offline verification of RFC-3161 tokens. The token itself carries the signer cert and intermediate CA (we request `-cert` in the TSQ). The checker uses the pinned .pem in this directory as the `-CAfile` trust anchor and passes the intermediates extracted from the token as `-untrusted`. No network call needed at verification time.

Verified working command shape (both TSAs, on 2026-07-30):

```
openssl ts -verify -data <original_bytes> -in <tsr> \
    -CAfile ops/projects/P032/B0/tsa/<name>.pem \
    -untrusted <intermediates-extracted-from-token>
# → "Verification: OK"
```

## PRIMARY — `digicert_primary.pem`

- **TSA endpoint (what B0m1 protocol names):** `http://timestamp.digicert.com`
- **Pinned identity:** DigiCert Trusted Root G4 (self-signed)
- **Subject:** `C=US, O=DigiCert Inc, OU=www.digicert.com, CN=DigiCert Trusted Root G4`
- **Issuer:** same (self-signed)
- **Serial:** `059B1B579E8E2132E23907BDA777755C`
- **notAfter:** `Jan 15 12:00:00 2038 GMT`
- **SHA-256 fingerprint (cert):** `55:2F:7B:DC:F1:A7:AF:9E:6C:E6:72:01:7F:4F:12:AB:F7:72:40:C7:8E:76:1A:C2:03:D1:D9:D2:0A:C8:99:88`
- **SHA-256 of `digicert_primary.pem` file:** `ce7d6b44f5d510391be98c8d76b18709400a30cd87659bfebe1c6f97ff5181ee`
- **Source URL:** `https://cacerts.digicert.com/DigiCertTrustedRootG4.crt` (DER, converted to PEM)
- **Cost tier:** free, no registration; DigiCert publicly documents `timestamp.digicert.com` for third-party codesigning use.

## FALLBACK — `sectigo_fallback.pem`

- **TSA endpoint (what B0m1 protocol names):** `http://timestamp.sectigo.com`
- **Pinned identity:** USERTrust RSA Certification Authority (self-signed) — the root under which Sectigo's public timestamping chain issues.
- **Subject:** `C=US, ST=New Jersey, L=Jersey City, O=The USERTRUST Network, CN=USERTrust RSA Certification Authority`
- **Issuer:** same (self-signed)
- **Serial:** `01FD6D30FCA3CA51A81BBC640E35032D`
- **notAfter:** `Jan 18 23:59:59 2038 GMT`
- **SHA-256 fingerprint (cert):** `E7:93:C9:B0:2F:D8:AA:13:E2:1C:31:22:8A:CC:B0:81:19:64:3B:74:9C:89:89:64:B1:74:6D:46:C3:D4:CB:D2`
- **SHA-256 of `sectigo_fallback.pem` file:** `8a3dbcb92ab1c6277647fe2ab8536b5c982abbfdb1f1df5728e01b906aba953a`
- **Source URL:** `http://crt.usertrust.com/USERTrustRSACertificationAuthority.crt` (DER, converted to PEM)
- **Cost tier:** free, no registration; Sectigo publicly documents `timestamp.sectigo.com` for third-party codesigning use.

## Rotation / re-pin policy

- **When to re-pin:** if either root approaches its `notAfter` (both are 2038-01), if a CA replaces the root, if the endpoint issues signer certs under a different root, or if the endpoint stops issuing free tokens.
- **How to re-pin:** re-run the T-B0m0 probe against both endpoints, extract the top self-signed root each signer chains to, replace the .pem, update this README (SHA-256, notAfter, date pinned), route the change past Director.
