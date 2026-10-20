# SPDX-FileCopyrightText: © 2026 Tenstorrent AI ULC
# SPDX-License-Identifier: Apache-2.0

import pytest
from helpers.chip_architecture import is_4row_arch
from helpers.constraints import get_valid_math_fidelities
from helpers.llk_params import (
    PERF_LOOP_FACTOR_QUASAR,
    PERF_RUN_TYPES_QUASAR,
    ImpliedMathFormat,
    Transpose,
)
from helpers.param_config import parametrize, runtime
from quasar.test_matmul_quasar import (
    FULL_MATMUL_SHAPES,
    INT4_BF16_MATMUL_FORMATS,
    INT8_INT8_MATMUL_FORMATS,
    MATMUL_FORMAT,
    MXFP4_BF16_MATMUL_FORMATS,
    MXFP4_MXINT4_MATMUL_FORMATS,
    MXINT4_BF16_MATMUL_FORMATS,
    MXINT4_FP8_MATMUL_FORMATS,
    TINY_MATMUL_FORMATS,
    TINY_MATMUL_SHAPE_CASES,
    matmul_dest_acc_modes,
    matmul_dest_sync_modes,
    matmul_enable_direct_indexing,
    matmul_implied_math_formats,
    matmul_int4_bf16_register_hints,
    matmul_register_format_hints,
    matmul_tile_dimensions,
)
from quasar.test_matmul_quasar import test_matmul as run_matmul


@pytest.mark.perf
@pytest.mark.quasar
@parametrize(
    input_tile_dimensions=runtime(FULL_MATMUL_SHAPES),
    format=MATMUL_FORMAT,
    math_fidelity=lambda format: get_valid_math_fidelities(format),
    dest_sync_mode=lambda: matmul_dest_sync_modes(is_perf=True),
    dest_acc=matmul_dest_acc_modes,
    matmul_tile_dims=runtime(
        lambda dest_acc, dest_sync_mode: matmul_tile_dimensions(
            dest_acc,
            dest_sync_mode,
            exact_dest_fill=True,
            is_perf=True,
        )
    ),
    implied_math_format=lambda format: matmul_implied_math_formats(
        format, is_perf=True
    ),
    register_format_hint=matmul_register_format_hints,
    enable_direct_indexing=matmul_enable_direct_indexing,
    transpose=[Transpose.No],
    run_types=PERF_RUN_TYPES_QUASAR,
    loop_factor=[PERF_LOOP_FACTOR_QUASAR],
    is_perf=[True],
)
def test_perf_matmul_quasar(
    perf_report,
    input_tile_dimensions,
    matmul_tile_dims,
    math_fidelity,
    dest_sync_mode,
    dest_acc,
    format,
    implied_math_format,
    register_format_hint,
    enable_direct_indexing,
    transpose,
    run_types,
    loop_factor,
    is_perf,
):
    run_matmul(
        input_tile_dimensions,
        matmul_tile_dims,
        math_fidelity,
        dest_sync_mode,
        dest_acc,
        format,
        implied_math_format,
        register_format_hint,
        enable_direct_indexing,
        transpose,
        run_types=run_types,
        loop_factor=loop_factor,
        is_perf=is_perf,
        perf_report=perf_report,
    )


def matmul_mixed_precision_perf_parametrize(formats, register_format_hints):
    """Parameterize one separately reported mixed-precision benchmark profile."""
    return parametrize(
        input_tile_dimensions=runtime(FULL_MATMUL_SHAPES),
        format=formats,
        math_fidelity=lambda format: get_valid_math_fidelities(format),
        dest_sync_mode=lambda: matmul_dest_sync_modes(is_perf=True),
        dest_acc=matmul_dest_acc_modes,
        matmul_tile_dims=runtime(
            lambda dest_acc, dest_sync_mode: matmul_tile_dimensions(
                dest_acc,
                dest_sync_mode,
                exact_dest_fill=True,
                is_perf=True,
            )
        ),
        implied_math_format=[ImpliedMathFormat.Yes],
        register_format_hint=register_format_hints,
        enable_direct_indexing=matmul_enable_direct_indexing,
        transpose=[Transpose.No],
        run_types=PERF_RUN_TYPES_QUASAR,
        loop_factor=[PERF_LOOP_FACTOR_QUASAR],
        is_perf=[True],
    )


