# Common Review Checklist (Language-Agnostic)

This reference defines universal code quality, security, and test coverage standards applicable across all languages and frameworks. It is loaded automatically during review.

---

## 1. Security (CRITICAL)

Security defects expose systems, credentials, or user data to compromise. Any finding in this section is a merge-blocking defect.

### 1.1 Hardcoded Credentials
- **Check**: No API keys, passwords, bearer tokens, private keys, or sensitive connection strings in source files.
- **Remediation**: Inject via environment variables, secret managers, or external vault references. Ensure secret files are ignored in `.gitignore`.

```typescript
// BAD: Secret committed in code
const client = new Client({ apiKey: "sk-proj-948201948102948102" });

// GOOD: Injected securely from environment
const client = new Client({ apiKey: process.env.SERVICE_API_KEY });
```

### 1.2 SQL Injection & Unsanitized Queries
- **Check**: All SQL/NoSQL queries must use parameterized placeholders or prepared statements. Never concatenate or interpolate user input directly into queries.
- **Remediation**: Use parameterized queries, positional variables, or query builders/ORMs.

```go
// BAD: String concatenation in query
query := fmt.Sprintf("SELECT id, name FROM users WHERE role = '%s'", role)
rows, err := db.Query(query)

// GOOD: Parameterized query
rows, err := db.Query("SELECT id, name FROM users WHERE role = $1", role)
```

### 1.3 Cross-Site Scripting (XSS)
- **Check**: User-supplied input rendered in web pages, email templates, or UI views must be properly escaped or sanitized.
- **Remediation**: Use context-aware escaping libraries (e.g., DOMPurify) or native templating frameworks that auto-escape (e.g., React JSX, Go `html/template`).

```tsx
// BAD: Rendering unsanitized HTML
<div dangerouslySetInnerHTML={{ __html: userBio }} />

// GOOD: Sanitize before rendering or render text
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userBio) }} />
// OR directly as text:
<div>{userBio}</div>
```

### 1.4 Path Traversal
- **Check**: File system lookups or uploads accepting path parameters must be validated, sanitized, and restricted within an allowed base directory.
- **Remediation**: Use `filepath.Clean`, reject `..` traversal sequences, and verify that the resolved path resides within the authorized directory root.

```python
# BAD: Direct path concatenation allows ../../etc/passwd
filepath = os.path.join(UPLOAD_DIR, user_filename)
with open(filepath, "r") as f:
    return f.read()

# GOOD: Normalize and enforce directory containment
safe_filename = os.path.basename(user_filename)
filepath = os.path.abspath(os.path.join(UPLOAD_DIR, safe_filename))
if not filepath.startswith(os.path.abspath(UPLOAD_DIR)):
    raise PermissionError("Path traversal detected")
```

### 1.5 Cross-Site Request Forgery (CSRF)
- **Check**: State-changing HTTP endpoints (POST, PUT, DELETE, PATCH) served to browsers must enforce CSRF token validation or rely on `SameSite=Strict`/`Lax` cookies with explicit anti-forgery headers.
- **Remediation**: Apply CSRF middleware on state-altering session-backed routes.

### 1.6 Authentication & Authorization Bypasses
- **Check**: All protected handlers, endpoints, and RPCs must verify caller identity and authorization permissions. Verify that multi-tenant resources check tenant ownership on every read/write.
- **Remediation**: Apply authentication and authorization guards at middleware or router boundary.

```go
// BAD: IDOR / Missing ownership verification
func GetOrder(w http.ResponseWriter, r *http.Request) {
    orderID := r.URL.Query().Get("id")
    order, _ := db.FindOrder(orderID) // Any user can query any order!
    json.NewEncoder(w).Encode(order)
}

// GOOD: Enforce authenticated user scope
func GetOrder(w http.ResponseWriter, r *http.Request) {
    userID := auth.FromContext(r.Context()).UserID
    orderID := r.URL.Query().Get("id")
    order, err := db.FindUserOrder(userID, orderID)
    if err != nil {
        http.Error(w, "Not found", http.StatusNotFound)
        return
    }
    json.NewEncoder(w).Encode(order)
}
```

### 1.7 Insecure Dependencies
- **Check**: Do not introduce packages with known high/critical CVEs or unmaintained abandoned libraries.
- **Remediation**: Run automated dependency audits (`npm audit`, `govulncheck`, `pip-audit`).

### 1.8 Exposed Secrets in Logs & Telemetry
- **Check**: Avoid logging authentication tokens, passwords, credit card numbers, or PII.
- **Remediation**: Mask sensitive fields or omit payload details in loggers and telemetry traces.

---

## 2. Code Quality & Bugs (HIGH)

Issues in this category cause runtime panics, incorrect business logic, resource leaks, or maintainability degradation.

### 2.1 Logic Errors
- **Check**: Verify boolean logic, inverted conditionals, off-by-one loop boundaries, and correct state transition handling.
- **Remediation**: Add explicit branch coverage and simplify compound conditional expressions.

### 2.2 Null & Nil Handling
- **Check**: Pointers, nullable objects, and optional fields must be validated for existence before member access or dereferencing.
- **Remediation**: Add explicit nil/null guards, optional chaining (`?.`), or guard clauses with early returns.

