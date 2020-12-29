#ifndef STEPPER_GPO_HPP_
#define STEPPER_GPO_HPP_

#include <stdint.h>

struct GpoDef
{
    volatile unsigned char * pDir;
    volatile unsigned char * pOut;
    uint8_t pBit;
};

class Gpo {
  private:
    volatile unsigned char *pDir;
    volatile unsigned char *pOut;
    uint8_t pBit;
    bool current;

  public:
    Gpo();
    Gpo(const GpoDef*);
    void set();
    void clear();
    void toggle();
};



#endif /* STEPPER_GPO_HPP_ */
