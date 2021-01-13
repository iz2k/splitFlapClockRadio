import { Injectable } from '@angular/core';
import {Socket} from 'ngx-socket-io';
import {Observable} from 'rxjs';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {backendHost, backendPort} from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BackendService extends Socket {

  private urlEndPoint = 'http://' + backendHost + ':' + backendPort;

  constructor(private http: HttpClient){
        super({ url: 'http://' + backendHost + ':' + backendPort, options: {} });
        console.log('Creating Backend Service');
        this.ioSocket.on('connect', () => console.log('Backend WebSocket Connected'));
  }

  getTime(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-time');
  }

  getStatus(type): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-status?type=' + type);
  }

  getMode(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-mode');
  }

  setMode(value): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/set-mode?mode=' + value);
  }

  setParameter(type, parameter, value): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/set-parameter?type=' + type + '&parameter=' + parameter + '&value=' + value);
  }

  setTimeZone(timezone): Observable<any> {
    return this.http.post<any>(this.urlEndPoint + '/set-timezone', timezone,
      {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      });
  }

  getApiConfig(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-api-config');
  }

  getLocationConfig(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-location-config');
  }

  getSensorsConfig(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-sensors-config');
  }

  getWeather(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-weather');
  }

  setApiParameters(arglist): Observable<any> {
    let paramsString = '';
    arglist.forEach(arg => paramsString = paramsString + arg.parameter.toString() + '=' +  arg.value.toString() + '&');
    return this.http.get<any>(this.urlEndPoint + '/set-api?' + paramsString);
  }

  setLocationParameters(arglist): Observable<any> {
    let paramsString = '';
    arglist.forEach(arg => paramsString = paramsString + arg.parameter.toString() + '=' +  arg.value.toString() + '&');
    return this.http.get<any>(this.urlEndPoint + '/set-location?' + paramsString);
  }

  setSensorsParameters(arglist): Observable<any> {
    let paramsString = '';
    arglist.forEach(arg => paramsString = paramsString + arg.parameter.toString() + '=' +  arg.value.toString() + '&');
    return this.http.get<any>(this.urlEndPoint + '/set-sensors?' + paramsString);
  }

  getHome(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-sensors');
  }

  getMeasurements(filter): Observable<any> {
    return this.http.post<any>(this.urlEndPoint + '/get-measurements', filter,
      {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      });
  }

  resetBaseline(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/reset-sensors-baseline');
  }

  reloadSensors(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/reload-sensors');
  }

  reloadWeather(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/reload-weather');
  }
}
