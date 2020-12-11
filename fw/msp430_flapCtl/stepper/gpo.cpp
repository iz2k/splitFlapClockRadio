#include <stepper/gpo.hpp>


Gpo::Gpo() {
};

Gpo::Gpo(GpoDef gpoDef) {
    this->pDir = gpoDef.pDir;
    this->pOut = gpoDef.pOut;
    this->pBit = gpoDef.pBit;

    //Set pin to output direction
    *this->pDir |= this->pBit;
    this->clear();
};

void Gpo::set() {
    *this->pOut |= this->pBit;
    this->current = true;
};

void Gpo::clear() {
    *this->pOut &= ~this->pBit;
    this->current = false;
};

void Gpo::toggle() {
    this->current ? this->clear() : this->set();
};
