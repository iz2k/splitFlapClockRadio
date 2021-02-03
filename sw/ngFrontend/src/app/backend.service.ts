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

  getClockMode(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-clock-mode');
  }

  setClockMode(value): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/set-clock-mode?mode=' + value);
  }

  getClockStatus(type): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-clock-status?type=' + type);
  }

  setClockParameter(type, parameter, value): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/set-clock-parameter?type=' + type + '&parameter=' + parameter + '&value=' + value);
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

  getRadioStatus(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-radio-status');
  }

  getAlarmList(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-alarm-list');
  }

  setAlarm(alarm): Observable<any> {
    return this.http.post<any>(this.urlEndPoint + '/set-alarm', alarm,
      {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      });
  }

  deleteAlarm(idx): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/delete-alarm?idx=' + idx);
  }

  getRadioItems(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-radio-items');
  }

  tuneRadio(freq): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/set-radio-tune?freq=' + freq);
  }

  addRadioStation(freq, name): Observable<any> {
    return this.http.post<any>(this.urlEndPoint + '/add-radio-item', [freq, name],
      {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      });
  }

  deleteRadioStation(idx): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/delete-radio-item?idx=' + idx);
  }

  getSpotifyStatus(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-spotify-status');
  }

  spotifySearch(type, terms): Observable<any> {
    return this.http.post<any>(this.urlEndPoint + '/spotify-search', {type, terms},
      {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      });
  }

  spotifyPlay(uri): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/spotify-play?uri=' + uri);
  }

  spotifyAddItem(type, name, uri, img): Observable<any> {
    return this.http.post<any>(this.urlEndPoint + '/add-spotify-item', {Type: type, Name: name, URI: uri, Image: img},
      {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      });
  }

  getSpotifyItems(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-spotify-items');
  }

  deleteSpotifyItem(idx): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/delete-spotify-item?idx=' + idx);
  }

  getSpotifyAuth(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-spotify-auth');
  }

  checkSpotifyDevice(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/spotify-check-device');
  }

  startSpotifyAuth(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/spotify-auth-start');
  }

  endSpotifyAuth(code): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/spotify-auth-end?code=' + code);
  }

  spotifyUpdateRaspotifyCredentials(username, password): Observable<any> {
    return this.http.post<any>(this.urlEndPoint + '/spotify-update-raspotify', {username, password},
      {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      });
  }

  getVolume(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-volume');
  }

  setVolume(vol): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/set-volume?vol=' + vol);
  }

  toggleMute(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/toggle-mute');
  }

}
