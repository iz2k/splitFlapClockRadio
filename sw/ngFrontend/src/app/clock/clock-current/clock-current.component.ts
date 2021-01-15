import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-clock-current',
  templateUrl: './clock-current.component.html',
  styleUrls: ['./clock-current.component.css']
})
export class ClockCurrentComponent implements OnInit {

  constructor(private backend: BackendService) { }

  HoursTensPlace = 0;
  HoursOnesPlace = 0;
  MinutesTensPlace = 0;
  MinutesOnesPlace = 0;
  SecondsTensPlace = 0;
  SecondsOnesPlace = 0;
  DateText = '';

  tzFormGroup: FormGroup;
  timezone = new FormControl('');

  clockTime: any;

  monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  ngOnInit(): void {
    this.backend.getTime().subscribe(json => {
      this.updateClockTime(json);
      this.timezone.valueChanges.subscribe(tz => this.timezoneChange(tz));
    });
    this.tzFormGroup = new FormGroup(
{
          timezone: this.timezone
        });
    this.periodicEvent();
  }

  periodicEvent(): void {
    setInterval
      (_ => {
        this.incrementClockTime();
        this.updateFlipClockWidget();
      }, 1000);
  }

  updateClockTime(json): void {
    console.log(json);
    this.clockTime = json;
    if (this.timezone.value.nameValue !== this.clockTime.timezone) {
      this.timezone.setValue(this.clockTime.timezone);
    }
    this.updateFlipClockWidget();
  }

  updateFlipClockWidget(): void {
    this.DateText = this.clockTime.year + ', ' + this.monthNames[this.clockTime.month - 1] + ' ' + this.clockTime.day;
    this.HoursTensPlace = Math.floor(this.clockTime.hour / 10);
    this.HoursOnesPlace = Math.floor(this.clockTime.hour % 10);
    this.MinutesTensPlace = Math.floor(this.clockTime.minute / 10);
    this.MinutesOnesPlace = Math.floor(this.clockTime.minute % 10);
    this.SecondsTensPlace = Math.floor(this.clockTime.second / 10);
    this.SecondsOnesPlace = Math.floor(this.clockTime.second % 10);
  }

  incrementClockTime(): void {
    this.clockTime.second++;
    if (this.clockTime.second > 59) {
      this.clockTime.second = 0;
      this.clockTime.minute++;
      if (this.clockTime.minute > 59){
        this.clockTime.minute = 0;
        this.clockTime.hour++;
        if (this.clockTime.hour > 23){
          this.clockTime.hour = 0;
        }
      }
    }
  }

  timezoneChange(tz): void {
    console.log('timezone changed');
    console.log(tz);
    this.backend.setTimeZone(tz).subscribe(ans => {
      this.backend.getTime().subscribe(json => this.updateClockTime(json));
      console.log(ans);
    });
  }
}
