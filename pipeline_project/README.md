Challenege

Stage 1 – Load

Read the CSV.

Nothing else.

Stage 2 – Inspect

Produce a report.

Things I expect an engineer to check include:

Number of rows
Number of columns
Missing values
Duplicate rows
Data types
Unique departments
Unique cities
Numeric columns
Invalid values

But don't stop there if you think of more.

Stage 3 – Quality Report

Instead of just printing random things...

Produce something like

========== DATA QUALITY REPORT ==========

Rows: 20
Columns: 7

Missing Values
--------------
Age ............. 2
Department ...... 1
Salary .......... 1
Start Date ...... 1

Duplicate Rows
--------------
1 duplicate row found

Potential Issues
----------------
Negative salary detected
Invalid age detected (>100)
Inconsistent city names
Non-numeric salary detected

=========================================

It doesn't have to match this exactly.

Make it readable.

Stage 4 – Cleaning Policy

I don't want you to clean immediately.

Write comments first.

Example:

# Missing age:
# Fill using department average age.

# City:
# Standardize using title case.

# Salary:
# Convert invalid text to NaN.

# Negative salary:
# Flag for manual review.

This is exactly what we'd do in industry.

Stage 5 – Clean

Apply your policy.

Examples (not exhaustive):

Standardize city names
Remove duplicates
Convert salary to numeric
Handle not_available
Trim whitespace
Fix capitalization
Handle missing values
Handle impossible values
Stage 6 – Produce Outputs

Save:

clean_employee_data.csv

Then print:

Average salary by department
Employee count by department
Average age by city
Highest paying department
Any other interesting summaries you think are useful
⭐ Bonus Challenges (Optional)

If you finish early:

1.

Sort employees by salary.

2.

Find the newest employee.

3.

Find employees hired before 2021.

4.

Create a new column:

salary_band

Example:

<40000       Low
40000-60000 Medium
>60000       High
5.

Export a second CSV containing only:

Engineering employees



# Your cleaning policy
# Assumptions you made
# Interesting findings
# Limitations
# Future improvements
