from ai.dependency_mediator import resolve_dependencies

requirements = [
    "tensorflow==2.9.0",
    "flask==2.1.0",
    "torch==1.7.0",
    "scipy==1.3.0"
]

resolved = resolve_dependencies(requirements)

print("✅ Final Cleaned Dependencies:")
for r in resolved:
    print("-", r)
