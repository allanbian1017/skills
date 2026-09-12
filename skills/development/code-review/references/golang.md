# Go Style Guide (Uber Go Hybrid Rubric)

This reference defines the coding standards for Go codebases derived from the Uber Go Style Guide. It is split into binary-evaluable Rubric Rules (which contribute to the style compliance score) and Contextual Guidelines (which provide non-scoring advisory feedback requiring engineering judgment).

## Category Index
- **Guidelines**: Core Go idioms, error handling, safety, lifecycle management, and concurrency.
- **Performance**: High-efficiency idioms for allocations, strings, and collections.
- **Style**: Code formatting, naming, variable scoping, and declarations.
- **Patterns**: Idiomatic Go structural and testing patterns.

---

# Rubric Rules

Binary pass/fail checks evaluated during style reviews. Each rule impacts the automated style compliance score.

### R-GO-01: Error Wrapping
- **Severity**: HIGH
- **Category**: Guidelines
- **Check**: Wrap error context using `fmt.Errorf` with `%w`. Do not use `%s` or `%v` which discards error unwrapping chains.
- **Bad**: `fmt.Errorf("open config: %v", err)`
- **Good**: `fmt.Errorf("open config: %w", err)`

### R-GO-02: Don't Panic
- **Severity**: HIGH
- **Category**: Guidelines
- **Check**: Normal application and library code must return errors to callers rather than invoking `panic()`.
- **Bad**: `if err != nil { panic(err) }`
- **Good**: `if err != nil { return fmt.Errorf("read failed: %w", err) }`

### R-GO-03: Handle Type Assertion Failures
- **Severity**: HIGH
- **Category**: Guidelines
- **Check**: Use the two-value comma-ok syntax for type assertions to prevent unhandled runtime panics.
- **Bad**: `val := data.(string)`
- **Good**: `val, ok := data.(string); if !ok { return errors.New("data is not a string") }`

### R-GO-04: Handle Errors Once
- **Severity**: HIGH
- **Category**: Guidelines
- **Check**: Handle an error exactly once: either log it or return it to the caller, never do both.
- **Bad**: `log.Errorf("query failed: %v", err); return err`
- **Good**: `return fmt.Errorf("query failed: %w", err)`

### R-GO-05: Exit Only in Main
- **Severity**: HIGH
- **Category**: Guidelines
- **Check**: Call `os.Exit` or `log.Fatal*` only from `main()`. All library and helper functions must return an error instead.
- **Bad**: `func connectDB() { if err != nil { log.Fatalf("db err: %v", err) } }`
- **Good**: `func connectDB() error { if err != nil { return fmt.Errorf("db err: %w", err) }; return nil }`

### R-GO-06: Pointers to Interfaces
- **Severity**: HIGH
- **Category**: Guidelines
- **Check**: Do not accept or return pointers to interfaces (`*Interface`). Interfaces already hold pointer or value data.
- **Bad**: `func Process(r *io.Reader) error`
- **Good**: `func Process(r io.Reader) error`

### R-GO-07: Goroutine Lifetimes
- **Severity**: HIGH
- **Category**: Guidelines
- **Check**: Never spawn fire-and-forget goroutines without a wait mechanism (`sync.WaitGroup`, `errgroup`) or context cancellation.
- **Bad**: `go worker.Run()`
- **Good**: `g.Go(func() error { return worker.Run(ctx) })`

### R-GO-08: Use Time Package for Durations
- **Severity**: HIGH
- **Category**: Guidelines
- **Check**: Use `time.Time` for timestamps and `time.Duration` for intervals. Do not pass raw integers or floats for durations.
- **Bad**: `func Poll(intervalMs int)`
- **Good**: `func Poll(interval time.Duration)`

### R-GO-09: Avoid Mutable Globals
- **Severity**: HIGH
- **Category**: Guidelines
- **Check**: Do not expose mutable package-level global variables. Use unexported variables with getter functions or instance structs.
- **Bad**: `var Registry = make(map[string]Service)`
- **Good**: `var _registry = make(map[string]Service); func GetService(name string) (Service, bool) { v, ok := _registry[name]; return v, ok }`

