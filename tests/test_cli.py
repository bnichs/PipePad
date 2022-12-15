from pyshelltest import PyShellTestGenerator


generator = PyShellTestGenerator.from_toml("tests/test_cli.toml")
TestCli = generator.generate()
