# q_date_in_lifetime

**Are dates for resources that are associated with a patient within that patient's life?**

Each patient potentially has a `Patient.birthDate` and a `Patient.deceasedDateTime`.
Every resource with a date element should occur while the patient is alive, minus some margin (30 days).

### Numerator (population)

Given: any resource `R` that has a date field `R.date`, and a patient reference `P` with a
valid birthdate `P.birthDate` or a date of death `P.deceasedDateTime`.
`R.date` must appear within the lifespan of the patient, as defined below:
- Deceased patients: the period between `P.birthDate`and `P.deceasedDateTime + 30 days`
- Living patients: the period between `P.birthDate` and the end of time.
- Deceased patients with no `P.birthDate`: the period between the beginning of time and
`P.deceasedDateTime + 30 days`

### Denominator

Any resource `R` that has a date field `R.date` and a patient reference `P` with a
valid birthdate, `P.birthDate`, and, optionally, a date of death, `P.deceasedDateTime`.

### Interesting Cases
**DOB**: 1999-12-31  
**DOD**: 2000-01-01  
**Observation A**: 1999  
**Observation B**: 2000  

Both `O.A` and `O.B` are valid. `O.A` can be interpreted as `1999-12-31T23:59:59`, which
is after the DOB and before the DOD. `O.B` can be interpreted as `2000-01-01T01:01:01` which is
after the DOB and before the DOD.