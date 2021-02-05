import { Component, OnInit } from '@angular/core';
import {RestSensorsService} from '../rest-sensors.service';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-home-current',
  templateUrl: './sensors-current.component.html',
  styleUrls: ['./sensors-current.component.css']
})
export class SensorsCurrentComponent implements OnInit {

  homeReport: any;

  constructor(private backend: BackendService,
              private restSensors: RestSensorsService) { }

  ngOnInit(): void {
    this.restSensors.getSensors().subscribe(json => {
      this.parseHome(json);
    });
    this.backend.ioSocket.on('sensorData', json => this.parseHome(JSON.parse(json)));
  }

  parseHome(json): void {
      this.homeReport = json;
      console.log(json);
  }
}
