import { Injectable } from '@angular/core';
import {BackendService} from '../backend.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestClockService {


  constructor(private backend: BackendService){}

  getTime(): Observable<any> {
    return this.backend.get('/rest/clock/get-time');
  }

  setTimeZone(timezone): Observable<any> {
    return this.backend.post('/rest/clock/set-timezone', timezone);
  }

  getClockMode(): Observable<any> {
    return this.backend.get('/rest/clock/get-mode');
  }

  setClockMode(value): Observable<any> {
    return this.backend.get('/rest/clock/set-mode?mode=' + value);
  }

  getFlapStatus(type): Observable<any> {
    return this.backend.get('/rest/clock/get-flap-status?type=' + type);
  }

  setFlapParameter(type, parameter, value): Observable<any> {
    return this.backend.get('/rest/clock/set-flap-parameter?type=' + type + '&parameter=' + parameter + '&value=' + value);
  }

}
