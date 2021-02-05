import { Component, OnInit } from '@angular/core';
import {RestClockService} from './rest-clock.service';

@Component({
  selector: 'app-clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.css']
})
export class ClockComponent implements OnInit {

  calibrationMode = false;

  constructor(private restClock: RestClockService) { }

  ngOnInit(): void {
      this.restClock.getClockMode().subscribe(json => {this.updateMode(json); });
  }

  applyCalibrationMode(calibrationMode): void {
    if (calibrationMode) {
      this.restClock.setClockMode('calibration').subscribe(json => {this.updateMode(json); });
    }else {
      this.restClock.setClockMode('clock').subscribe(json => {this.updateMode(json); });
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
