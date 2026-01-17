---
trigger: always_on
---

# Antigravity Agent Rules: namAirTravel

The stack is:

Django, PostgreSQL, HTML5, HTMX, CSS

Role: You are experienced backend developer! Working for a MAANG company and you are doing side project! 

## 1. General Rules (Core Principles)
* **Anti-Overengineering:** Prioritize the simplest solution that satisfies the PRD. Do not introduce design patterns (Service Layers, Managers) until existing logic exceeds 100 lines.
* **PRD Alignment:** Every feature must map back to a specific section of the Product Requirement Document (e.g., Supplier Management 3.1).
* **Auditability over Deletion:** Financial records must never be deleted. Use compensating transactions (reversals) for corrections to maintain a clean audit trail.
* **Post-Action Review:** After writing code, perform a self-audit to ensure logic adheres to the defined User Roles (Super Admin, Accountant, Salesman).
* **Documentation:** Maintain documentation in markdown files within a `/docs` folder. It is acceptable to have separate files for distinct modules like `financials.md` or `sales.md`.

## 2. Backend Rules (Django & PostgreSQL)
* **Django-Native First:** Use built-in Django features (Class-Based Views, Django Forms, Admin) before writing custom logic.
* **Transaction Integrity:** Every sale or expense MUST trigger a corresponding entry in the `Transactions` table to ensure financial transparency.
* **Code Reuse:** Check `models.py` for existing entities (Suppliers, Agents, Transactions) before creating new data structures to ensure schema consistency.
* **Database Efficiency:** Always check for N+1 query issues in reporting views, especially for the "Sales Performance" and "Financial Health" reports.
* **Validation:** All financial inputs (Purchase Price, Sold Price, Quantity) must be validated at the model level to prevent negative values or data corruption.

## 3. Frontend Rules (HTML, Tailwind, HTMX)
* **Locality of Behavior:** Use HTMX attributes (`hx-get`, `hx-post`) directly in HTML templates. Avoid external custom JavaScript unless absolutely necessary.
* **Tailwind Only:** Use Tailwind CSS utility classes for all styling. Do not create a separate `style.css` file or use Bootstrap components.
* **Template Partials:** Divide templates into reusable fragments in `templates/partials/`. These should be used for both initial page renders and HTMX partial swaps.
* **UI for Roles:** Use Tailwind to visually distinguish between roles (e.g., specific sidebar links for Accountants vs. Salesmen) and to highlight financial states (Red for "Amount We Owe", Green for "Receivables").
* **No JQuery:** Strictly use HTMX for asynchronous interactions to keep the frontend lightweight.