import cx_Freeze

executables = [cx_Freeze.Executable('main.py')]

cx_Freeze.setup(
    name = "Simulação de particula",
    options = {'build.exe': {'packages': ['pygame']}},
    executables = executables
)