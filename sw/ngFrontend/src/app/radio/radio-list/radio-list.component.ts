import { Component, OnInit } from '@angular/core';
import {RestRadioService} from '../rest-radio.service';

@Component({
  selector: 'app-radio-list',
  templateUrl: './radio-list.component.html',
  styleUrls: ['./radio-list.component.css']
})
export class RadioListComponent implements OnInit {

  radioItems: any;

  constructor(private restRadio: RestRadioService) { }

  ngOnInit(): void {
    this.restRadio.getRadioItems().subscribe(json => {
      this.parseRadioItems(json);
    });
  }

  parseRadioItems(json): void {
      this.radioItems = json;
      console.log(json);
  }

  tune(freq: any): void {
    this.restRadio.tuneRadio(freq).subscribe(json => {
      console.log(json);
    });

  }

  addRadioStation(): void {
    this.restRadio.getRadioStatus().subscribe(json => {
      console.log(json);
      const radioItem = {Name: json.PS, Frequency: json.freq};
      this.radioItems.push(radioItem);
      this.restRadio.addRadioItem(json.freq, json.PS).subscribe(ans => {
        console.log(ans);
      });
    });
  }

  deleteRadioStation(idx: number): void {
    this.radioItems.splice(idx, 1);
    this.restRadio.deleteRadioItem(idx).subscribe(ans => {
        console.log(ans);
      });
  }
}
