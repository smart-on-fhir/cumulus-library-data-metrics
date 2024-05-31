---
title: Metadata
sql:
  metrics: data/output-tables.db
---

```sql id=tbl_list
SELECT table_name 
FROM metrics.information_schema.tables
ORDER BY 1
```

```js
  const results = view(Inputs.search( tbl_list, {placeholder: "filter tables"} ))
```

${html`<ul>${[...results].map( t => html`<li>${t.table_name}</li>`)}</ul>`}