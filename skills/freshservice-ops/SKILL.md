---
name: freshservice-ops
description: >
  Freshservice ITSM operations — create, search, and update tickets; manage assets and inventory;
  browse and request service catalog items; manage onboarding and offboarding requests;
  search solution articles. Use when the user asks about IT tickets, assets, service requests,
  onboarding, offboarding, or Freshservice.
license: MIT
compatibility: Requires Freshservice MCP server (fs-remote or vamsee-fs-mcp-remote)
metadata:
  author: lakamsani
  version: "1.0"
  category: itsm
allowed-tools: Bash(curl:*) Read Write
---

# Freshservice Operations

Interact with Freshservice ITSM via MCP tools for ticket management, asset tracking, service catalog, and HR workflows.

## When to Use

Activate when the user mentions:
- IT tickets, incidents, service requests, problems, changes
- Asset management, inventory, hardware, software tracking
- Service catalog items, request fulfillment
- Employee onboarding or offboarding requests
- Solution articles, knowledge base
- Freshservice, ITSM, IT service management

## Available Operations

### Tickets
- `fetchTickets` — List tickets with filters (status, priority, agent, dates)
- `fetchTicket` — Get full ticket details by ID
- `createTicket` — Create new incident/service request
- `updateTicket` — Update ticket fields (status, priority, assignment, custom fields)
- `createTicketNote` — Add a note or reply to a ticket

### Assets
- `fetchAssets` — List assets with filters
- `fetchAsset` — Get asset details by ID
- `createAsset` — Register a new asset
- `updateAsset` — Update asset fields

### Service Catalog
- `fetchServiceItems` — Browse catalog items
- `fetchServiceItem` — Get item details and form fields
- `fetchCatalogItemFields` — Get required fields for requesting an item
- `placeRequestServiceCatalogItem` — Submit a service request

### People
- `fetchAgents` — List IT agents
- `fetchAgent` — Get agent details
- `fetchRequesters` — List requesters/employees
- `fetchRequester` — Get requester details

### Onboarding / Offboarding
- `fetchOnboardingRequests` — List onboarding requests
- `fetchOnboardingRequestForm` — Get onboarding form fields
- `createOnboardingRequest` — Create onboarding request
- `fetchOffboardingRequests` — List offboarding requests
- `createOffboardingRequest` — Create offboarding request

### Knowledge Base
- `fetchSolutionArticles` — List solution articles
- `fetchSolutionArticle` — Get article by ID
- `fetchSolutionArticleSearch` — Search articles by keyword
- `createSolutionArticle` — Publish new article
- `updateSolutionArticle` — Update existing article

## Tips
- Always confirm destructive operations (ticket closure, asset deletion) with the user
- When creating tickets, ask for subject, description, and priority at minimum
- Use `fetchCatalogItemFields` before `placeRequestServiceCatalogItem` to know required fields