### R-GO-10: Defer Resource Cleanup
- **Severity**: MEDIUM
- **Category**: Guidelines
- **Check**: Use `defer` to clean up resources (files, locks, network connections) immediately after acquisition.
- **Bad**: `mu.Lock(); doWork(); mu.Unlock()`
- **Good**: `mu.Lock(); defer mu.Unlock(); doWork()`

### R-GO-11: Consistent Receiver Types
- **Severity**: MEDIUM
- **Category**: Guidelines
- **Check**: Do not mix value and pointer receivers on the same struct type. If any method requires a pointer receiver, use pointer receivers for all methods.
- **Bad**: `func (s *Service) Start() error; func (s Service) Status() string`
- **Good**: `func (s *Service) Start() error; func (s *Service) Status() string`

### R-GO-12: Avoid init()
- **Severity**: MEDIUM
- **Category**: Guidelines
- **Check**: Avoid `init()` functions for side effects or state initialization. Use explicit constructor functions instead.
- **Bad**: `func init() { dbConn = connectDB() }`
- **Good**: `func NewDB(cfg Config) (*DB, error) { return connectDB(cfg) }`

### R-GO-13: Field Tags in Marshaled Structs
- **Severity**: MEDIUM
- **Category**: Guidelines
- **Check**: Explicitly specify field tags (`json:"..."`, `yaml:"..."`) on all fields of structs serialized across boundaries.
- **Bad**: `type User struct { Name string; Age int }`
- **Good**: ``type User struct { Name string `json:"name"`; Age int `json:"age"` }``

### R-GO-14: Start Enums at One
- **Severity**: MEDIUM
- **Category**: Guidelines
- **Check**: Enums declared with `iota` must start at 1 unless zero is an explicit and valid default value.
- **Bad**: `type State int; const (Active State = iota; Inactive)`
- **Good**: `type State int; const (Unknown State = iota; Active; Inactive)`

### R-GO-15: Error Naming Conventions
- **Severity**: LOW
- **Category**: Guidelines
- **Check**: Static error variables must start with `Err` or `err`. Custom error types must end with `Error`.
- **Bad**: `var TimeoutError = errors.New("timeout"); type MalformedPayload struct{}`
- **Good**: `var ErrTimeout = errors.New("timeout"); type MalformedPayloadError struct{}`

### R-GO-16: Preallocate Slice and Map Capacity
- **Severity**: MEDIUM
- **Category**: Performance
- **Check**: Specify initial capacity with `make([]T, 0, cap)` or `make(map[K]V, cap)` when the size is known in advance.
- **Bad**: `var out []int; for _, v := range src { out = append(out, v.ID) }`
- **Good**: `out := make([]int, 0, len(src)); for _, v := range src { out = append(out, v.ID) }`

### R-GO-17: Prefer strconv over fmt
- **Severity**: MEDIUM
- **Category**: Performance
- **Check**: Use `strconv` functions (`strconv.Itoa`, `strconv.FormatInt`) instead of `fmt.Sprintf` for primitive conversions.
- **Bad**: `s := fmt.Sprintf("%d", userID)`
- **Good**: `s := strconv.Itoa(userID)`

### R-GO-18: Avoid Repeated String-to-Byte Conversions
- **Severity**: MEDIUM
- **Category**: Performance
- **Check**: Do not convert strings to `[]byte` inside loops or repetitive blocks. Convert once outside the iteration.
- **Bad**: `for _, writer := range writers { writer.Write([]byte(msg)) }`
- **Good**: `b := []byte(msg); for _, writer := range writers { writer.Write(b) }`

### R-GO-19: Reduce Nesting (Guard Clauses)
- **Severity**: MEDIUM
- **Category**: Style
- **Check**: Handle error cases and edge conditions early with guard clauses to minimize indentation levels.
- **Bad**: `if err == nil { if user.Valid { return execute() } } else { return err }`
- **Good**: `if err != nil { return err }; if !user.Valid { return ErrInvalidUser }; return execute()`

