import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-clock-calibrate',
  templateUrl: './clock-calibrate.component.html',
  styleUrls: ['./clock-calibrate.component.css']
})
export class ClockCalibrateComponent implements OnInit {

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
  }

}
