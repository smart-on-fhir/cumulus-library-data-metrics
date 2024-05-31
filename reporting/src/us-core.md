---
title: US Core v4 Elements
sql:
  metrics: data/output-tables.db
---

```sql id=must_support_tables 
SELECT table_name 
FROM information_schema.tables
WHERE table_name LIKE '%c_us_core_v4_count_%' 
ORDER BY table_name
```

## Must Support Elements

```js 
const formatNumber = d3.format(",");

const must_support_resources = [...must_support_tables].map( t => `
  SELECT 
    '${t.table_name.split("_us_core_v4_count_").slice(-1)[0]}' AS resource,
    *
  FROM metrics.${t.table_name}
`).join("\nUNION BY NAME\n")

const must_support_elements = await sql([`
  WITH unpivoted AS (
    UNPIVOT(
      SELECT *
      FROM (${must_support_resources})
    )
    ON COLUMNS('valid_*')
    INTO NAME element VALUE valid
  ),
  totaled AS (
    SELECT 
      resource, 
      element, 
      sum(cnt) AS total_cnt
    FROM unpivoted
    GROUP BY 1,2
  )
  SELECT
    unpivoted.resource,
    replace(unpivoted.element, 'valid_', '') AS element,
    unpivoted.resource || ' - ' || replace(unpivoted.element, 'valid_', '') 
      AS resource_element,
    CASE 
      WHEN valid = true THEN 'present and valid' 
      ELSE 'missing or invalid' 
    END AS validity,
    SUM(cnt) AS cnt,
    round(SUM(cnt) / MAX(total_cnt)*100) AS pct
  FROM unpivoted
  LEFT JOIN totaled 
    ON totaled.element = unpivoted.element
      AND totaled.resource = unpivoted.resource
  WHERE unpivoted.element != 'valid_mandatory'
  GROUP BY 1,2,3,4
  ORDER BY 1,2,3,4
`]);

const filtered_elements = view(Inputs.search( must_support_elements, {placeholder: "filter by resource or element"} ))
```

```js
Plot.plot({
  marginLeft: 300,
  y: {label: null},
  x: {label: "%"},
  color: {
    legend: true, 
    domain: ["present and valid", "missing or invalid"], 
    range: [ "#FFD580", "#f28e2c"] 
  },
  marks: [
    Plot.barX(filtered_elements, 
      Plot.stackX({
        order: "validity", 
        reverse: true,
        x: "pct",
        y: "resource_element",
        fill: "validity",
        tip: true,
        title: d => `${d.validity}: ${formatNumber(d.cnt)} ${d.pct != null ? "("+Math.round(d.pct)+"%)": "na"}`
      })
    )
  ]
})
```