### R-GO-20: No Unnecessary Else
- **Severity**: LOW
- **Category**: Style
- **Check**: Do not use `else` or `else if` following a block that terminates with `return`, `break`, `continue`, or `panic`.
- **Bad**: `if val < 0 { return -val } else { return val }`
- **Good**: `if val < 0 { return -val }; return val`

### R-GO-21: Import Group Ordering
- **Severity**: LOW
- **Category**: Style
- **Check**: Organize imports into three grouped blocks separated by empty lines: standard library, third-party packages, internal packages.
- **Bad**: `import ("fmt"; "github.com/uber-go/zap"; "strings")`
- **Good**: `import ("fmt"\n\t"strings"\n\n\t"github.com/uber-go/zap")`

### R-GO-22: Use Field Names to Initialize Structs
- **Severity**: MEDIUM
- **Category**: Style
- **Check**: Always specify explicit field names when instantiating structs. Do not use positional value initialization.
- **Bad**: `pt := Point{10, 20}`
- **Good**: `pt := Point{X: 10, Y: 20}`

### R-GO-23: Nil is Valid Slice
- **Severity**: MEDIUM
- **Category**: Style
- **Check**: Return `nil` rather than an empty slice literal `[]T{}` when returning an empty slice, and check empty via `len(s) == 0`.
- **Bad**: `if len(src) == 0 { return []string{} }`
- **Good**: `if len(src) == 0 { return nil }`

### R-GO-24: Top-Level Variable Declarations
- **Severity**: LOW
- **Category**: Style
- **Check**: Use the `var` keyword for top-level package declarations. Short variable declaration (`:=`) is not allowed at package scope.
- **Bad**: `_defaultPort := 8080`
- **Good**: `var _defaultPort = 8080`

### R-GO-25: Prefix Unexported Top-Level Variables
- **Severity**: LOW
- **Category**: Style
- **Check**: Prefix unexported package-level variables and constants with an underscore `_` to clarify package scope and prevent shadowing.
- **Bad**: `var defaultTimeout = 30 * time.Second`
- **Good**: `var _defaultTimeout = 30 * time.Second`

### R-GO-26: Avoid Shadowing Built-In Identifiers
- **Severity**: LOW
- **Category**: Style
- **Check**: Do not declare variables or parameters named after Go predeclared built-ins (`string`, `error`, `len`, `make`, `new`, `cap`, `close`).
- **Bad**: `func Process(string string, error error)`
- **Good**: `func Process(msg string, cause error)`

### R-GO-27: Table-Driven Tests
- **Severity**: MEDIUM
- **Category**: Patterns
- **Check**: Write unit tests using table-driven test slices with named cases executed via `t.Run(tt.name, ...)`.
- **Bad**: `func TestParse(t *testing.T) { assert(Parse("a") == 1); assert(Parse("b") == 2) }`
- **Good**: `tests := []struct{name string; in string; want int}{{...}}; for _, tt := range tests { t.Run(tt.name, func(t *testing.T) { ... }) }`

---

# Contextual Guidelines

Judgment-based rules evaluated qualitatively during code reviews. These provide advisory comments without impacting the numerical style score.

### C-GO-01: Pointer vs Value Receivers
- **Category**: Guidelines
- **Description**: Methods can bind to value receivers or pointer receivers.
- **Guidance**: Use pointer receivers if the method mutates the receiver, if the struct contains synchronization primitives (such as `sync.Mutex`), or if the struct is large. Use value receivers for small, immutable types or basic type aliases. When in doubt, prefer pointer receivers.

### C-GO-02: Copy Slices and Maps at Boundaries
- **Category**: Guidelines
- **Description**: Slices and maps store references to backing arrays and hash tables, allowing unexpected caller mutations across boundaries.
- **Guidance**: Make defensive copies when storing slices or maps passed in from external callers or returning internal state to callers. Skip defensive copying only in internal, performance-critical paths where ownership transfer is clearly documented.

