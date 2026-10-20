// SPDX-FileCopyrightText: © 2026 Tenstorrent USA, Inc.
//
// SPDX-License-Identifier: Apache-2.0

#pragma once

#include "ckernel.h"
#include "ckernel_defs.h"
#include "cmath_common.h"
#include "sfpi.h"

namespace ckernel {
namespace sfpu {

inline void left_shift_init() { math::_reset_counters_<p_setrwc::SET_ABD_F>(); }

// Left shift by an immediate scalar amount. If shift amount is >= 32, the result is 0.
template <bool APPROXIMATION_MODE, DataFormat DATA_FORMAT = DataFormat::Int32, int ITERATIONS = 8>
inline void calculate_left_shift(const uint shift_amt) {
    // Quasar has no UInt32 data format, so only Int32 and UInt16 remain.
    static_assert(
        DATA_FORMAT == DataFormat::Int32 || DATA_FORMAT == DataFormat::UInt16,
        "Unsupported data format for shift operation. Supported data formats are: Int32, UInt16");
    const bool out_of_range = shift_amt >= 32;
    // SFPI overloads both `vInt << unsigned` and `vUInt << unsigned`, so the shift amount's type is
    // independent of the element type being shifted. Cast to a 32-bit `unsigned` so shift is chosen exactly.
    const unsigned amt = static_cast<unsigned>(shift_amt);
#pragma GCC unroll 8
    for (int d = 0; d < ITERATIONS; d++) {
        if constexpr (DATA_FORMAT == DataFormat::UInt16) {
            sfpi::vUInt v = sfpi::dst_reg[0].mode<sfpi::DataLayout::U16>();
            sfpi::dst_reg[0].mode<sfpi::DataLayout::U16>() = out_of_range ? sfpi::vUInt(0u) : (v << amt);
        } else {
            sfpi::vInt v = sfpi::dst_reg[0].mode<sfpi::DataLayout::I32>();
            sfpi::dst_reg[0].mode<sfpi::DataLayout::I32>() = out_of_range ? sfpi::vInt(0) : (v << amt);
        }
        sfpi::dst_reg++;
    }
}

inline void right_shift_init() { math::_reset_counters_<p_setrwc::SET_ABD_F>(); }

// SMAG32 right shift used by the Quasar quantization API. The magnitude is
// shifted and the original sign bit is restored, including for a zero result.
// The Blackhole implementation only has defined inputs for shift amounts
// [0, 31]; clamp larger runtime values defensively to 31 to avoid a C++ shift
// by 32. In the rounded variant, callers must also ensure
// |input| + 2^(shift-1) <= INT32_MAX for shift > 0.
template <bool ROUND_TO_NEAREST, int ITERATIONS = 8>
inline void calculate_right_shift_sm_impl(const uint shift_amt) {
    constexpr std::uint32_t magnitude_mask = 0x7fffffffu;
    constexpr std::uint32_t sign_mask = 0x80000000u;
    const unsigned shift = shift_amt > 31 ? 31u : static_cast<unsigned>(shift_amt);
    const std::uint32_t rounding_bit = (ROUND_TO_NEAREST && shift > 0) ? (1u << (shift - 1)) : 0u;

#pragma GCC unroll 8
    for (int d = 0; d < ITERATIONS; d++) {
        sfpi::vSMag input = sfpi::dst_reg[0].mode<sfpi::DataLayout::SM32>();
        sfpi::vUInt raw = sfpi::as<sfpi::vUInt>(input);
        sfpi::vUInt magnitude = raw & magnitude_mask;
        magnitude += rounding_bit;
        sfpi::vUInt result = (magnitude >> shift) | (raw & sign_mask);
        sfpi::dst_reg[0].mode<sfpi::DataLayout::SM32>() = sfpi::as<sfpi::vSMag>(result);
        sfpi::dst_reg++;
    }
}

template <bool APPROXIMATION_MODE, int ITERATIONS = 8>
inline void calculate_right_shift_sm_with_rounding(const uint shift_amt) {
    calculate_right_shift_sm_impl<true, ITERATIONS>(shift_amt);
}

template <bool APPROXIMATION_MODE, int ITERATIONS = 8>
inline void calculate_right_shift_sm(const uint shift_amt) {
    if constexpr (APPROXIMATION_MODE) {
        calculate_right_shift_sm_impl<false, ITERATIONS>(shift_amt);
    } else {
        calculate_right_shift_sm_with_rounding<APPROXIMATION_MODE, ITERATIONS>(shift_amt);
    }
}

// Right shift by an immediate scalar amount. Signed data uses an arithmetic
// shift; unsigned data uses a logical shift.
// A shift amount >= 32 saturates to 31.
template <bool APPROXIMATION_MODE, DataFormat DATA_FORMAT = DataFormat::Int32, int ITERATIONS = 8>
inline void calculate_right_shift(const uint shift_amt) {
    // Quasar has no UInt32 data format, so only Int32 and UInt16 remain.
    static_assert(
        DATA_FORMAT == DataFormat::Int32 || DATA_FORMAT == DataFormat::UInt16,
        "Unsupported data format for shift operation. Supported data formats are: Int32, UInt16");
    // SFPI overloads both `vInt << unsigned` and `vUInt << unsigned`, so the shift amount's type is
    // independent of the element type being shifted. Cast to a 32-bit `unsigned` so shift is chosen exactly.
    const unsigned eff = (shift_amt >= 32) ? 31u : static_cast<unsigned>(shift_amt);
    const unsigned sign_mask = (eff > 0) ? (~0u << (32 - eff)) : 0u;
#pragma GCC unroll 8
    for (int d = 0; d < ITERATIONS; d++) {
        if constexpr (DATA_FORMAT == DataFormat::UInt16) {
            sfpi::vUInt v = sfpi::dst_reg[0].mode<sfpi::DataLayout::U16>();
            sfpi::dst_reg[0].mode<sfpi::DataLayout::U16>() = v >> eff;
        } else {
            sfpi::vInt v = sfpi::dst_reg[0].mode<sfpi::DataLayout::I32>();
            sfpi::vUInt res = sfpi::as<sfpi::vUInt>(v) >> eff;
            if constexpr (DATA_FORMAT == DataFormat::Int32) {
                v_if(v < 0) { res = res | sign_mask; }
                v_endif;
            }
            sfpi::dst_reg[0].mode<sfpi::DataLayout::I32>() = sfpi::as<sfpi::vInt>(res);
        }
        sfpi::dst_reg++;
    }
}

}  // namespace sfpu
}  // namespace ckernel
