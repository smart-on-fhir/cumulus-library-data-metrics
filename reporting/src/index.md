---
title: Patients
sql:
  metrics: data/output-tables.db
---

```js
const formatNumber = d3.format(",");
```

```sql id=[{patient_count}]
SELECT cnt AS patient_count
FROM metrics.data_metrics__count_c_resource_count_patient_all
```

#  ${formatNumber(patient_count)} Patients
<br/>

## Birth Decade

```sql id=birth_decade
SELECT
  birth_year::INT AS birth_year,
  CASE WHEN deceased THEN 'deceased' ELSE 'alive' END AS pt_state,
  sum(cnt) AS cnt
FROM 
  metrics.data_metrics__count_c_pt_count
GROUP BY 1,2
```

```js
Plot.plot({
  x: {
    tickFormat: d => d.toString(),
    label: "birth year",
  },
  y: {
    label: "count", 
    grid: true,
  },
  color: {
    legend: true,
    domain: ["alive", "deceased"], range: ["#f28e2c", "#FFD580"] 
  },
  marks: [
    Plot.rectY(
      birth_decade,
      Plot.binX({
        y: "sum",
        title: data => [
          d3.max(data, d=>d.pt_state), "\n",
          d3.min(data, d=>d.birth_year), " - ", 
          d3.max(data, d=>d.birth_year), ": ",
          d3.sum(data, d=>d.cnt)
        ].join("")
      },{
        x: "birth_year",
        y: "cnt",
        fill: "pt_state",
        tip: true,
        interval: 10
      })
    )
  ]
})
```

## Administrative Gender

```sql id=gender
SELECT 
  administrative_gender, 
  round(sum(cnt) / (
    SELECT 
      sum(cnt) 
    FROM 
      metrics.data_metrics__count_c_pt_count
  ), 2) AS pct_cnt,
  sum(cnt) AS cnt
FROM metrics.data_metrics__count_c_pt_count
GROUP BY 1
```

```js
Plot.plot({
  x: {label: "%", percent:true},
  marks: [
    Plot.ruleX([0, 1]),
    Plot.barX(gender, 
      Plot.stackX({
        order: "administrative_gender", 
        x: "pct_cnt", 
        fill: "#FFD580",
        insetLeft: 1,
        insetRight: 1,
        channels: {"count": "cnt"},
        tip: true
      })
    ),
    Plot.textX(gender, 
      Plot.stackX({
        order: "administrative_gender", 
        x: "pct_cnt", 
        text: "administrative_gender", 
        fontWeight: "bold",
        insetLeft: 1,
        insetRight: 1
      })
    )
  ]
})
```

## Deceased Status

```sql id=deceased
SELECT
  CASE 
    WHEN deceased THEN 'deceased' 
    ELSE 'alive' 
  END AS pt_state,
  round(sum(cnt) / (
    SELECT sum(cnt) 
    FROM metrics.data_metrics__count_c_pt_count
  ), 2) AS pct_cnt,
  sum(cnt) AS cnt
FROM 
  metrics.data_metrics__count_c_pt_count
GROUP BY 1
```

```js
Plot.plot({
  x: {label: "%", percent:true},
  marks: [
    Plot.ruleX([0, 1]),
    Plot.barX(deceased, 
      Plot.stackX({
        order: "deceased", 
        x: "pct_cnt", 
        fill: "#FFD580",
        insetLeft: 1,
        insetRight: 1,
        channels: {"count": "cnt"},
        tip: true
      })
    ),
    Plot.textX(deceased, 
      Plot.stackX({
        order: "pt_state", 
        x: "pct_cnt", 
        text: "pt_state", 
        fontWeight: "bold",
        insetLeft: 1,
        insetRight: 1
      })
    )
  ]
})
```

## Race and Ethnicity
```sql id=race_ethnicity
SELECT 
  ethnicity, 
  race, 
  sum(cnt) AS cnt
FROM 
  metrics.data_metrics__count_c_pt_count
GROUP BY 1,2
```

```js
Plot.plot({
  x: {axis: null},
  y: {
    tickFormat: "s", 
    grid: true, 
    label: "count"
  },
  color: {legend: true},
  marks: [
    Plot.barY(race_ethnicity, {
      x: "race",
      y: "cnt",
      fill: "race",
      fx: "ethnicity",
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

## Age at Death

```sql id=age_at_death
SELECT age::INT AS age, sum(cnt) AS cnt
FROM metrics.data_metrics__count_c_pt_deceased_count
GROUP BY 1
```

```js
Plot.plot({
  x: {
    label: "count", 
    grid: true,
    interval: 1
  },
  marks: [
    Plot.barX(age_at_death, {
      y: "age",
      x: "cnt",
      fill: "#f28e2c"
    })
  ]
})
```