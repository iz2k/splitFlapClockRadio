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
    uint8_t currentDigit;
    uint8_t desiredDigit;
    Stepper();
    Stepper(StepperDef, StepperDirection);
    void test();
    void move();
    void stop();
};


#endif /* STEPPER_STEPPER_HPP_ */