def _run_mixed_precision_perf_matmul(
    perf_report,
    input_tile_dimensions,
    matmul_tile_dims,
    math_fidelity,
    dest_sync_mode,
    dest_acc,
    format,
    implied_math_format,
    register_format_hint,
    enable_direct_indexing,
    transpose,
    run_types,
    loop_factor,
    is_perf,
):
    run_matmul(
        input_tile_dimensions,
        matmul_tile_dims,
        math_fidelity,
        dest_sync_mode,
        dest_acc,
        format,
        implied_math_format,
        register_format_hint,
        enable_direct_indexing,
        transpose,
        run_types=run_types,
        loop_factor=loop_factor,
        is_perf=is_perf,
        perf_report=perf_report,
    )


@pytest.mark.perf
@pytest.mark.quasar
@matmul_mixed_precision_perf_parametrize(
    INT8_INT8_MATMUL_FORMATS, matmul_register_format_hints
)
def test_perf_matmul_int8_weight_int8_activation(
    perf_report,
    input_tile_dimensions,
    matmul_tile_dims,
    math_fidelity,
    dest_sync_mode,
    dest_acc,
    format,
    implied_math_format,
    register_format_hint,
    enable_direct_indexing,
    transpose,
    run_types,
    loop_factor,
    is_perf,
):
    _run_mixed_precision_perf_matmul(
        perf_report,
        input_tile_dimensions,
        matmul_tile_dims,
        math_fidelity,
        dest_sync_mode,
        dest_acc,
        format,
        implied_math_format,
        register_format_hint,
        enable_direct_indexing,
        transpose,
        run_types,
        loop_factor,
        is_perf,
    )


@pytest.mark.perf
@pytest.mark.quasar
@matmul_mixed_precision_perf_parametrize(
    MXFP4_BF16_MATMUL_FORMATS, matmul_register_format_hints
)
def test_perf_matmul_mxfp4_weight_bf16_activation(
    perf_report,
    input_tile_dimensions,
    matmul_tile_dims,
    math_fidelity,
    dest_sync_mode,
    dest_acc,
    format,
    implied_math_format,
    register_format_hint,
    enable_direct_indexing,
    transpose,
    run_types,
    loop_factor,
    is_perf,
):
    _run_mixed_precision_perf_matmul(
        perf_report,
        input_tile_dimensions,
        matmul_tile_dims,
        math_fidelity,
        dest_sync_mode,
        dest_acc,
        format,
        implied_math_format,
        register_format_hint,
        enable_direct_indexing,
        transpose,
        run_types,
        loop_factor,
        is_perf,
    )


@pytest.mark.perf
@pytest.mark.quasar
@matmul_mixed_precision_perf_parametrize(
    MXFP4_MXINT4_MATMUL_FORMATS, matmul_register_format_hints
)
def test_perf_matmul_mxfp4_mxint4_mixed_weight(
    perf_report,
    input_tile_dimensions,
    matmul_tile_dims,
    math_fidelity,
    dest_sync_mode,
    dest_acc,
    format,
    implied_math_format,
    register_format_hint,
    enable_direct_indexing,
    transpose,
    run_types,
    loop_factor,
    is_perf,
):
    _run_mixed_precision_perf_matmul(
        perf_report,
        input_tile_dimensions,
        matmul_tile_dims,
        math_fidelity,
        dest_sync_mode,
        dest_acc,
        format,
        implied_math_format,
        register_format_hint,
        enable_direct_indexing,
        transpose,
        run_types,
        loop_factor,
        is_perf,
    )


@pytest.mark.perf
@pytest.mark.quasar
@pytest.mark.skipif(
    not is_4row_arch(),
    reason="Int4 is benchmarked through Int8_2x, which exists only on the 4-row Quasar variant",
)
@matmul_mixed_precision_perf_parametrize(
    INT4_BF16_MATMUL_FORMATS, matmul_int4_bf16_register_hints
)
def test_perf_matmul_int4_bf16_mixed_weight(
    perf_report,
    input_tile_dimensions,
    matmul_tile_dims,
    math_fidelity,
    dest_sync_mode,
    dest_acc,
    format,
    implied_math_format,
    register_format_hint,
    enable_direct_indexing,
    transpose,
    run_types,
    loop_factor,
    is_perf,
):
    _run_mixed_precision_perf_matmul(
        perf_report,
        input_tile_dimensions,
        matmul_tile_dims,
        math_fidelity,
        dest_sync_mode,
        dest_acc,
        format,
        implied_math_format,
        register_format_hint,
        enable_direct_indexing,
        transpose,
        run_types,
        loop_factor,
        is_perf,
    )


