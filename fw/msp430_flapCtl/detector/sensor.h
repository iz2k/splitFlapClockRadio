/*
 * Sensor.h
 *
 *  Created on: 28 dic. 2020
 *      Author: IbonZalbide
 */

#ifndef DETECTOR_SENSOR_H_
#define DETECTOR_SENSOR_H_

class Sensor
{
public:
    Sensor();
    virtual ~Sensor();

    void enableSensorAll();
    void disableSensorAll();
    void enableSensorHH();
    void disableSensorHH();
    void enableSensorMM();
    void disableSensorMM();
    void enableSensorWW();
    void  disableSensorWW();

};

#endif /* DETECTOR_SENSOR_H_ */
