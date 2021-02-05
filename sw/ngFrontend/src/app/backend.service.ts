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

  get(url): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + url);
  }

  post(url, json): Observable<any> {
    return this.http.post<any>(this.urlEndPoint + url, json,
      {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      });
  }

}