@pytest.mark.perf
@pytest.mark.quasar
@matmul_mixed_precision_perf_parametrize(
    MXINT4_BF16_MATMUL_FORMATS, matmul_register_format_hints
)
def test_perf_matmul_mxint4_bf16_mixed_weight(
    perf_report,
    input_tile_dimensions,
    matmul_tile_dims,
    math_fidelity,
    dest_sync_mode,
    dest_acc,
    format,
    implied_math_format,
    register_format_hint,
    enable_direct_indexing,
    transpose,
    run_types,
    loop_factor,
    is_perf,
):
    _run_mixed_precision_perf_matmul(
        perf_report,
        input_tile_dimensions,
        matmul_tile_dims,
        math_fidelity,
        dest_sync_mode,
        dest_acc,
        format,
        implied_math_format,
        register_format_hint,
        enable_direct_indexing,
        transpose,
        run_types,
        loop_factor,
        is_perf,
    )


@pytest.mark.perf
@pytest.mark.quasar
@matmul_mixed_precision_perf_parametrize(
    MXINT4_FP8_MATMUL_FORMATS, matmul_register_format_hints
)
def test_perf_matmul_mxint4_fp8_mixed_weight(
    perf_report,
    input_tile_dimensions,
    matmul_tile_dims,
    math_fidelity,
    dest_sync_mode,
    dest_acc,
    format,
    implied_math_format,
    register_format_hint,
    enable_direct_indexing,
    transpose,
    run_types,
    loop_factor,
    is_perf,
):
    _run_mixed_precision_perf_matmul(
        perf_report,
        input_tile_dimensions,
        matmul_tile_dims,
        math_fidelity,
        dest_sync_mode,
        dest_acc,
        format,
        implied_math_format,
        register_format_hint,
        enable_direct_indexing,
        transpose,
        run_types,
        loop_factor,
        is_perf,
    )


@pytest.mark.perf
@pytest.mark.quasar
@parametrize(
    input_tile_dimensions=runtime(TINY_MATMUL_SHAPE_CASES),
    format=TINY_MATMUL_FORMATS,
    math_fidelity=lambda format: get_valid_math_fidelities(format),
    dest_sync_mode=lambda: matmul_dest_sync_modes(is_perf=True),
    dest_acc=matmul_dest_acc_modes,
    matmul_tile_dims=runtime(
        lambda dest_acc, dest_sync_mode: matmul_tile_dimensions(
            dest_acc,
            dest_sync_mode,
            exact_dest_fill=True,
            is_perf=True,
        )
    ),
    implied_math_format=lambda format: matmul_implied_math_formats(
        format, is_perf=True
    ),
    register_format_hint=matmul_register_format_hints,
    enable_direct_indexing=matmul_enable_direct_indexing,
    transpose=[Transpose.No],
    run_types=PERF_RUN_TYPES_QUASAR,
    loop_factor=[PERF_LOOP_FACTOR_QUASAR],
    is_perf=[True],
)
def test_perf_matmul_tiny_quasar(
    perf_report,
    input_tile_dimensions,
    math_fidelity,
    dest_sync_mode,
    dest_acc,
    matmul_tile_dims,
    format,
    implied_math_format,
    register_format_hint,
    enable_direct_indexing,
    transpose,
    run_types,
    loop_factor,
    is_perf,
):
    run_matmul(
        input_tile_dimensions,
        matmul_tile_dims,
        math_fidelity,
        dest_sync_mode,
        dest_acc,
        format,
        implied_math_format,
        register_format_hint,
        enable_direct_indexing,
        transpose,
        run_types=run_types,
        loop_factor=loop_factor,
        is_perf=is_perf,
        perf_report=perf_report,
    )
