import {Component, Input, OnInit} from '@angular/core';
import {BackendService} from '../../../backend.service';

@Component({
  selector: 'app-cal-split-flap',
  templateUrl: './cal-split-flap.component.html',
  styleUrls: ['./cal-split-flap.component.css']
})
export class CalSplitFlapComponent implements OnInit {

  @Input()
  type = 'None';
  status;
  statusArray;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.updateStatus();
  }

  updateStatus(): void {
    this.backend.getClockStatus(this.type).subscribe(json =>
    {
      this.status = json;
      console.log(this.status);
      this.updateStatusArray(json);
    });
  }

  updateStatusArray(json): void {
      this.statusArray = [];
      for (let key in json){
        this.statusArray.push({description: key, value: json[key]});
      }
  }

  setParameter(parameter, value): void {
    this.backend.setClockParameter(this.type, parameter, value).subscribe(json =>
    {
      this.status = json;
      console.log(json);
      this.updateStatusArray(json);
    });
  }

}
