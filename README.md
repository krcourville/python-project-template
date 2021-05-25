# Python Project Template

Simple start template for use with multiple AWS Lambdas.

> NOTE: Same code is deployed to each lambda. In cloudformation
> you simply wire up a AWS::Severless::Function resource to each handler.

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

## References

- [pytest - Good Integration Practices](https://docs.pytest.org/en/reorganize-docs/goodpractices.html)
- [python mono repo sample](https://github.com/ya-mori/python-monorepo)
