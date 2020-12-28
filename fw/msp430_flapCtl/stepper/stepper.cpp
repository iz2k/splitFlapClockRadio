#include <stepper/stepper.hpp>

Stepper::Stepper() {
};

Stepper::Stepper(StepperDef stepperGpoDefs, StepperDirection stepperDirection,
                 uint16_t *ir_threshold, uint16_t *hall_threshold, uint8_t *hall_digit) {
    for(int i=3; i>=0; i--){
        this->gpo[i] = Gpo(stepperGpoDefs.gpoDefs[i]);
    }
    this->idxStep=0;
    this->direction = stepperDirection;
    this->currentDigit = 0;
    this->desiredDigit = 1;
    this->pIrThreshold = ir_threshold;
    this->pHallThreshold = hall_threshold;
    this->pHallDigit = hall_digit;
    this->currentIR = 0;
    this->currentHall = 0;
};

void Stepper::test() {
    this->gpo[0].toggle();
    this->gpo[1].toggle();
    this->gpo[2].toggle();
    this->gpo[3].toggle();
};

const uint8_t stepMatrix [8][4] =
{
  {1, 0, 0, 0},
  {1, 1, 0, 0},
  {0, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 0},
  {0, 0, 1, 1},
  {0, 0, 0, 1},
  {1, 0, 0, 1}
};
void Stepper::move() {
    for(int i=3; i>=0; i--){
        stepMatrix[this->idxStep][i] ? (this->gpo[i].set()) : (this->gpo[i].clear());
    }

    if(this->direction == ClockWise)
    {
        if(--this->idxStep>7)this->idxStep=7;
    }else{
        if(++this->idxStep>7)this->idxStep=0;
    }
};

void Stepper::stop() {
    for(int i=3; i>=0; i--){
        this->gpo[i].clear();
    }
    this->idxStep=0;
};

