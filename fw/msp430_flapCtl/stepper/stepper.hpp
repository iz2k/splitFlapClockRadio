#ifndef STEPPER_STEPPER_HPP_
#define STEPPER_STEPPER_HPP_

#include <stdint.h>
#include "gpo.hpp"

struct StepperDef
{
    GpoDef gpoDefs[4];
};

class Stepper {
  private:
    Gpo gpo[4];

  public:
    Stepper();
    Stepper(StepperDef);
    void test();
};


#endif /* STEPPER_STEPPER_HPP_ */