```go
// BAD: Unchecked pointer dereference
func Process(meta *Metadata) string {
    return meta.TraceID // Panic if meta is nil!
}

// GOOD: Safe guard clause
func Process(meta *Metadata) string {
    if meta == nil {
        return ""
    }
    return meta.TraceID
}
```

### 2.3 Race Conditions & Concurrency
- **Check**: Shared mutable state accessed across goroutines, threads, or asynchronous callbacks must be synchronized using mutexes, atomic operations, or channels. Watch for Time-of-Check to Time-of-Use (TOCTOU) races.
- **Remediation**: Protect shared state with locks or encapsulate inside concurrent-safe structures.

```go
// BAD: Data race on shared counter
var counter int
for i := 0; i < 1000; i++ {
    go func() { counter++ }()
}

// GOOD: Atomic or mutex synchronization
var counter int64
for i := 0; i < 1000; i++ {
    go func() { atomic.AddInt64(&counter, 1) }()
}
```

### 2.4 Unhandled Errors & Exceptions
- **Check**: Return errors must never be swallowed with blank identifiers (`_ = err`), unhandled promise rejections, or empty `catch`/`recover` blocks without justification.
- **Remediation**: Handle, log, wrap, or propagate every error cleanly.

```go
// BAD: Swallowing error silently
data, _ := os.ReadFile("config.json")

// GOOD: Handle and propagate error
data, err := os.ReadFile("config.json")
if err != nil {
    return fmt.Errorf("read config file: %w", err)
}
```

### 2.5 Function & File Size Limits
- **Check**:
  - **Functions**: Limit function bodies to **under 50 lines**. Functions exceeding 50 lines often violate single-responsibility.
  - **Files**: Limit files to **under 800 lines**. Monolithic files should be split into focused domain modules.
- **Remediation**: Extract cohesive helper functions and modularize files by domain responsibility.

### 2.6 Deep Nesting (>4 Levels)
- **Check**: Code blocks nested deeper than 4 indentation levels are difficult to read and test.
- **Remediation**: Invert `if` statements with early returns / guard clauses, and decompose loops into helper functions.

```typescript
// BAD: Deep nesting (>4 levels)
function handleEvent(event: Event) {
  if (event) {
    if (event.type === 'ORDER') {
      if (event.payload) {
        if (event.payload.items.length > 0) {
          processOrder(event.payload);
        }
      }
    }
  }
}

// GOOD: Flat with guard clauses
function handleEvent(event: Event) {
  if (!event || event.type !== 'ORDER') return;
  if (!event.payload || event.payload.items.length === 0) return;
  processOrder(event.payload);
}
```

### 2.7 Mutation Patterns & Side Effects
- **Check**: Avoid in-place mutation of input arguments or global state unless explicitly intended for performance-critical buffers.
- **Remediation**: Prefer immutable copies, pure functions, and explicit return values.

```typescript
// BAD: In-place mutation of caller array
function addTags(article: Article, tags: string[]) {
  article.tags.push(...tags); // Side effect on input
  return article;
}

// GOOD: Pure transformation returning new object
function addTags(article: Article, tags: string[]): Article {
  return {
    ...article,
    tags: [...article.tags, ...tags],
  };
}
```

### 2.8 Debug Logging & Leftover Artifacts
- **Check**: No temporary debugging statements (`console.log`, `fmt.Println`, `print()`, `debugger;`) left in pull requests.
- **Remediation**: Remove debug calls or replace with structured logging at appropriate debug levels (`logger.Debug(...)`).

### 2.9 Dead Code
- **Check**: Remove commented-out code blocks, unused imports, unreferenced local variables, and unreachable switch/if branches.
- **Remediation**: Clean up dead code before submitting review.

---

## 3. Test Coverage & Verification (MEDIUM)

Inadequate test coverage leads to regressions and hidden boundary defects.

### 3.1 New Code Paths Without Tests
- **Check**: Every newly introduced function, API route, utility, or business logic branch must be accompanied by unit or integration tests.
- **Remediation**: Write automated tests that execute the new codepaths.

### 3.2 Missing Edge Cases & Boundary Conditions
- **Check**: Tests must verify boundary values and failure modes:
  - Nil / null / empty inputs (empty slices, zero-length strings).
  - Minimum and maximum threshold values (0, negative numbers, overflow boundaries).
  - Timeout, network disconnect, and database failure scenarios.
  - Unauthorized or invalid input rejection.
- **Remediation**: Implement table-driven tests covering both happy path and edge-case failure modes.

```go
// GOOD: Table-driven test covering normal, boundary, and error cases
func TestParsePort(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    int
        wantErr bool
    }{
        {name: "valid port", input: "8080", want: 8080, wantErr: false},
        {name: "boundary min", input: "1", want: 1, wantErr: false},
        {name: "boundary max", input: "65535", want: 65535, wantErr: false},
        {name: "empty input", input: "", want: 0, wantErr: true},
        {name: "out of range", input: "70000", want: 0, wantErr: true},
        {name: "non-numeric", input: "abc", want: 0, wantErr: true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParsePort(tt.input)
            if (err != nil) != tt.wantErr {
                t.Fatalf("ParsePort(%q) error = %v, wantErr %v", tt.input, err, tt.wantErr)
            }
            if got != tt.want {
                t.Errorf("ParsePort(%q) = %v, want %v", tt.input, got, tt.want)
            }
        })
    }
}
```
