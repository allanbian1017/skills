# Filename & Directory Rules

## Directory Convention

```
reports/{SourceType}_YYYY_MM_DD/
```

- `{SourceType}`: `Newsletter`, `Threads`, or `YouTube`
- Use today's local date
- Create if it doesn't exist

## Filename Sanitisation

Replace these characters with `_`: `/` `?` `=` `&` `(space)`

Strip leading/trailing underscores after replacement.

## Examples

| Input | Output |
|---|---|
| `@cooljerrett` + topic "AI productivity" | `cooljerrett_AI_productivity.md` |
| `[寄件者]_[電子報標題]` with special chars | `Sender_Name_Newsletter_Title.md` |
