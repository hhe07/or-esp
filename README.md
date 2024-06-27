# instructions

- acquire a copy of embench
- in your fusesoc installation folder, run ``abspath.py`` (making sure that ``inpath`` matches the name of the config file)
- copy the output of ``abspath.py``.
  - (optional, saves a command line flag) in ``run_fusesoc.py``, change the default value of ``--config-path`` to the directory name you just copied
  - otherwise, add ``--config-path {path_to_fusesoc_abs.conf}`` to the command line options
- copy the ``config/openrisc`` directory into ``config/`` of the embench copy
- copy the ``pylib/run_fusesoc.py`` support file into ``pylib/`` of the embench copy
- in the embench directory, run ``./benchmark_speed.py --timeout 120 --target-module run_fusesoc --fusesoc_target {target} ``
  - where ``{target}`` can either be ``marocchino_tb`` or ``mor1kx_tb``
  - the modified timeout is recommended specifically for ``marocchino``.
  - additional args can obviously be included, but check ``run_fusesoc.py`` and ``benchmark_speed.py`` for what is supported.
