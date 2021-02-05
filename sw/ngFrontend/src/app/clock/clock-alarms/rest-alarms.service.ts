import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import {BackendService} from '../../backend.service';

@Injectable({
  providedIn: 'root'
})
export class RestAlarmsService {


  constructor(private backend: BackendService){}

  getAlarmList(): Observable<any> {
    return this.backend.get('/rest/alarm/get-list');
  }

  setAlarm(alarm): Observable<any> {
    return this.backend.post( '/rest/alarm/set-alarm', alarm);
  }

  deleteAlarm(idx): Observable<any> {
    return this.backend.get('/rest/alarm/delete-alarm?idx=' + idx);
  }

}
