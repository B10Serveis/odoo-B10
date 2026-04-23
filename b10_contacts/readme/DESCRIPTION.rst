Personalitzacions de contactes:

- Afegeix un camp `original_name` en els estats (`res.country.state`) per emmagatzemar el nom original local.
- Carrega per defecte els noms en català/dialecte per a tots els estats d’Espanya via `data/res.country.state.csv`.
- Sense impacte en la vista de partner; és un camp addicional pensat per informes i migracions.
- Override de create() per restringir que només usuaris amb el grup Settings / Technical Features (base.group_system) puguin crear nous estats/provincias.
