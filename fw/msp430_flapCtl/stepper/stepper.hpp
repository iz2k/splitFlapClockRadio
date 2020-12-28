#ifndef STEPPER_STEPPER_HPP_
#define STEPPER_STEPPER_HPP_

#include <stdint.h>
#include "gpo.hpp"

struct StepperDef
{
    GpoDef gpoDefs[4];
};

typedef enum {
    ClockWise,
    AntiClockWise
} StepperDirection;

class Stepper {
  private:
    Gpo gpo[4];
    StepperDirection direction;
    uint8_t idxStep;

  public:
    // Properties
    uint8_t currentDigit;
    uint8_t desiredDigit;
    uint16_t currentIR;
    uint16_t *pIrThreshold;
    uint16_t currentHall;
    uint16_t *pHallThreshold;
    uint8_t *pHallDigit;
    uint8_t syncTrigger;

    // Methods
    Stepper();
    Stepper(StepperDef, StepperDirection, uint16_t*, uint16_t*, uint8_t*);
    void test();
    void move();
    void stop();
    void updateIR(uint16_t);
    void updateHall(uint16_t);
    void run();
};


#endif /* STEPPER_STEPPER_HPP_ */
