import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';
import {RestSensorsService} from '../rest-sensors.service';

@Component({
  selector: 'app-sensor-calibration',
  templateUrl: './sensor-calibration.component.html',
  styleUrls: ['./sensor-calibration.component.css']
})
export class SensorCalibrationComponent implements OnInit {

  storedBaselineEco2: any;
  storedBaselineTvoc: any;
  currentBaselineEco2: any;
  currentBaselineTvoc: any;

  constructor(private backend: BackendService,
              private restSensors: RestSensorsService) { }

  ngOnInit(): void {
    this.restSensors.getSensorsConfig().subscribe(json => {
      console.log(json);
      this.parseSensorsConfig(json);
    });
    this.backend.ioSocket.on('sensorData', json => this.parseHome(JSON.parse(json)));
  }

  parseSensorsConfig(json): void {
    this.storedBaselineEco2 = json.baselineEco2;
    this.storedBaselineTvoc = json.baselineTvoc;
  }

  private parseHome(json): void {
    console.log(json);
    this.currentBaselineEco2 = json.baseline[0];
    this.currentBaselineTvoc = json.baseline[1];
  }

  triggerCalibration(): void {
    this.restSensors.resetBaseline().subscribe();
  }

  saveBaselines(): void {
    this.restSensors.setSensorsParameters(
      [
        {parameter: 'baselineEco2', value: this.currentBaselineEco2},
        {parameter: 'baselineTvoc', value: this.currentBaselineTvoc},
      ]).subscribe(json =>
    {
      this.parseSensorsConfig(json);
      this.restSensors.reloadSensors().subscribe();
    });
  }

}
