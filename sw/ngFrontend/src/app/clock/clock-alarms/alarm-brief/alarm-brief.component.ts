import {Component, Input, OnInit} from '@angular/core';
import {AlarmConfigComponent} from '../alarm-config/alarm-config.component';
import {MatDialog} from '@angular/material/dialog';
import {RestAlarmsService} from '../rest-alarms.service';

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

  constructor(public dialog: MatDialog,
              private clockAlarmBackend: RestAlarmsService
              ) { }

  ngOnInit(): void {
  }

  toggleAlarm(b: boolean): void {
    console.log('toggle alarm');
    this.alarm.Active = b;
    this.setAlarmConfig([this.idx, this.alarm]);
  }

  openDialogEdit(): void {
    const dialogRef = this.dialog.open(AlarmConfigComponent, {
      data: JSON.parse(JSON.stringify(this.alarm))
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      if (result !== undefined){
        console.log(result);
        this.alarm = result;
        this.setAlarmConfig([this.idx, this.alarm]);
      }
    });
  }

  delete(): void {
    this.alarm = undefined;
    this.clockAlarmBackend.deleteAlarm(this.idx).subscribe(ans => {
      console.log(ans);
    });
  }

  setAlarmConfig(idxAndAlarm): void {
    this.clockAlarmBackend.setAlarm(idxAndAlarm).subscribe(ans => {
      console.log(ans);
    });
  }
}
