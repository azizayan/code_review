# Code Review 

A tool that reviews ML-related code (Python first) for: logical errors, ML-specific pitfalls (data leakage, bad evaluation, poor preprocessing, reproducibility issues), software engineering quality (structure, naming, modularity), experiment hygiene (random seeds, config separation, logging, metrics)

**Currently:** Small Python CLI that parses source files via `ast` and surfaces basic quality issues.

**Endgoal:** AI-powered code review with a strong focus on machine learning–specific code quality and AI system design.

