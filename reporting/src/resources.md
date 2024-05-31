---
title: Resources
sql:
  metrics: data/output-tables.db
---

```js
const formatNumber = d3.format(",");
```

```sql id=resource_count_tables 
SELECT table_name 
FROM information_schema.tables
WHERE table_name LIKE '%c_resource_count_%_year' 
    OR table_name LIKE '%c_resource_count_%_all'
ORDER BY table_name
```

```js 
const all_resources = [...resource_count_tables].map( t => `
  SELECT '${t.table_name.split("_").slice(-2)[0]}' AS resource, *
  FROM metrics.${t.table_name}
`).join("\nUNION BY NAME\n")

const [{resource_total_count}] = await sql([`
  SELECT sum(cnt) AS resource_total_count
  FROM (${all_resources})
`])
```

# ${formatNumber(resource_total_count)} Resources
<br/>


```js
const resource_counts = await sql([
  `SELECT 
      CASE
          WHEN category = 'cumulus__none' OR category IS NULL
            THEN resource
          ELSE resource || ' (' || category || ')'
      END AS resource,
      sum(cnt) AS cnt
  FROM (
    SELECT * FROM (${all_resources}) 
    ORDER BY resource, category 
  )
  GROUP BY 1
  ORDER BY 1
  `
])
```

## Count by Category

```js
Plot.plot({
  x: {
    grid: true, 
    label: "count",
    type: "sqrt",
    tickFormat: "s"
  },
  y: {label: null},
  marginLeft: 200,
  marks: [
    Plot.barX(resource_counts, {
        x: "cnt",
        y: "resource",
        tip: true,
        fill: "#6cc5b0"
    }),
    Plot.ruleY([0])
  ]
})
```

```js
const resource_counts_by_year = await sql([
    `SELECT 
        CASE
            WHEN category = 'cumulus__none' OR category IS NULL
            THEN resource
            ELSE resource || ' (' || category || ')'
        END AS resource,
        year::INT AS year,
        sum(cnt) AS cnt
    FROM (
        SELECT * FROM (${all_resources}) 
        ORDER BY resource, category 
    )
    GROUP BY 1,2
    ORDER BY 1,2
    `
])
```

## Resources Generated Per Year

```js
Plot.plot({
  y: {
    grid: true, 
    label: "count",
    type: "sqrt",
    insetTop: 10
  },
  x: {
    tickFormat: d => d.toString()
  },
  axis: null,
  marginLeft: 20,
  marginRight: 20,
  marks: [
    Plot.barY(resource_counts_by_year, {
        x: "year",
        y: "cnt",
        fy: "resource",
        tip: true,
        title: d => `${d.year} resources: ${formatNumber(d.cnt)}`,
        fill: "#6cc5b0"
    }),
    Plot.text( resource_counts_by_year, 
      Plot.selectFirst({
        text: "resource", 
        fy: "resource", 
        frameAnchor: "top-left", 
        dx: 6, 
        dy: 6
      })
    ),
    Plot.frame()
  ]
})
```

## Resources per Patient (Average)

```sql id=resources_per_pt
SELECT 
  id || CASE 
    WHEN category = '* No recognized category' THEN ''
    WHEN category = '* All' THEN ''
    ELSE ' (' || category || ')'
  END AS resourceType,
  average::FLOAT AS avg, 
  max
FROM metrics.data_metrics__c_resources_per_pt_summary
WHERE 
  (id = 'Observation' AND category != '* All' )
  OR (id = 'Condition' AND category != '* All')
  OR (
    id  != 'Observation' 
    AND id != 'Condition' 
    AND id != '* All' 
    AND category = '* All'
  )
ORDER BY resourceType
```

```js
Plot.plot({
  x: {
    grid: true, 
    label: "avg count",
    type: "sqrt",
    tickFormat: "s"
  },
  y: {
    grid: true,
    label: null
  },
  marginLeft: 200,
  marginRight: 100,
  marks: [
    Plot.dot(resources_per_pt, {
      y: "resourceType",
      x: "avg",
      stroke:"#6cc5b0", 
      fill: "#6cc5b0", 
      r: 5
    })
  ]
})
```

## Resources per Patient (Max)
```js
Plot.plot({
  x: {
    grid: true, 
    label: "max count",
    type: "sqrt",
    tickFormat: "s"
  },
  y: {
    grid: true,
    label: null
  },
  marginLeft: 200,
  marginRight: 100,
  marks: [
    Plot.dot(resources_per_pt, {
      y: "resourceType",
      x: "max",
      stroke:"#6cc5b0", 
      fill: "#6cc5b0", 
      r: 5
    })
  ]
})
```