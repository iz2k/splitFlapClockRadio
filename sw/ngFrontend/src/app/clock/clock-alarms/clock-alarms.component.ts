import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';
import {RestAlarmsService} from './rest-alarms.service';

@Component({
  selector: 'app-clock-alarms',
  templateUrl: './clock-alarms.component.html',
  styleUrls: ['./clock-alarms.component.css']
})
export class ClockAlarmsComponent implements OnInit {

  alarmList: any;

  constructor(private backend: BackendService,
              private restAlarms: RestAlarmsService) { }

  ngOnInit(): void {
    this.restAlarms.getAlarmList().subscribe(json => {
      this.parseAlarmList(json);
    });
  }

  parseAlarmList(json): void {
      this.alarmList = json;
      console.log(json);
  }

  newAlarm(): void {
      console.log('json');
      this.alarmList.push({
        Active: false,
        EnableWeatherForecast: false,
        Hour: 0,
        Message: '',
        Minute: 0,
        Name: '',
        PlayItem: {},
        PlaySource: '',
        WeekDays: [false, false, false, false, false, false, false]
      });
  }
}
