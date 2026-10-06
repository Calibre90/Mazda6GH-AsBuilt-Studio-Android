# Run84 License Admin

This branch is reserved for the owner-only Android license administrator.

Security rule:
- Do not commit the Run84 production private key.
- Do not commit a signing implementation containing private key material.
- The customer Run84 application remains on the run84-licensed branch.
- Device Code -> Lifetime Key signing is performed only with the owner's private production key.

Planned Android UI:
1. Device Code input.
2. Generate Lifetime Key action.
3. Read-only Lifetime Key output.
4. Copy Lifetime Key action.

The production private key must remain outside GitHub and outside the customer APK.
