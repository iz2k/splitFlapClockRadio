import { Component, OnInit } from '@angular/core';
import {BackendService} from '../backend.service';

@Component({
  selector: 'app-clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.css']
})
export class ClockComponent implements OnInit {

  calibrationMode = false;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
      this.backend.getClockMode().subscribe(json => {this.updateMode(json); });
  }

  applyCalibrationMode(calibrationMode): void {
    if (calibrationMode) {
      this.backend.setClockMode('calibration').subscribe(json => {this.updateMode(json); });
    }else {
      this.backend.setClockMode('clock').subscribe(json => {this.updateMode(json); });
    }
  }

  updateMode(json): void {
    console.log(json);
    if (json === 'clock') {
      this.calibrationMode = false;
      console.log('false');
    }else{
      this.calibrationMode = true;
      console.log('true');
    }
  }
}
