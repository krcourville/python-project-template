# Python Project Template

Simple start template for use with multiple AWS Lambdas.

> NOTE: Same code is deployed to each lambda. In cloudformation
> you simply wire up a AWS::Severless::Function resource to each handler.

## Benefits of this template

- No additional software required
- tests just work from terminal and VS Code
- test do not have to import `src`
- Minimial VS Code Tooling required

## Caveats of template

- assuming use of aws sam and no additoinal build steps,
  same code is deployed to each lambda. Possibly a concern
  for large projects or scenarios where it is desired to not deploy
  a large library to all lambdas.

## Getting Started

```bash
# set up env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# run unit tests
cd project1
python -m pytest
```

## Use VS Code

Assuming installation of recommended extensions, unit tests will just work with no additional steps

Intellisense will also work with no additional steps.

## TODO

- [ ] Linting
- [ ] Pre-commit hook

## References

- [pytest - Good Integration Practices](https://docs.pytest.org/en/reorganize-docs/goodpractices.html)
- [python mono repo sample](https://github.com/ya-mori/python-monorepo)