### C-GO-03: Zero-Value Mutexes and Struct Embedding
- **Category**: Guidelines
- **Description**: Go mutexes (`sync.Mutex` and `sync.RWMutex`) are initialized and valid at zero value without pointer allocation.
- **Guidance**: Keep mutexes as value fields (`mu sync.Mutex`). Do not allocate pointers to mutexes. Keep mutexes unexported rather than embedding them directly in public structs, preventing external callers from acquiring or unlocking internal locks.

### C-GO-04: Channel Sizing and Concurrency Coordination
- **Category**: Guidelines
- **Description**: Channels should default to unbuffered (size zero) or single-element buffer (size one).
- **Guidance**: Unbuffered channels synchronize goroutine execution cleanly. A buffer of one is suitable for non-blocking sends or signal tokens. Buffers larger than one require explicit design justification documenting queue boundaries, memory limits, and backpressure behavior.

### C-GO-05: Interface Compliance Verification
- **Category**: Guidelines
- **Description**: Verifying that a concrete type satisfies an interface contract at compile time.
- **Guidance**: Use explicit type assertion assignments (`var _ Handler = (*HandlerImpl)(nil)`) when declaring types intended to implement an interface that lacks a static constructor return type check, ensuring compilation breaks if interface definitions change.

### C-GO-06: Avoid Embedding Types in Public Structs
- **Category**: Guidelines
- **Description**: Struct embedding hoists all inner fields and methods into the outer struct's exported surface.
- **Guidance**: Avoid embedding inner structs in public types unless you explicitly want to expose all methods of the embedded type. Prefer explicit composition with named unexported fields to maintain encapsulation and decouple API evolution.

### C-GO-07: Atomic Primitives vs Mutexes
- **Category**: Performance
- **Description**: Synchronization using atomic operations (`go.uber.org/atomic` or `sync/atomic`) versus locks.
- **Guidance**: Use atomic primitives for single independent values, such as counters, boolean flags, or monotonic sequence IDs. When two or more shared variables must be read and updated together atomically, always use a `sync.Mutex` or `sync.RWMutex`.

### C-GO-08: Functional Grouping and Ordering
- **Category**: Style
- **Description**: The logical ordering and grouping of functions, types, and methods within source files.
- **Guidance**: Arrange functions logically in top-down call order: constructors first right after type declarations, followed by exported methods, followed by unexported helper functions. Group related methods together, and keep interface implementations adjacent.

### C-GO-09: Avoid Naked Parameters
- **Category**: Style
- **Description**: Function invocations with literal boolean, integer, or nil values obscure semantic meaning.
- **Guidance**: When passing literal values whose purpose is not obvious from argument context, define explicit named constants, use functional options, or annotate call sites with C-style comments (e.g., `process(/* enableCache = */ false)`).

### C-GO-10: Line Length and Visual Wrap
- **Category**: Style
- **Description**: Formatting code with sensible line lengths to ensure readability in diffs and code review tools.
- **Guidance**: Aim for lines under 99 characters where practical. When wrapping long expressions, break after operators or commas, and indent wrapped argument lists consistently. Avoid excessive one-line chaining that obscures error checking or intermediate states.

### C-GO-11: Package Naming and Granularity
- **Category**: Style
- **Description**: Package names should be concise, cohesive, and clearly identify the package's single responsibility.
- **Guidance**: Use short, lowercase, single-word names with no underscores or mixedCaps. Avoid generic catch-all packages like `util`, `common`, or `helper`. If a package grows too large or encompasses unrelated responsibilities, split it along functional domains.

### C-GO-12: Functional Options Pattern
- **Category**: Patterns
- **Description**: Configuration pattern for constructors and public APIs with multiple optional parameters.
- **Guidance**: Use functional options (`type Option func(*Server)`) for public APIs and constructors with 3 or more optional configurations to provide backwards-compatible extensibility. For internal or simple constructors, a standard configuration struct is simpler and preferred.
