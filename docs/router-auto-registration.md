# Router Auto-Registration

How the backend automatically discovers and registers all module routers at
startup. There is **no central router include list** — routers are found by
scanning the filesystem.

- Source: `common/router.py` (`RouterRegister`, `APIRouterPro`, `auto_register_routers`)
- Entry point: `server.py:166` calls `auto_register_routers(app)` during `create_app()`

## Overview

Each feature module (`module_admin`, `module_ai`, `module_generator`,
`module_task`, ...) keeps its HTTP routes under a `controller/` directory. At
startup the registrar globs the project tree for those controller files,
imports each one, collects the router objects defined in it, sorts them, and
includes them in the FastAPI app.

```
<module>/controller/<name>_controller.py
        defines a module-level APIRouterPro instance
                        |
                        v
   glob  ->  import  ->  collect routers  ->  sort  ->  app.include_router(...)
```

## The four steps

The work happens in `RouterRegister.register_routers()`, which runs four
private steps.

### 1. Discover controller files

`_find_controller_files()` globs from the backend root:

```python
pattern = os.path.join(self.project_root, '*', 'controller', '[!_]*.py')
return sorted(glob.glob(pattern))
```

The pattern matches `<any-dir>/controller/<file>.py`. Two rules follow from it:

- A module is discovered only if it has a `controller/` subdirectory containing
  matching files. This is why `sub_applications` (which has no `controller/`
  directory) is **not** part of this scan — see "What is not scanned" below.
- The `[!_]` prefix skips files whose names start with an underscore, so
  `__init__.py` and helpers like `_base_controller.py` are ignored.

No module names are hardcoded. Adding a new
`module_x/controller/foo_controller.py` is enough for it to be picked up on the
next startup.

### 2. Import modules and collect routers

`_import_module_and_get_routers()` turns each file path into a dotted module
name, imports it, and walks the module's own `__dict__` for router instances:

```python
module = importlib.import_module(module_name)
for attr_name, attr in module.__dict__.items():
    if isinstance(attr, APIRouterPro):
        if attr.auto_register:          # APIRouterPro can opt out
            routers.append((attr_name, attr))
    elif isinstance(attr, APIRouter):   # plain APIRouter is always included
        routers.append((attr_name, attr))
```

- `APIRouterPro` instances are registered only when `auto_register=True`
  (the default). Set `auto_register=False` to define a router that the scanner
  skips.
- Plain `APIRouter` instances are always registered.

### 3. Sort

`_sort_routers()` orders routers before registration, because FastAPI matches
routes in registration order:

```python
if isinstance(router, APIRouterPro):
    return (0, router.order_num, attr_name)   # APIRouterPro first, by order_num
return (1, attr_name)                          # then plain APIRouter, by name
```

- `APIRouterPro` routers come first, ordered by `order_num` (lower = earlier),
  then by attribute name as a tie-breaker.
- Plain `APIRouter` routers come after, ordered by attribute name.

### 4. Register

`_register_routers_to_app()` calls `app.include_router(router)` for each router
in sorted order.

## How to add an endpoint group

Create a controller file under any module's `controller/` directory with a
module-level `APIRouterPro`:

```python
# module_x/controller/foo_controller.py
from common.router import APIRouterPro

fooController = APIRouterPro(
    prefix='/x/foo',
    order_num=...,          # lower registers earlier
    tags=['foo'],
    dependencies=[...],     # auth / db / data-scope dependencies
)


@fooController.get('/list')
async def list_foo():
    ...
```

It is wired up automatically on the next startup. No edit to any central
registry is required.

### Opting a router out

```python
internalRouter = APIRouterPro(prefix='/internal', auto_register=False)
# discovered during the scan but skipped; include it manually if needed
```

## `APIRouterPro`

`APIRouterPro` extends FastAPI's `APIRouter` and adds two fields used by the
registrar:

- `order_num` (default `100`) — registration order; lower registers earlier.
- `auto_register` (default `True`) — whether the scanner includes this router.

Everything else is standard `APIRouter` (prefix, tags, dependencies, responses,
etc.).

## What is not scanned

`sub_applications` is **not** part of router auto-registration. It has no
`controller/` directory, so the glob never matches it. Sub-applications (for
example static-file serving) are mounted separately:

- `server.py:160` calls `handle_sub_applications(app)`
  (`sub_applications/handle.py`), which calls `mount_staticfiles(app)` to
  `app.mount(...)` the upload directory.

So the order in `create_app()` is: mount sub-applications first
(`server.py:160`), then auto-register module routers (`server.py:166`).

The router scan discovers the four router-bearing modules: `module_admin`,
`module_ai`, `module_generator`, and `module_task`.
