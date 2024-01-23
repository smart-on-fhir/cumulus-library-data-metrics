# c_pt_count

**Basic Patient Demographics**

### Fields

- administrative_gender
- birth_year
- ethnicity
- race
- status

### Notes on `race` & `ethnicity`

These values are pulled from their US Core extensions.

The Library `core` study look at ethnicity and race in depth,
comparing the various extension
fields like `ombCategory`, `detailed`, and `text`
and using whichever it finds to grab a
human-readable text string from the whole set.
It's focused on presentation of the value.

In contrast, this metric only pulls ethnicity and race from `ombCategory`
(ignoring `detailed` and `text`, instead only looking at the code & system,
not the text display value).

This metric is more focused on "is your body of FHIR records
appropriately machine-readable?" and for that,
we're more focused on the codes and systems
than the text value.
We don't even require any text value, providing our own.
