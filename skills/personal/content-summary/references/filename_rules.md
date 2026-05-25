# Filename & Directory Rules

## Directory Convention

```
reports/{SourceType}_YYYY_MM_DD/
```

- `{SourceType}`: `Newsletter`, `Threads`, `YouTube`, or `Website`
- Use today's local date
- Create if it doesn't exist

## Filename Sanitisation

Replace these characters with `_`: `/` `?` `=` `&` `(space)`

Strip leading/trailing underscores after replacement.

## Website Naming

For `Website` reports, prefix with the domain (hostname without `www.`) followed by a slugified title:

```
[domain]_[slugified_title].md
```

## Examples

| Input | Output |
|---|---|
| `@cooljerrett` + topic "AI productivity" | `cooljerrett_AI_productivity.md` |
| `[寄件者]_[電子報標題]` with special chars | `Sender_Name_Newsletter_Title.md` |
| `https://martinfowler.com/articles/event-driven.html` | `martinfowler.com_articles_event-driven.md` |
