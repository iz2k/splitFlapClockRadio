/*
 * board.hpp
 *
 *  Created on: 11 dic. 2020
 *      Author: IbonZalbide
 */

#ifndef BOARD_HPP_
#define BOARD_HPP_

#include <stepper/stepper.hpp>

/* STEPPERS */
static const StepperDef hhStepperDef = {
                                        .gpoDefs[0]={&P3DIR, &P3OUT, BIT6},
                                        .gpoDefs[1]={&P3DIR, &P3OUT, BIT2},
                                        .gpoDefs[2]={&P3DIR, &P3OUT, BIT5},
                                        .gpoDefs[3]={&P2DIR, &P2OUT, BIT7}};
static const StepperDef mmStepperDef = {
                                        .gpoDefs[0]={&P2DIR, &P2OUT, BIT5},
                                        .gpoDefs[1]={&P2DIR, &P2OUT, BIT6},
                                        .gpoDefs[2]={&P3DIR, &P3OUT, BIT7},
                                        .gpoDefs[3]={&P4DIR, &P4OUT, BIT0}};
static const StepperDef wwStepperDef = {
                                        .gpoDefs[0]={&P3DIR, &P3OUT, BIT3},
                                        .gpoDefs[1]={&P2DIR, &P2OUT, BIT3},
                                        .gpoDefs[2]={&P3DIR, &P3OUT, BIT4},
                                        .gpoDefs[3]={&P3DIR, &P3OUT, BIT1}};

/* IR DETECTORS */

/* MAGNETIC DETECTORS */


#endif /* BOARD_HPP_ */
