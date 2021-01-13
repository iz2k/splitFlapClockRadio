import { Component, OnInit } from '@angular/core';
import {FormControl} from '@angular/forms';
import {BackendService} from "../../backend.service";

@Component({
  selector: 'app-clock-current',
  templateUrl: './clock-current.component.html',
  styleUrls: ['./clock-current.component.css']
})
export class ClockCurrentComponent implements OnInit {

  HoursTensPlace = 0;
  HoursOnesPlace = 0;
  MinutesTensPlace = 0;
  MinutesOnesPlace = 0;
  SecondsTensPlace = 0;
  SecondsOnesPlace = 0;
  calibrationMode = false;
  date: FormControl;
  clockTime = {
    year: 2021,
    month: 1,
    day: 13,
    hour: 10,
    minute: 15,
    second: 5
  };

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.backend.getTime().subscribe(json => {
      this.updateClockTime(json);
    });
    this.periodicEvent();
  }

  periodicEvent(): void {
    setInterval
      (_ => {
        this.incrementClockTime();
        if (!this.calibrationMode) {
          this.updateFlipClockWidget();
        }
      }, 1000);
  }

  updateClockTime(json): void {
    console.log(json);
    this.clockTime = json;
    this.updateFlipClockWidget();
  }

  updateFlipClockWidget(): void {
      this.date = new FormControl(new Date(this.clockTime.year, this.clockTime.month - 1, this.clockTime.day,
                                          this.clockTime.hour, this.clockTime.minute, this.clockTime.second));
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
}
