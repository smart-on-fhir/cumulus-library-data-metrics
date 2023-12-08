CREATE TABLE quality__count_c_pt_deceased_count AS (
WITH

parsed AS (
    SELECT
        id,
        active,
        gender,
        from_iso8601_timestamp(birthDate) AS birthDate,
        deceasedBoolean,
        from_iso8601_timestamp(deceasedDateTime) AS deceasedDateTime
    FROM patient
    WHERE
        deceasedBoolean = TRUE
        OR deceasedDateTime IS NOT NULL
),

simplified AS (
    SELECT
        id,

        COALESCE(
            gender,
            'missing-or-null'
        ) AS administrative_gender,

        CASE WHEN active IS NULL
        THEN 'missing-or-null'
        ELSE (CASE WHEN active THEN 'active' ELSE 'inactive' END)
        END AS status,

        -- Calculate age at death.
        -- Note that if deceasedBoolean is used instead of deceasedDateTime,
        -- this will result in None (as we want).
        COALESCE(
            -- We want a date-difference method that takes month/day into consideration.
            -- That is, we don't want a simple (year_part - year_part) calculation.
            -- Which means DATE_DIFF in Athena, but DATE_SUB in DuckDB...  :shakes_fist:
            -- So we extract days-of-year and compare them to add an offset.
            -- Note that 'doy' is the only alias for day-of-year that is shared between SQLs.
            CAST(
                year(deceasedDateTime)
                - year(birthDate)
                - (
                    CASE WHEN
                        extract(doy FROM birthDate) > extract(doy FROM deceasedDateTime)
                    THEN 1
                    ELSE 0
                    END
                )
                AS VARCHAR
            ),
            'missing-or-null'
        ) AS age

    FROM parsed
)

SELECT
    COUNT(DISTINCT id) AS cnt,
    administrative_gender,
    status,
    age
FROM simplified
GROUP BY CUBE(
    administrative_gender,
    status,
    age
)
);