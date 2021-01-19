import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-clock-alarms',
  templateUrl: './clock-alarms.component.html',
  styleUrls: ['./clock-alarms.component.css']
})
export class ClockAlarmsComponent implements OnInit {

  alarmList: any;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.backend.getAlarmList().subscribe(json => {
      this.parseAlarmList(json);
    });
  }

  parseAlarmList(json): void {
      this.alarmList = json;
      console.log(json);
  }

}
