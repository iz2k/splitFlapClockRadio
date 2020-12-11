#include <stepper/stepper.hpp>

Stepper::Stepper() {
};

Stepper::Stepper(StepperDef stepperGpoDefs) {
    for(int i=3; i>=0; i--){
        this->gpo[i] = Gpo(stepperGpoDefs.gpoDefs[i]);
    }
};

void Stepper::test() {
    this->gpo[0].toggle();
    this->gpo[1].toggle();
    this->gpo[2].toggle();
    this->gpo[3].toggle();
};
