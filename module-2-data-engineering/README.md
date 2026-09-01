# Employee Data Pipeline

## Overview

This project is part of Module 2 of my AI Engineering roadmap.

The objective was to build a small data engineering pipeline that takes a deliberately messy employee dataset and transforms it into structured, validated and analysis-ready data.

The project began as a way to learn Pandas, but evolved into an exercise in data-quality policy, pipeline architecture, validation and separation of responsibilities.

---

# Pipeline Architecture

```text
CSV Input
   ↓
Validate File
   ↓
Load Raw Data
   ↓
Inspect Dataset
   ↓
Generate Quality Report
   ↓
Apply Cleaning Policy
   ↓
Generate Summary Statistics
   ↓
Export Clean Dataset
```

The raw DataFrame is preserved while cleaning operations are performed on a copy.

---

# CLI Usage

The pipeline accepts a CSV filepath followed by a command.

```bash
python employee_pipeline.py employee_data.csv <command>
```

Supported commands include:

```text
quality_report
cleaned_data
summary
export_data
```

A specific quality metric can also be requested.

Example:

```bash
python employee_pipeline.py employee_data.csv quality_report missing_by_column
```

---

# Data Quality Inspection

The pipeline inspects the raw dataset for:

* Number of rows
* Number of columns
* Missing values by column
* Total missing values
* Duplicate rows
* Duplicate employee identifiers
* Data types
* Unique departments
* Unique cities
* Numeric columns

The quality report is generated before cleaning so that problems in the original dataset remain visible.

---

# Cleaning Policy

## Employee ID

Rules:

* Must be numeric.
* Intended to uniquely identify an employee.
* Duplicate IDs are treated as potential integrity problems.

A duplicated identifier is not automatically corrected because the pipeline cannot safely determine which record represents the correct employee state.

---

## Name

Rules:

* Expected to contain a valid employee name.
* Should not be empty.

No attempt is made to infer missing names automatically.

---

## Department

Rules:

* Standardize text formatting.
* Missing departments require review.

Rows with missing departments receive a review flag rather than having a department invented automatically.

---

## Age

Rules:

* Must be numeric.
* Valid range: 18–100.

Missing or invalid ages are replaced using the median calculated from valid ages.

This decision provides a usable numeric value without allowing extreme invalid values to distort the imputation calculation.

---

## City

Rules:

* Remove leading and trailing whitespace.
* Standardize using uppercase.
* Maintain consistent spelling.

The pipeline does not automatically guess corrections for genuinely misspelled cities because doing so could introduce incorrect information.

---

## Salary

Rules:

* Convert values to numeric format.
* Non-numeric values become missing values.
* Negative salaries are treated as invalid.
* Invalid salaries require review.

A separate `salary_flag` is used rather than inserting text such as `"Needs Reviewing"` into the numeric salary column.

This preserves the salary column's numeric data type for later analysis.

---

## Start Date

Rules:

* Convert values to datetime format.
* Invalid or missing dates require review.

A separate flag identifies records that need investigation.

---

# Duplicate Handling

The project distinguishes between two different problems.

### Duplicate Row

Two entire records are identical.

Exact duplicate rows can be removed using the cleaning pipeline.

### Duplicate Employee ID

Two records share the same employee identifier but may contain different attributes.

This is treated as an integrity problem rather than automatically deleting one of the records.

The correct record cannot safely be inferred without additional business context.

---

# Summary Statistics

After cleaning, the pipeline calculates:

* Average salary by department
* Employee count by department
* Average age by city
* Highest salary by department
* Highest-paying department

These summaries are calculated from the cleaned dataset rather than the raw input.

---

# Output

The cleaned dataset can be exported as:

```text
clean_employee_data.csv
```

The pipeline confirms the export filepath after successfully writing the file.

---

# Concepts Practised

## Pandas

* DataFrames
* Series
* Boolean masks
* `.loc[]`
* `.isna()`
* `.between()`
* `.groupby()`
* `.mean()`
* `.median()`
* `.max()`
* `.idxmax()`
* `.drop_duplicates()`
* `.select_dtypes()`
* `.to_numeric()`
* `.to_datetime()`
* String transformations
* CSV import/export

## Python Engineering

* Function decomposition
* CLI argument handling
* Input validation
* Separation of concerns
* Explicit data flow
* Returning data from functions
* Command routing
* Refactoring exploratory code into a pipeline

## Git

During this module the repository was also reorganized from week-based folders into module-based folders.

The process included:

* Inspecting tracked vs untracked files
* Staging deliberate changes
* Understanding Git rename detection
* Fetching remote changes
* Rebasing local commits
* Resolving merge conflicts
* Understanding local vs remote history
* Maintaining a clean working tree

---

# Challenges & Lessons

## Boolean Masks

Boolean masks became one of the most important recurring patterns in the module.

Instead of repeatedly writing complex conditions directly inside transformations, meaningful masks were created and reused.

This improved readability and made validation rules easier to reason about.

---

## Pandas Objects

A key lesson was understanding the difference between:

* DataFrame
* Series
* Index
* GroupBy objects
* normal Python objects

Rather than memorising method chains, the focus became:

> **What object am I holding right now?**

Understanding the returned object made method chaining significantly easier to reason about.

---

## Cleaning Requires Context

One of the biggest lessons from this project was that data cleaning is not simply about calling methods such as `dropna()`.

A technical operation may be easy while the correct business decision remains unclear.

For example:

* An unknown salary should not automatically become zero.
* An impossible age should not automatically be assumed to be a typo.
* Duplicate employee IDs should not automatically cause one record to be deleted.

When the correct value cannot safely be inferred, the pipeline should identify the problem rather than manufacture certainty.

---

# Engineering Takeaways

> **Inspect before cleaning.**

> **Unknown is not the same as zero.**

> **Return data. Print presentation.**

> **A pipeline isn't a long script. It's a series of trustworthy transformations.**

> **Functions should separate responsibilities, not merely reduce lines of code.**

> **Detect what you cannot safely infer; don't manufacture certainty.**

> **A duplicate is defined by what the data represents, not simply by whether two rows look alike.**

---

# Retrospective

## What clicked?

Boolean masks became much more intuitive once I understood them as reusable descriptions of which rows satisfy a condition.

Pandas also became easier once I stopped thinking primarily about methods and started thinking about transformations and the objects being returned.

## What was surprisingly difficult?

The hardest part was often not the Pandas syntax.

It was deciding what the pipeline *should* do with ambiguous or invalid data.

Refactoring exploratory code into functions with clear responsibilities also required more thought than simply making the script work.

## What would I do differently if I rebuilt this project?

I would define the pipeline architecture and cleaning policy earlier.

I would separate inspection, cleaning, presentation and export from the beginning rather than initially allowing them to grow together in one script.

I would also define validation rules for identifiers and important business fields before applying transformations.

---

# Future Improvements

Potential improvements include:

* Automated tests
* Logging
* JSON quality-report export
* More robust schema validation
* Configurable cleaning policies
* Improved CLI argument parsing
* Larger dataset testing
* Performance profiling
* Database input/output
* API integration

---

# Status

**Module 2 — Complete ✅**

This project marks the transition from learning Python syntax and individual Pandas operations toward designing small data-processing systems with explicit policies, responsibilities and data flows.
