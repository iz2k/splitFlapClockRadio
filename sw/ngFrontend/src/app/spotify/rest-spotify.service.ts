import { Injectable } from '@angular/core';
import {BackendService} from '../backend.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestSpotifyService {


  constructor(private backend: BackendService){}

  getSpotifyStatus(): Observable<any> {
    return this.backend.get('/rest/spotify/get-status');
  }

  spotifySearch(type, terms): Observable<any> {
    return this.backend.post('/rest/spotify/search', {type, terms});
  }

  spotifyPlay(uri): Observable<any> {
    return this.backend.get('/rest/spotify/play?uri=' + uri);
  }

  getSpotifyItems(): Observable<any> {
    return this.backend.get('/rest/spotify/get-items');
  }

  spotifyAddItem(type, name, uri, img): Observable<any> {
    return this.backend.post('/rest/spotify/add-item',
      {Type: type, Name: name, URI: uri, Image: img});
  }

  deleteSpotifyItem(idx): Observable<any> {
    return this.backend.get('/rest/spotify/delete-item?idx=' + idx);
  }

  getSpotifyAuth(): Observable<any> {
    return this.backend.get('/rest/spotify/get-auth-status');
  }

  checkSpotifyDevice(): Observable<any> {
    return this.backend.get('/rest/spotify/check-device');
  }

  spotifyUpdateRaspotifyCredentials(username, password): Observable<any> {
    return this.backend.post('/rest/spotify/update-raspotify',
      {username, password});
  }

}
