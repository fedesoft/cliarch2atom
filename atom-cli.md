
- borrar objectos digitales dado un slug, con -d hace dry-run

```bash
sudo php symfony digitalobject:delete --and-descendants m1-09
```

- borrar descripciones dado un slug, se puede pasar --no-confirmation

```bash
sudo php symfony tools:delete-description "m1-09"
```

- limpiar cache y regenerar index

```bash
sudo php symfony cc && sudo php symfony search:populate
```

- regenerar index

```
 --slug Slug of resource to index (ignoring exclude-types option).

 --ignore-descendants  Don't index resource's descendants (applies to --slug option only).

 --exclude-types Exclude document type(s) (command-separated) from indexing

 --show-types Show available document type(s), that can be excluded, before indexing

 --update Don't delete existing records before indexing.
```

```bash
sudo php symfony search:populate
```