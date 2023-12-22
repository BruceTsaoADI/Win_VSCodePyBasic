/*
 * File:           C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\01_Project\20230815_Audio\02_Project\20230912_ANC NTU\03_SW\SigmaProject\20231027_MCUImplementTutorial\Export\SineTone_IC_1_SIGMA_PARAM.h
 *
 * Created:        Monday, December 11, 2023 3:03:48 PM
 * Description:    SineTone:IC 1-Sigma parameter RAM definitions.
 *
 * This software is distributed in the hope that it will be useful,
 * but is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
 * CONDITIONS OF ANY KIND, without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * This software may only be used to program products purchased from
 * Analog Devices for incorporation by you into audio products that
 * are intended for resale to audio product end users. This software
 * may not be distributed whole or in any part to third parties.
 *
 * Copyright ©2023 Analog Devices, Inc. All rights reserved.
 */
#ifndef __SINETONE_IC_1_SIGMA_PARAM_H__
#define __SINETONE_IC_1_SIGMA_PARAM_H__


/* Module Non Modulo Location Start - Non Modulo Location Start*/
#define MOD_NONMODULOLOCATIONSTART_COUNT               1
#define MOD_NONMODULOLOCATIONSTART_DEVICE              "IC1_Sigma"
#define MOD_NONMODULOLOCATIONSTART_NON_MODULO_LOCATION_START_ADDR 8192
#define MOD_NONMODULOLOCATIONSTART_NON_MODULO_LOCATION_START_FIXPT 0x00000800
#define MOD_NONMODULOLOCATIONSTART_NON_MODULO_LOCATION_START_VALUE SIGMASTUDIOTYPE_INTEGER_CONVERT(2048)
#define MOD_NONMODULOLOCATIONSTART_NON_MODULO_LOCATION_START_TYPE SIGMASTUDIOTYPE_INTEGER

/* Module SafeLoadModule - SafeLoadModule*/
#define MOD_SAFELOADMODULE_COUNT                       7
#define MOD_SAFELOADMODULE_DEVICE                      "IC1_Sigma"
#define MOD_SAFELOADMODULE_DATALOADSTART_SAFELOAD_ADDR 8196
#define MOD_SAFELOADMODULE_DATALOAD1_SAFELOAD_ADDR     8200
#define MOD_SAFELOADMODULE_DATALOAD2_SAFELOAD_ADDR     8204
#define MOD_SAFELOADMODULE_DATALOAD3_SAFELOAD_ADDR     8208
#define MOD_SAFELOADMODULE_DATALOADEND_SAFELOAD_ADDR   8212
#define MOD_SAFELOADMODULE_ADDRESSLOAD_SAFELOAD_ADDR   8216
#define MOD_SAFELOADMODULE_NUMLOAD_SAFELOAD_ADDR       8220

/* Module Coefficient Offset Location Start - Coefficient Offset Location Start*/
#define MOD_COEFFICIENTOFFSETLOCATIONSTART_COUNT       1
#define MOD_COEFFICIENTOFFSETLOCATIONSTART_DEVICE      "IC1_Sigma"
#define MOD_COEFFICIENTOFFSETLOCATIONSTART_COEFFICIENT_OFFSET_LOCATION_START_ADDR 8224
#define MOD_COEFFICIENTOFFSETLOCATIONSTART_COEFFICIENT_OFFSET_LOCATION_START_FIXPT 0x00002004
#define MOD_COEFFICIENTOFFSETLOCATIONSTART_COEFFICIENT_OFFSET_LOCATION_START_VALUE SIGMASTUDIOTYPE_INTEGER_CONVERT(8196)
#define MOD_COEFFICIENTOFFSETLOCATIONSTART_COEFFICIENT_OFFSET_LOCATION_START_TYPE SIGMASTUDIOTYPE_INTEGER

/* Module Tone1 - Sine Tone*/
#define MOD_TONE1_COUNT                                3
#define MOD_TONE1_DEVICE                               "IC1_Sigma"
#define MOD_STATIC_TONE1_ALG0_MASK_ADDR                8228
#define MOD_STATIC_TONE1_ALG0_MASK_FIXPT               0x000000FF
#define MOD_STATIC_TONE1_ALG0_MASK_VALUE               SIGMASTUDIOTYPE_INTEGER_CONVERT(255)
#define MOD_STATIC_TONE1_ALG0_MASK_TYPE                SIGMASTUDIOTYPE_INTEGER
#define MOD_TONE1_ALG0_INCREMENT_ADDR                  8232
#define MOD_TONE1_ALG0_INCREMENT_FIXPT                 0x00055555
#define MOD_TONE1_ALG0_INCREMENT_VALUE                 SIGMASTUDIOTYPE_FIXPOINT_CONVERT(0.0416666666666667)
#define MOD_TONE1_ALG0_INCREMENT_TYPE                  SIGMASTUDIOTYPE_FIXPOINT
#define MOD_TONE1_ALG0_ON_ADDR                         8236
#define MOD_TONE1_ALG0_ON_FIXPT                        0x00800000
#define MOD_TONE1_ALG0_ON_VALUE                        SIGMASTUDIOTYPE_FIXPOINT_CONVERT(1)
#define MOD_TONE1_ALG0_ON_TYPE                         SIGMASTUDIOTYPE_FIXPOINT

/* Module Tone2 - Sine Tone*/
#define MOD_TONE2_COUNT                                3
#define MOD_TONE2_DEVICE                               "IC1_Sigma"
#define MOD_STATIC_TONE2_ALG0_MASK_ADDR                8240
#define MOD_STATIC_TONE2_ALG0_MASK_FIXPT               0x000000FF
#define MOD_STATIC_TONE2_ALG0_MASK_VALUE               SIGMASTUDIOTYPE_INTEGER_CONVERT(255)
#define MOD_STATIC_TONE2_ALG0_MASK_TYPE                SIGMASTUDIOTYPE_INTEGER
#define MOD_TONE2_ALG0_INCREMENT_ADDR                  8244
#define MOD_TONE2_ALG0_INCREMENT_FIXPT                 0x0002AAAE
#define MOD_TONE2_ALG0_INCREMENT_VALUE                 SIGMASTUDIOTYPE_FIXPOINT_CONVERT(0.02083375)
#define MOD_TONE2_ALG0_INCREMENT_TYPE                  SIGMASTUDIOTYPE_FIXPOINT
#define MOD_TONE2_ALG0_ON_ADDR                         8248
#define MOD_TONE2_ALG0_ON_FIXPT                        0x00800000
#define MOD_TONE2_ALG0_ON_VALUE                        SIGMASTUDIOTYPE_FIXPOINT_CONVERT(1)
#define MOD_TONE2_ALG0_ON_TYPE                         SIGMASTUDIOTYPE_FIXPOINT

#endif
