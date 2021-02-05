import { Injectable } from '@angular/core';
import {BackendService} from '../backend.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestSensorsService {


  constructor(private backend: BackendService){}


  getSensors(): Observable<any> {
    return this.backend.get('/rest/sensors/get-current');
  }

  getSensorsConfig(): Observable<any> {
    return this.backend.get('/rest/sensors/get-config');
  }

  resetBaseline(): Observable<any> {
    return this.backend.get('/rest/sensors/reset-baseline');
  }

  reloadSensors(): Observable<any> {
    return this.backend.get('/rest/sensors/reload');
  }

  setSensorsParameters(arglist): Observable<any> {
    let paramsString = '';
    arglist.forEach(arg => paramsString = paramsString + arg.parameter.toString() + '=' +  arg.value.toString() + '&');
    return this.backend.get('/rest/sensors/set-params?' + paramsString);
  }
}
