#include <stepper/Stepper.h>

Stepper::Stepper() {
};

Stepper::Stepper(const StepperDef *stepperDef) {
    for(int i=3; i>=0; i--){
        this->gpo[i] = Gpo(&(*stepperDef).gpoDefs[i]);
    }
    this->direction = (*stepperDef).direction;
    this->idxStep=0;
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
