"""Local-only reference screening. Inputs/outputs can be confidential: never deploy them.

Linear Voc temperature model only; not a complete string-sizing calculation.
Current comparisons use STC values, without bifacial gain or design factors.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import cupy as cp


def screen(ref, profile):
    module, inverter = ref['module'], ref['inverter']
    temps = np.linspace(module['minimumOperatingC'], module['maximumOperatingC'], 12601)
    series = np.arange(1, 61)
    voc = np.array([b['voc'] for b in module['bins']])
    beta = module['vocCoefficientPerC']
    limit = min(module['maximumSystemV'], inverter['maximumDcV'])
    # Different algebra on GPU and CPU, double precision on both.
    gpu = cp.asarray(series)[None, :, None] * (
        cp.asarray(voc)[None, None, :] +
        cp.asarray(voc)[None, None, :] * beta * (cp.asarray(temps)[:, None, None] - 25))
    cpu = np.multiply.outer(1 + beta * (temps - 25), series)[:, :, None] * voc
    observed = cp.asnumpy(gpu)
    tolerance = 1e-8
    max_error = float(np.max(np.abs(observed - cpu)))
    # Boundary band reported separately: do not hide floating-point equality effects.
    boundary = np.abs(cpu - limit) <= tolerance
    disagreement = int(np.count_nonzero(((observed > limit) != (cpu > limit)) & ~boundary))
    if not np.isfinite(observed).all() or max_error > tolerance or disagreement:
        raise RuntimeError('Independent reference comparison failed')
    chosen = next(b for b in module['bins'] if b['watts'] == profile['moduleW'])
    n = profile['series']
    crossing = 25 + (limit / (n * chosen['voc']) - 1) / beta if beta else None
    variants = []
    for variant in inverter['variants']:
        parallel = variant['inputsPerMppt']
        variants.append({
            'mppts': variant['mppts'],
            'maximum_input_strings': parallel * variant['mppts'],
            'selected_string_count_fits': profile['stringsPerInverter'] <= parallel * variant['mppts'],
            'fully_populated_mppt_imp_stc_A': parallel * chosen['imp'],
            'operating_limit_exceeded_at_stc': parallel * chosen['imp'] > variant['operatingLimitA'],
            'fully_populated_mppt_isc_stc_A': parallel * chosen['isc'],
            'short_circuit_limit_exceeded_at_stc': parallel * chosen['isc'] > variant['shortCircuitLimitA'],
        })
    return {
        'status': 'numeric comparison passed; engineering admission unresolved',
        'cases': int(cpu.size), 'max_cpu_gpu_error_V': max_error,
        'classification_disagreements_outside_boundary_band': disagreement,
        'boundary_band_cases': int(boundary.sum()),
        'selected_string_voltage_limit_V': limit,
        'selected_linear_voc_crossing_cell_temperature_C': crossing,
        'selected_voc_at_minimum_module_operating_temperature_V': n * chosen['voc'] * (1 + beta * (temps[0] - 25)),
        'variants': variants,
        'missing_checks': ['site design cell temperatures', 'voltage tolerances',
            'bifacial and irradiance current factors', 'MPPT voltage temperature model',
            'installed inverter variant', 'protection coordination', 'cable sizing and routing',
            'approved equipment revision and junction geometry'],
        'scope': 'Private draft reference screening, not approval or probability of safety',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--references', required=True, type=Path)
    parser.add_argument('--profile', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    result = screen(json.loads(args.references.read_text(encoding='utf-8-sig')),
                    json.loads(args.profile.read_text(encoding='utf-8-sig')))
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['status', 'cases', 'max_cpu_gpu_error_V']}))
