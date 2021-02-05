import {Component, Input, OnInit} from '@angular/core';
import {RestClockService} from '../../rest-clock.service';

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

  constructor(private restClock: RestClockService) { }

  ngOnInit(): void {
    this.updateStatus();
  }

  updateStatus(): void {
    this.restClock.getFlapStatus(this.type).subscribe(json =>
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
    this.restClock.setFlapParameter(this.type, parameter, value).subscribe(json =>
    {
      this.status = json;
      console.log(json);
      this.updateStatusArray(json);
    });
  }

}
