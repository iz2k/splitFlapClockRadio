import { Injectable } from '@angular/core';
import {BackendService} from '../backend.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestAudioService {


  constructor(private backend: BackendService){}

  getVolume(): Observable<any> {
    return this.backend.get('/rest/audio/get-volume');
  }

  setVolume(vol): Observable<any> {
    return this.backend.get('/rest/audio/set-volume?vol=' + vol);
  }

  toggleMute(): Observable<any> {
    return this.backend.get('/rest/audio/toggle-mute');
  }

}
