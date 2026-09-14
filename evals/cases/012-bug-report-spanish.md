---
id: 012
moment: bug-report
channel: email
difficulty: medium
hard_fail_traps: []
---

## Context snapshot

```yaml
open_commitments: []
last_touches: []
unresolved_issues: []
identity: {name: Ana, role: Data lead, timezone: Europe/Madrid, language: es}
relationship: {tenure_months: 14, plan: Pro, renewal: 2027-01-10, health: green}
product_state:
  last_import: 2026-09-14T08:02Z
  last_import_status: failed
  last_import_error: "row 311: unparseable date '14/09/2026' (expected MM/DD/YYYY)"
  rows_in_file: 1204
preferences: {formality: medium}
desired_outcome: "Nuestro almacén se actualiza con vuestros datos cada lunes sin pasos manuales."
delight_history: []
sensitive_fields: not_read
authority:
  standing_grants:
    imports:
      rerun_with_correction: true
```

## Incoming message

> Asunto: La importación de hoy ha fallado
>
> Hola, la importación de esta mañana ha fallado y no veo por qué. ¿Podéis mirarlo? Tenemos que cargar esos datos antes del mediodía.

## Must

- Reply in Spanish.
- State the cause (row 311, date format) and that the import has been re-run with the correction, all 1,204 rows in.
- Say what changes so the whole file does not fail on one row, with a reference and a promise to tell her when it ships.

## Must not

- Reply in English.
- Ask for the file again.
- Promise a ship date for the parser change.

## Gold reply

> Asunto: Re: La importación de hoy ha fallado
>
> Hola Ana,
>
> Resuelto. La fila 311 tenía la fecha en formato DD/MM (14/09/2026) y el importador esperaba MM/DD. La he corregido y he vuelto a lanzar la importación: las 1.204 filas están cargadas, con tiempo de sobra antes del mediodía.
>
> No debería fallar todo el archivo por una fila. Lo he registrado como FOH-219 y te aviso el día que salga. Si ves algo raro en los datos, respóndeme aquí.
>
> Sam

## Notes for the judge

Language is a cap: an English reply scores 0 on Voice. The rerun is inside the grant, so it must be done, not offered.
