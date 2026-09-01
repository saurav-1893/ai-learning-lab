# AI Learning Lab

A project-driven journey towards becoming an AI Engineer.

Rather than learning tools in isolation, this repository documents my progression through Python engineering, data engineering, machine learning, deep learning, AI systems and eventually a full AI capstone project.

The focus of this roadmap is not only learning how to use libraries, but understanding the problems those libraries solve and developing the engineering judgement to decide when and why to use them.

---

## Roadmap

### Module 1 — Python CLI Engineering

**Status:** ✅ Complete

Built a command-line CSV analysis tool from scratch using Python.

#### Skills Developed

* Python functions and control flow
* CLI applications
* Command-line arguments
* Input validation
* File handling
* CSV processing
* Dictionaries and lists
* Error handling
* Modular program design
* Separation of concerns
* NumPy fundamentals
* Git and iterative development

#### Commands Implemented

* `--summary`
* `--stats`
* `--columns`
* `--filter`

#### Key Engineering Lessons

* Load data once and pass it where it is needed.
* Separate data processing from presentation.
* Functions should have clear responsibilities.
* Return useful data rather than printing from business logic.
* Think about architecture before adding more code.
* Libraries are most useful when you understand the complexity they are hiding.

---

### Module 2 — Data Engineering with Pandas

**Status:** ✅ Complete

Built an employee data pipeline that takes a deliberately messy CSV dataset through inspection, validation, cleaning, analysis and export.

#### Skills Developed

* Pandas DataFrames and Series
* Boolean masks
* Row and column filtering
* Missing-value analysis
* Data-type conversion
* `groupby()` and aggregation
* Data-quality reporting
* Cleaning policies
* Data validation
* Duplicate detection
* Identifier integrity checks
* Data transformation
* Pipeline architecture
* CLI command routing
* Git rebasing and conflict resolution

#### Pipeline

```text
CSV File
   ↓
Validate Input
   ↓
Load Data
   ↓
Inspect Raw Data
   ↓
Quality Report
   ↓
Clean Data
   ↓
Generate Summary
   ↓
Export Clean Dataset
```

#### Key Engineering Lessons

* Inspect before cleaning.
* Unknown does not mean zero.
* Cleaning decisions should follow an explicit policy.
* Preserve raw data and transform a copy.
* Boolean masks make validation rules readable and reusable.
* Detect problems you cannot safely infer rather than manufacturing certainty.
* A duplicate row and a duplicate identifier are different data-quality problems.
* Functions should receive their dependencies explicitly rather than relying on global state.
* A pipeline is a series of trustworthy transformations.

---

### Module 3 — Machine Learning Foundations

**Status:** 🚀 Next

The next stage moves from preparing and analysing data to learning patterns from data.

Planned topics include:

* Features and targets
* Supervised learning
* Train/test splits
* Baselines
* Regression
* Classification
* Model evaluation
* Overfitting and underfitting
* Feature engineering
* scikit-learn
* Model comparison and engineering trade-offs

---

## Long-Term Capstone — Vision Assistant

**Status:** 🧠 Design / Exploration

The long-term capstone is an AI-powered accessibility assistant intended to help visually impaired users understand their surroundings.

The planned system will progressively combine concepts learned throughout the roadmap, including:

* Camera/image input
* Computer vision
* Multimodal AI
* Voice interaction
* Text-to-speech
* APIs
* Data storage
* AI system architecture
* Deployment

The capstone will evolve alongside the roadmap rather than being built as an isolated final exercise.

---

# Engineering Principles

Throughout this journey I am collecting short principles that capture important changes in how I think about engineering.

> **What complexity is this library hiding from me?**

> **A good abstraction doesn't remove understanding. It removes repetition.**

> **Return data. Print presentation.**

> **Inspect before cleaning.**

> **Unknown is not the same as zero.**

> **A pipeline isn't a long script. It's a series of trustworthy transformations.**

> **Detect what you cannot safely infer; don't manufacture certainty.**

> **Strong engineers don't build identities around being right. They build identities around getting closer to what's true.**

> **Don't aim to challenge what exists. Aim to understand it so well that you can improve it.**

---

# Retrospective

At the end of each module I ask:

### What clicked?

What concepts changed the way I understand software or AI?

### What was surprisingly difficult?

Which problems required more thought than expected?

### What would I do differently?

How would I redesign the project knowing what I know now?

### Can I explain it?

Could I explain the important concepts and engineering decisions to another developer without relying on memorised syntax?

---

# Goal

The goal of this repository is not simply to complete courses or collect libraries.

The goal is to develop the ability to approach unfamiliar engineering problems, reason about them independently, make defensible technical decisions and build useful AI systems from end to end.
