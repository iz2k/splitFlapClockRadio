import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-radio-current',
  templateUrl: './radio-current.component.html',
  styleUrls: ['./radio-current.component.css']
})
export class RadioCurrentComponent implements OnInit {

  fmRadioReport: any;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.backend.getRadioStatus().subscribe(json => {
      this.parseFmRadioReport(json);
    });
    this.backend.ioSocket.on('fmRadioReport', json => this.parseFmRadioReport(JSON.parse(json)));
  }

  parseFmRadioReport(json): void {
      this.fmRadioReport = json;
      //console.log(json);
  }

  turnOn(event: Event): void {
    this.backend.ioSocket.emit('fmRadio', ['turn_on', 0]);
  }
  turnOff(event: Event): void {
    this.backend.ioSocket.emit('fmRadio', ['turn_off', 0]);
  }
  seekUp(event: Event): void {
    console.log('algo');
    this.backend.ioSocket.emit('fmRadio', ['seek_up', 0]);
  }
  seekDown(event: Event): void {
    this.backend.ioSocket.emit('fmRadio', ['seek_down', 0]);
  }

}
