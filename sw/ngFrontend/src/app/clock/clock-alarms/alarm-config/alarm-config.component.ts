import {Component, Inject, OnInit} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {BackendService} from '../../../backend.service';
import {RestRadioService} from '../../../radio/rest-radio.service';
import {RestSpotifyService} from '../../../spotify/rest-spotify.service';

@Component({
  selector: 'app-alarm-config',
  templateUrl: './alarm-config.component.html',
  styleUrls: ['./alarm-config.component.css']
})
export class AlarmConfigComponent implements OnInit {

  time;
  radioList: any;
  spotifyList: any;

  constructor(
    public dialogRef: MatDialogRef<AlarmConfigComponent>,
    private backend: BackendService,
    private restRadio: RestRadioService,
    private restSpotify: RestSpotifyService,
    @Inject(MAT_DIALOG_DATA) public alarm: any) {}

  onCancel(): void {
    this.dialogRef.close();
  }

  ngOnInit(): void {
    console.log(this.alarm);
    this.time = {hour: this.alarm.Hour, minute: this.alarm.Minute};
    this.restRadio.getRadioItems().subscribe(json => {
      this.radioList = json;
      console.log(json);
    });
    this.restSpotify.getSpotifyItems().subscribe(json => {
      this.spotifyList = json;
      console.log(json);
    });
  }

  onApply(): void {
    this.alarm.Hour = this.time.hour;
    this.alarm.Minute = this.time.minute;
    this.dialogRef.close(this.alarm);
  }
}
