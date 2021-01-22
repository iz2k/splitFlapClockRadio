import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-radio-list',
  templateUrl: './radio-list.component.html',
  styleUrls: ['./radio-list.component.css']
})
export class RadioListComponent implements OnInit {

  radioItems: any;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.backend.getRadioItems().subscribe(json => {
      this.parseRadioItems(json);
    });
  }

  parseRadioItems(json): void {
      this.radioItems = json;
      console.log(json);
  }

  tune(freq: any): void {
    this.backend.tuneRadio(freq).subscribe(json => {
      console.log(json);
    });

  }

  addRadioStation(): void {
    this.backend.getRadioStatus().subscribe(json => {
      console.log(json);
      const radioItem = {Name: json.PS, Frequency: json.freq};
      this.radioItems.push(radioItem);
      this.backend.addRadioStation(json.freq, json.PS).subscribe(ans => {
        console.log(ans);
      });
    });
  }

  deleteRadioStation(idx: number): void {
    this.radioItems.pop(idx);
    this.backend.deleteRadioStation(idx).subscribe(ans => {
        console.log(ans);
      });
  }
}
