#!/usr/bin/env python3

# Python module to run programs using FuseSoC.

"""
Embench module to run benchmark programs.

This version is suitable for running programs natively.
"""

__all__ = [
    'get_target_args',
    'build_benchmark_cmd',
    'decode_results',
]

import argparse
import re

from embench_core import log

cpu_mhz = 1

def get_target_args(remnant):
    """Parse left over arguments"""
    parser = argparse.ArgumentParser(description='Get target specific args')


    parser.add_argument(
        '--config-path',
        type=str,
        default='/home/hhe07/Documents/openrisc/fusesoc/fusesoc_abs.conf',
        help='path to fusesoc.conf. config file must be absolute.'
    )

    parser.add_argument(
        '--target',
        type=str,
        default='mor1kx_tb',
        help='target to test'
    )

    parser.add_argument(
        '--tool',
        type=str,
        default='verilator',
        help='tool to use (verilator highly recommended)'
    )

    parser.add_argument(
        '--system',
        type=str,
        default='::mor1kx-generic:1.1',
        help='soc to test'
    )

    parser.add_argument(
        '--fusesoc_target',
        type=str,
        default='mor1kx_tb',
        help='soc to test'
    )

    parser.add_argument(
        '--ext_args',
        type=str,
        default='',
        help='extra args to pass after all other arguments (i.e. to turn on tracing)'
    )

    # No target arguments
    return parser.parse_args(remnant)


def build_benchmark_cmd(bench, args):
    """Construct the command to run the benchmark.  "args" is a
       namespace with target specific arguments"""

    # Due to way the target interface currently works we need to construct
    # a command that records both the return value and execution time to
    # stdin/stdout. Obviously using time will not be very precise.
    out = [
        'fusesoc', '--config', args.config_path, 'run', '--target', args.fusesoc_target, '--tool', args.tool, args.system, '--elf_load', f'./{bench}'
    ]

    out.extend(['--trace_to_screen', '--vcd', 'wow.vcd'])

    """ if args.ext_args != '':
        out.extend([args.ext_args]) """

    return out


def decode_results(stdout_str, stderr_str):
    """Extract the results from the output string of the run. Return the
       elapsed time in milliseconds or zero if the run failed."""
    # See above in build_benchmark_cmd how we record the return value and
    # execution time. Return code is in standard output. Execution time is in
    # standard error.

    # Match "RET=rc"
    rcstr = re.search('Success\! Got NOP\_EXIT', stdout_str, re.S)
    if not rcstr:
        log.debug('Warning: Failed to find return code')
        return 0.0

    # Match "real s.mm?m?"
    time = re.search('Simulation ended at PC = ([0-9A-Fa-f]+) \((\d+)\)', stdout_str, re.S)
    if time:
        global cpu_mhz
        ms_elapsed = int(time.group(2)) / cpu_mhz / 1000.0
        # Return value cannot be zero (will be interpreted as error)
        return max(float(ms_elapsed), 0.001)

    # We must have failed to find a time
    log.debug('Warning: Failed to find timing')
    return 0.0
