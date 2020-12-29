/*
 * board.hpp
 *
 *  Created on: 11 dic. 2020
 *      Author: IbonZalbide
 */

#ifndef BOARD_HPP_
#define BOARD_HPP_

#include <splitFlap/SplitFlap.h>
#include <nvm/nvm.h>

/* SPLIT-FLAP CONFIGURATIONS */
static const SplitFlapDef hhSplitFlapDef = {
                .stepperDef = {
                    .gpoDefs[0]={&P3DIR, &P3OUT, BIT6},
                    .gpoDefs[1]={&P3DIR, &P3OUT, BIT2},
                    .gpoDefs[2]={&P3DIR, &P3OUT, BIT5},
                    .gpoDefs[3]={&P2DIR, &P2OUT, BIT7},
                    .direction=ClockWise,
                    .divisor=3},
                .detectorDef = {
                    .enableGpoDef={&P2DIR, &P2OUT, BIT0},
                    .chHall=4,
                    .chIr=5},
                .pIrThreshold=&hh_ir_threshold,
                .pHallThreshold=&hh_hall_threshold,
                .pHallDigit=&hh_hall_digit
            };


static const SplitFlapDef mmSplitFlapDef = {
                .stepperDef = {
                   .gpoDefs[0]={&P2DIR, &P2OUT, BIT5},
                   .gpoDefs[1]={&P2DIR, &P2OUT, BIT6},
                   .gpoDefs[2]={&P3DIR, &P3OUT, BIT7},
                   .gpoDefs[3]={&P4DIR, &P4OUT, BIT0},
                   .direction=AntiClockWise,
                   .divisor=6},
               .detectorDef = {
                   .enableGpoDef={&P2DIR, &P2OUT, BIT4},
                   .chHall=6,
                   .chIr=7},
                .pIrThreshold=&mm_ir_threshold,
                .pHallThreshold=&mm_hall_threshold,
                .pHallDigit=&mm_hall_digit
            };


static const SplitFlapDef wwSplitFlapDef = {
                .stepperDef = {
                    .gpoDefs[0]={&P3DIR, &P3OUT, BIT3},
                    .gpoDefs[1]={&P2DIR, &P2OUT, BIT3},
                    .gpoDefs[2]={&P3DIR, &P3OUT, BIT4},
                    .gpoDefs[3]={&P3DIR, &P3OUT, BIT1},
                    .direction=ClockWise,
                    .divisor=3},
                .detectorDef = {
                    .enableGpoDef={&P3DIR, &P3OUT, BIT0},
                    .chHall=0,
                    .chIr=1},
                .pIrThreshold=&ww_ir_threshold,
                .pHallThreshold=&ww_hall_threshold,
                .pHallDigit=&ww_hall_digit
            };

/* IR DETECTORS */

/* MAGNETIC DETECTORS */


#endif /* BOARD_HPP_ */
