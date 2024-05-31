---
title: Terminology Use
toc: false
sql:
  metrics: data/output-tables.db
---

```js
const formatNumber = d3.format(",");
```

```sql id=terminology_tables
SELECT table_name 
FROM information_schema.tables
WHERE table_name LIKE '%count_c_system_use_%'
ORDER BY table_name
```

```js 
const all_terminologies = [...terminology_tables].map( t => `
  SELECT 
    '${t.table_name.split("_").slice(-2)[0]}' AS resource,
    '${t.table_name.split("_").slice(-2)[1]}' AS element,
    *
  FROM metrics.${t.table_name}
`).join("\nUNION BY NAME\n")

const all_terminology_counts = await sql([`
  WITH count_by_element_system AS (
    SELECT
      resource || CASE 
        WHEN category IS NOT NULL THEN ' (' || category || ')'
        ELSE ''
      END AS resource,
      element,
      CASE 
        WHEN systems = 'cumulus__none' THEN 'none' 
        ELSE lower(systems)
      END AS systems,
      sum(cnt) AS cnt
    FROM (${all_terminologies})
    GROUP BY 1,2,3
    ORDER BY 1,2,3
  ),
  count_by_element AS (
    SELECT 
      resource,
      element, 
      sum(cnt) AS total_cnt
    FROM count_by_element_system
    GROUP BY 1,2
  )
  SELECT 
    count_by_element_system.*,
    count_by_element_system.resource || ' - ' || 
      count_by_element_system.element AS resource_element,
    round((cnt/total_cnt)*100) AS pct
  FROM count_by_element_system
  LEFT JOIN count_by_element
    ON count_by_element_system.resource = count_by_element.resource 
      AND count_by_element_system.element = count_by_element.element
`])
```

```js
  //necessary so colors don't change when filtering
  const system_list = new Set([...all_terminology_counts].map( d => d.systems ).sort())
```

```js
  const filtered_terminology = view(Inputs.search( all_terminology_counts, {placeholder: "filter by resource, element or system"} ))
```

```js
Plot.plot({
  marginLeft: 300,
  y: {
    label: null,
    tickFormat(d) {
      const [a, b] = d.split(" - ");
      return `${a}: ${b}`;
    }
  },
  x: {label: "%"},
  color: {
    legend: true,
    scheme: "accent",
    domain: system_list
  },
  marks: [
    Plot.barX(filtered_terminology, 
      Plot.stackX({
        x: "pct",
        y: "resource_element",
        fill: "systems",
        tip: true,
        title: d => `${d.systems}: ${formatNumber(d.cnt)} ${d.pct != null ? "("+Math.round(d.pct)+"%)": "na"}`
      })
    )
  ]
})
```