#ifndef STEPPER_STEPPER_HPP_
#define STEPPER_STEPPER_HPP_

#include <stdint.h>
#include <gpo/Gpo.h>

typedef enum {
    ClockWise,
    AntiClockWise
} StepperDirection;

struct StepperDef
{
    GpoDef gpoDefs[4];
    StepperDirection direction;
    uint8_t divisor;
};


class Stepper {
  private:
    Gpo gpo[4];
    StepperDirection direction;
    uint8_t idxStep;
    uint8_t divisor;
    uint8_t idxDiv;

  public:

    // Methods
    Stepper();
    Stepper(const StepperDef*);
    void move();
    void stop();
};


#endif /* STEPPER_STEPPER_HPP_ */
