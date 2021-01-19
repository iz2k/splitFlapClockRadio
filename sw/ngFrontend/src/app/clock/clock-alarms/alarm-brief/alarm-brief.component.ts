import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-alarm-brief',
  templateUrl: './alarm-brief.component.html',
  styleUrls: ['./alarm-brief.component.css']
})
export class AlarmBriefComponent implements OnInit {

  @Input()
  alarm;
  @Input()
  idx;

  constructor() { }

  ngOnInit(): void {
  }

  toggleAlarm(b: boolean): void {
    console.log('toggle alarm');
  }
}
