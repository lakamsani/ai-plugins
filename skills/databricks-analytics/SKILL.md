---
name: databricks-analytics
description: >
  Query and explore Databricks warehouses via Baikal MCP — list catalogs, schemas, and tables;
  inspect table metadata and column types; execute read-only SQL queries; monitor warehouse status.
  Use when the user asks about data analytics, SQL queries, Databricks, data warehouses,
  table schemas, or Baikal pipelines.
license: MIT
compatibility: Requires Baikal MCP server (baikal-mcp)
metadata:
  author: lakamsani
  version: "1.0"
  category: analytics
allowed-tools: Bash Read Write
---

# Databricks Analytics

Explore and query Databricks data warehouses through the Baikal MCP integration.

## When to Use

Activate when the user mentions:
- SQL queries, data analysis, analytics
- Databricks, data warehouse, lakehouse
- Table schemas, column metadata, catalog browsing
- Baikal, ETL pipelines, data ingestion
- Data exploration, warehouse status

## Available Operations

### Discovery
- `list_databricks_host` — List available Databricks hosts/workspaces
- `list_warehouses` — List SQL warehouses on a host
- `get_warehouse_status` — Check warehouse state (running, stopped, etc.)
- `start_sql_warehouse` — Start a stopped warehouse

### Schema Browsing
- `list_catalogs` — List all catalogs in a workspace
- `list_schemas` — List schemas within a catalog
- `list_tables` — List tables within a schema
- `get_table_metadata` — Get column names, types, and table properties

### Querying
- `read_only_execute_query` — Execute read-only SQL (SELECT, SHOW, DESCRIBE)

## Workflow

1. `list_databricks_host` to find the target workspace
2. `list_warehouses` + `get_warehouse_status` to find a running warehouse
3. `list_catalogs` > `list_schemas` > `list_tables` to navigate to the data
4. `get_table_metadata` to understand columns before querying
5. `read_only_execute_query` to run analytical SQL

## Tips
- Always check warehouse status before querying — start it if stopped
- Use `get_table_metadata` before writing queries to get correct column names
- Queries are read-only; INSERT/UPDATE/DELETE/DROP will be rejected
- For large result sets, use LIMIT in your SQL
