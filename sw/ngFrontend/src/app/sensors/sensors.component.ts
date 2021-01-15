import { Component, OnInit } from '@angular/core';
import {BackendService} from '../backend.service';

@Component({
  selector: 'app-sensors',
  templateUrl: './sensors.component.html',
  styleUrls: ['./sensors.component.css']
})
export class SensorsComponent implements OnInit {

  calibrationMode = false;
  constructor() { }

  ngOnInit(): void {
  }

  applyCalibrationMode(calibrationMode): void {
    this.calibrationMode = calibrationMode;
  }
}
