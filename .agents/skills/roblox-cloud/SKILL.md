---
name: roblox-open-cloud
description: Provides expert guidance and API references for Roblox Open Cloud development. Use this whenever the user asks to interact with Roblox APIs, DataStores, MessagingService, or Experience management.
---

# Roblox Open Cloud Skill

## Goal
To ensure all Roblox Open Cloud integrations follow the latest official API standards and security practices.

## Instructions
1. **Always Reference Docs**: Before providing any code or architecture advice, verify the endpoint details at the official reference: https://create.roblox.com/docs/cloud/reference/domains/apis
2. **Authentication**: Prioritize API Key or OAuth 2.0 implementation over legacy cookie-based methods.
3. **Error Handling**: Always include logic to handle Roblox-specific error codes (e.g., 429 Too Many Requests, 403 Forbidden).
4. **Data Management**: When using DataStore or MemoryStore APIs, ensure you are following the latest JSON schema requirements.

## Resources
- **Primary API Index**: https://create.roblox.com/docs/cloud/reference/domains/apis
- **Common Features**: Avatars, Game Passes, Users, Groups, and Assets.
- **Endpoints references**: Refer to the following folders for the local api references:
resources/asset-permissions-api/v1.json - for asset permissions api
resources/assets/v1.json - for assets api
resources/datastores-api/v1.json - for datastores api
resources/developer-products-api/v1.json - for developer products api
resources/game-passes-http-service/v1.json - for game passes http service api
resources/messaging-service/v1.json - for messaging service api
resources/open-eval-api/v1.json - for open eval api
resources/secrets-store-service/v1.json - for secrets store api
resources/toolbox-service/v1.json - for toolbox service api
resources/universes-api/v1.json - for universes api
resources/cloud.docs.json - open cloud api docs
resources/openapi.json - open cloud api

## Constraints
- Do not use deprecated "Legacy" endpoints unless explicitly requested.
- Always include the correct `x-api-key` header in example requests.

## Undocumented Findings (Use with Caution)
- **Asset Delivery API**: When using `https://apis.roblox.com/asset-delivery-api/v1/assetId/{id}`, you can request specific formats by setting the `Roblox-AssetFormat` header:
  - `avatar_meshpart_head`: Returns a MeshPart-compatible head (instead of SpecialMesh).
  - `avatar_meshpart_accessory`: Returns a MeshPart-compatible accessory (instead of SpecialMesh).
  - Note: This is part of Web API v2 behavior and is NOT yet part of the official Open Cloud spec. Use only if necessary for importers/tools.