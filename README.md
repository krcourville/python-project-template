# Python Project Template

Simple start template for use with multiple AWS Lambdas.

> NOTE: Same code is deployed to each lambda. In cloudformation
> you simply wire up a AWS::Severless::Function resource to each handler.

## Benefits of this template

- No additional software or package managers required
- tests "just work" from terminal and VS Code
- test do not have to import `src`
- Minimial VS Code Tooling required

## Caveats of template

- assuming use of aws sam and no additional build steps,
  same code is deployed to each lambda. Possibly a concern
  for large projects or scenarios where it is desired to not deploy
  a large library to all lambdas.
  - Can possibly be offset by lambda layers (which adds some complexity to code and cloudformation)
  - Can possibly of offset by using custom build tasks via makefile (which aws sam seems to support) to only copy the code/modules you want for each lambda.

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
- [poetry](https://python-poetry.org/) (Poetry is not currently part of the template, just borrowed from its project structure)
