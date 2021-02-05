import { Injectable } from '@angular/core';
import {BackendService} from '../backend.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestWeatherService {


  constructor(private backend: BackendService){}

  getWeather(): Observable<any> {
    return this.backend.get('/rest/weather/get-current');
  }

  reloadWeather(): Observable<any> {
    return this.backend.get('/rest/weather/reload');
  }

  getApis(): Observable<any> {
    return this.backend.get('/rest/weather/get-apis');
  }

  setApis(arglist): Observable<any> {
    let paramsString = '';
    arglist.forEach(arg => paramsString = paramsString + arg.parameter.toString() + '=' +  arg.value.toString() + '&');
    return this.backend.get('/rest/weather/set-apis?' + paramsString);
  }

  getLocation(): Observable<any> {
    return this.backend.get('/rest/weather/get-location');
  }

  setLocation(arglist): Observable<any> {
    let paramsString = '';
    arglist.forEach(arg => paramsString = paramsString + arg.parameter.toString() + '=' + arg.value.toString() + '&');
    return this.backend.get('/rest/weather/set-location?' + paramsString);
  }

}
