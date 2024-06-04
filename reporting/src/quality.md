---
title: Quality
toc: false
sql:
  metrics: data/output-tables.db
---

```js
const qualityMetrics = [
  {name: "q_ref_target_valid", title: "Reference Targets in Dataset"},
  {name: "q_ref_target_pop", title: "References Populated"},
  {name: "q_date_recent", title: "Dates Are Plausible"},
  {name: "q_valid_us_core_v4", title: "Mandatory US Core Fields Are Populated"},
  {name: "q_system_use", title: "Expected Terminology Systems Are Used"}
]

const buildMetricHeading = metricId => {
  const metric = qualityMetrics.find( m => m.name == metricId);
  const slug = metric.title.toLowerCase().replace(" ", "-");

  return html`<h2 id="${slug}" tabindex="-1">
    <a class="observablehq-header-anchor" href="#${slug}">${metric.title}</a>
  </h2>`
}

const formatNumber = d3.format(",");
```

## Overview

```js
const invalidMetricSql = [
  "SELECT metric FROM (",
  qualityMetrics.map( m => [
    `SELECT '${m.name}' AS metric,`, 
    "  sum(numerator) AS numerator,", 
    "  sum(denominator) AS denominator",
    `FROM metrics.data_metrics__${m.name}_summary`
  ].join("\n")).join("\nUNION ALL\n"),
  ")",
 "WHERE numerator > 0 AND denominator > 0"
].join("\n")

const [...invalid_metrics] = await sql([invalidMetricSql]);
```

```js
html`<div style="padding-left: 20px;">
  ${qualityMetrics.map( m => html `<div>
    ${invalid_metrics.find(im => im.metric == m.name) ? "❌" : "✅"}&nbsp;
    <a href="#${m.title.toLowerCase().replace(" ", "-")}">${m.title}</a>
  </div>`)}
</div>`
```

${buildMetricHeading("q_ref_target_valid")}

```sql id=ref_target_valid
SELECT 
  id.split('_')[1] AS resource,
  id.split('_')[2] AS target,
  round((1-(numerator/denominator))*100, 0)::INT AS valid_pct
FROM  
  metrics.data_metrics__q_ref_target_valid_summary
```

```js
Plot.plot({
  padding: 0,
  grid: false,
  x: {
    axis: "top", 
    label: null
  },
  y: {label: null},
  color: {
    type: "linear",
    scheme: "spectral",
    domain: [0, 100]
  },
  marginLeft: 200,
  marks: [
    Plot.cell(ref_target_valid, {
      x: "target", 
      y: "resource", 
      fill: "valid_pct", 
      tip: true,
      inset: 0.5
    }),
    Plot.text(ref_target_valid, {
      x: "target", 
      y: "resource",
      text: (d) => d.valid_pct ? d.valid_pct+"%" : null,
      fill: (d) => d.valid_pct > 70 ? "white" : "black",
      fontWeight: "bold",
      title: "title"
    })
  ]
})
```

${buildMetricHeading("q_ref_target_pop")}

```sql id=ref_target_pop
SELECT 
  id.split('_')[1] AS resource,
  id.split('_')[2] AS target,
  round((1-(numerator/denominator))*100, 0)::INT AS valid_pct
FROM  
  metrics.data_metrics__q_ref_target_pop_summary
```

```js
Plot.plot({
  padding: 0,
  grid: false,
  x: {
    axis: "top", 
    label: null
  },
  y: {label: null},
  color: {
    type: "linear",
    scheme: "spectral",
    domain: [0, 100]
  },
  marginLeft: 200,
  marks: [
    Plot.cell(ref_target_pop, {
      x: "target", 
      y: "resource", 
      fill: "valid_pct", 
      inset: 0.5
    }),
    Plot.text(ref_target_pop, {
      x: "target", 
      y: "resource",
      text: (d) => d.valid_pct ? d.valid_pct+"%" : null, 
      fill: (d) => d.valid_pct > 70 ? "white" : "black",
      fontWeight: "bold",
      title: "title"
    })
  ]
})
```

${buildMetricHeading("q_date_recent")}

```sql id=date_recent
SELECT
  'invalid' AS validity,
  id, 
  numerator AS cnt,
  numerator/denominator*100 AS pct, 
FROM 
  metrics.data_metrics__q_date_recent_summary
UNION ALL
SELECT 
  'valid' AS validity, 
  id, 
  (denominator-numerator) AS cnt,
  ((denominator-numerator)/denominator)*100 AS pct
FROM 
  metrics.data_metrics__q_date_recent_summary
```

```js
Plot.plot({
  marginLeft: 200,
  y: {label: null},
  x: {label: "%"},
  color: {
    legend: true, 
    domain: ["invalid", "valid"],
    range: ["#f28e2c", "#FFD580"] 
},
  marks: [
    Plot.barX(date_recent, 
      Plot.stackX({
        order: "validity", 
        x: "pct",
        y: "id",
        fill: "validity",
        tip: true,
        title: d => `${d.validity} resources: ${formatNumber(d.cnt)} ${d.pct != null ? "("+Math.round(d.pct)+"%)": "na"}`
      })
    )
  ]
})
```

${buildMetricHeading("q_valid_us_core_v4")}

```sql id=valid_us_core_v4
SELECT 
  'invalid' AS validity,
  id, 
  numerator AS cnt,
  numerator/denominator*100 AS pct, 
FROM  
  metrics.data_metrics__q_valid_us_core_v4_summary
UNION ALL
SELECT 
  'valid' AS validity, 
  id,
  (denominator-numerator) AS cnt,
  ((denominator-numerator)/denominator)*100 AS pct
FROM
  metrics.data_metrics__q_valid_us_core_v4_summary
```

```js
Plot.plot({
  marginLeft: 200,
  y: {label: null},
  x: {label: "%"},
  color: {
    legend: true, 
    domain: ["invalid", "valid"], 
    range: ["#f28e2c", "#FFD580"] 
  },
  marks: [
    Plot.barX(valid_us_core_v4, 
      Plot.stackX({
        order: "validity", 
        x: "pct",
        y: "id",
        fill: "validity",
        tip: true,
        title: d => `${d.validity} resources: ${formatNumber(d.cnt)} ${d.pct != null ? "("+Math.round(d.pct)+"%)": "na"}`
      })
    )
  ]
})
```

${buildMetricHeading("q_system_use")}

```sql id=expected_terminologies
SELECT 
  'invalid' AS validity,
  id, 
  numerator AS cnt,
  numerator/denominator*100 AS pct, 
FROM
  metrics.data_metrics__q_system_use_summary
UNION ALL
SELECT 
  'valid' AS validity, 
  id,
  (denominator-numerator) AS cnt,
  ((denominator-numerator)/denominator)*100 AS pct
FROM
  metrics.data_metrics__q_system_use_summary
```

```js
Plot.plot({
  marginLeft: 200,
  y: {label: null},
  x: {label: "%"},
  color: {
    legend: true, 
    domain: ["invalid", "valid"], 
    range: ["#f28e2c", "#FFD580"] 
  },
  marks: [
    Plot.barX(expected_terminologies, 
      Plot.stackX({
        order: "validity", 
        x: "pct",
        y: "id",
        fill: "validity",
        tip: true,
        title: d => `${d.validity} resources: ${formatNumber(d.cnt)} ${d.pct != null ? "("+Math.round(d.pct)+"%)": "na"}`
      })
    )
  ]
})
```