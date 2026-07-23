# High-level architecture considerations

## Scale

- 3,000 companies
- 3–5 users per company
- Peak usage: end of month (reporting cycle)
- Auto-scaling required to handle monthly peaks

## Data integrity

- Per-declaration isolation — each time a user declares new bills, must guarantee data integrity
- Migration, recovery, backup designed around isolation boundaries

## Deployment

- Greenfield build — no existing infrastructure
- Deployment considerations for a SaaS platform serving CDI's customers
- Tech stack: no locks yet, in consideration
